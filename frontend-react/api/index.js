const {
  state,
  send,
  nowIso,
  normalizeUser,
  findUserById,
  findUserByUsername,
  classifyText,
  toClientPost,
} = require('./store');

function getPathParts(req) {
  const raw = (req.url || '/').split('?')[0];
  const cleaned = raw.replace(/^\//, '').replace(/^api\/?/, '');
  return cleaned ? cleaned.split('/').filter(Boolean) : [];
}

const WARNING_LIMIT = 3;

function applyModerationWarning(user, result) {
  if (!user || !result?.is_hate_speech) {
    return { suspendedNow: false };
  }

  user.warning_count = (user.warning_count || 0) + 1;
  state.violations.push({
    id: state.nextViolationId++,
    user_id: user.id,
    username: user.username,
    action: result.action_taken === 'block' ? 'block' : 'warn',
    category: result.category || 'general',
    confidence: result.confidence || 0.7,
    created_at: nowIso(),
  });

  const suspendedNow = !user.is_suspended && user.warning_count >= WARNING_LIMIT;
  if (suspendedNow) {
    user.is_suspended = true;
    state.violations.push({
      id: state.nextViolationId++,
      user_id: user.id,
      username: user.username,
      action: 'suspend',
      category: 'general',
      confidence: 1,
      created_at: nowIso(),
    });
  }

  return { suspendedNow };
}

module.exports = function handler(req, res) {
  const method = req.method;
  const parts = getPathParts(req);

  if (method === 'OPTIONS') {
    return res.status(204).end();
  }

  if (parts[0] === 'auth' && parts[1] === 'register' && method === 'POST') {
    const { username, email, password } = req.body || {};
    if (!username || !email || !password) return send(res, 400, { error: 'Missing required fields' });
    if (findUserByUsername(username)) return send(res, 409, { error: 'Username already exists' });

    const user = {
      id: state.nextUserId++, username, email, password,
      isAdmin: false, is_suspended: false, warning_count: 0, followers: [], following: [],
    };
    state.users.push(user);
    return send(res, 201, { message: 'Registered successfully', user: normalizeUser(user) });
  }

  if (parts[0] === 'auth' && parts[1] === 'login' && method === 'POST') {
    const { username, password } = req.body || {};
    const user = findUserByUsername(username);
    if (!user || user.password !== password) return send(res, 401, { error: 'Invalid username or password' });
    if (user.is_suspended) return send(res, 403, { error: 'Account suspended' });
    return send(res, 200, { message: 'Login successful', user: normalizeUser(user) });
  }

  if (parts[0] === 'auth' && parts[1] === 'logout' && method === 'POST') {
    return send(res, 200, { message: 'Logged out' });
  }

  if (parts[0] === 'analyze' && method === 'POST') {
    const { text, user_id } = req.body || {};
    const result = classifyText(text);

    const user = findUserById(user_id);
    if (user && user.is_suspended) {
      return send(res, 200, {
        result: {
          is_hate_speech: true,
          confidence: 1,
          category: 'general',
        },
        action_taken: 'block',
        message: 'Account suspended after 3 warnings. Contact admin to reactivate.',
        message_key: 'account_suspended_after_warnings',
        message_params: { warning_limit: WARNING_LIMIT },
        warning_count: user.warning_count || 0,
        account_suspended: true,
      });
    }

    const { suspendedNow } = applyModerationWarning(user, result);

    if (suspendedNow) {
      return send(res, 200, {
        result: {
          is_hate_speech: true,
          confidence: 1,
          category: result.category || 'general',
        },
        action_taken: 'block',
        message: 'Account suspended after 3 warnings. Contact admin to reactivate.',
        message_key: 'account_suspended_after_warnings',
        message_params: { warning_limit: WARNING_LIMIT },
        warning_count: user.warning_count || WARNING_LIMIT,
        account_suspended: true,
      });
    }

    return send(res, 200, {
      result: {
        is_hate_speech: result.is_hate_speech,
        confidence: result.confidence,
        category: result.category,
      },
      action_taken: result.action_taken,
      message: result.message,
      message_key: result.message_key,
      message_params: result.message_params,
      warning_count: user ? (user.warning_count || 0) : 0,
      account_suspended: !!user?.is_suspended,
    });
  }

  if (parts[0] === 'posts' && parts.length === 1 && method === 'GET') {
    const viewerId = req.query?.viewer_id;
    const posts = [...state.posts]
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      .map((p) => toClientPost(p, viewerId));
    return send(res, 200, { posts, page: 1 });
  }

  if (parts[0] === 'posts' && parts.length === 1 && method === 'POST') {
    const { content, user_id, image_url } = req.body || {};
    const author = findUserById(user_id);
    if (!author) return send(res, 400, { error: 'Invalid user_id' });
    if (author.is_suspended) {
      return send(res, 403, {
        error: 'Account suspended after 3 warnings. Contact admin to reactivate.',
        error_key: 'account_suspended_after_warnings',
      });
    }

    const analysis = classifyText(content || '');
    if (analysis.action_taken === 'block') {
      return send(res, 403, {
        error: analysis.message,
        error_key: 'post_blocked_high_confidence_hate_speech',
        analysis: { category: analysis.category, confidence: analysis.confidence },
      });
    }

    const post = {
      id: state.nextPostId++,
      user_id: Number(user_id),
      username: author.username,
      content: content || '',
      image_url: image_url || null,
      likes: [],
      comments: [],
      created_at: nowIso(),
    };
    state.posts.push(post);
    return send(res, 201, { post: toClientPost(post, user_id) });
  }

  if (parts[0] === 'posts' && parts.length >= 2) {
    const postId = Number(parts[1]);
    const post = state.posts.find((p) => p.id === postId);
    if (!post) return send(res, 404, { error: 'Post not found' });

    if (parts[2] === 'like' && method === 'POST') {
      const userId = Number(req.body?.user_id || req.query?.viewer_id || 1);
      if (!post.likes.includes(userId)) post.likes.push(userId);
      return send(res, 200, { success: true, likes_count: post.likes.length });
    }

    if (parts[2] === 'unlike' && method === 'POST') {
      const userId = Number(req.body?.user_id || req.query?.viewer_id || 1);
      post.likes = post.likes.filter((id) => id !== userId);
      return send(res, 200, { success: true, likes_count: post.likes.length });
    }

    if (parts[2] === 'comments' && method === 'POST') {
      const text = String(req.body?.comment || '').trim();
      const userId = Number(req.body?.user_id);
      const user = findUserById(userId);
      if (!text || !user) return send(res, 400, { error: 'Invalid comment payload' });
      if (user.is_suspended) {
        return send(res, 403, {
          error: 'Account suspended after 3 warnings. Contact admin to reactivate.',
          error_key: 'account_suspended_after_warnings',
        });
      }

      const analysis = classifyText(text);
      if (analysis.action_taken === 'block') {
        return send(res, 403, {
          error: 'Comment blocked due to hate speech.',
          error_key: 'comment_blocked_high_confidence_hate_speech',
          analysis: { category: analysis.category, confidence: analysis.confidence },
        });
      }

      const comment = {
        id: state.nextCommentId++,
        user_id: user.id,
        username: req.body?.username || user.username,
        text,
        created_at: nowIso(),
      };
      post.comments.push(comment);
      return send(res, 201, { comment });
    }

    if (parts.length === 2 && method === 'DELETE') {
      const userId = Number(req.body?.user_id);
      const idx = state.posts.findIndex((p) => p.id === postId);
      if (idx < 0) return send(res, 404, { error: 'Post not found' });
      if (state.posts[idx].user_id !== userId) return send(res, 403, { error: 'Only owner can delete this post' });
      state.posts.splice(idx, 1);
      return send(res, 200, { success: true });
    }
  }

  if (parts[0] === 'users' && parts.length === 1 && method === 'GET') {
    const username = String(req.query?.username || '').trim().toLowerCase();
    const viewerId = Number(req.query?.viewer_id);
    let users = state.users;
    if (username) users = users.filter((u) => u.username.toLowerCase().includes(username));
    return send(res, 200, { users: users.map((u) => normalizeUser(u, viewerId)) });
  }

  if (parts[0] === 'users' && parts.length >= 2) {
    const userId = Number(parts[1]);
    const user = findUserById(userId);
    if (!user) return send(res, 404, { error: 'User not found' });

    if (parts.length === 2 && method === 'GET') {
      return send(res, 200, { user: normalizeUser(user, req.query?.viewer_id) });
    }

    if (parts[2] === 'posts' && method === 'GET') {
      const posts = state.posts
        .filter((p) => p.user_id === userId)
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
        .map((p) => toClientPost(p, req.query?.viewer_id));
      return send(res, 200, { posts });
    }

    if (parts[2] === 'follow' && method === 'POST') {
      const followerId = Number(req.body?.follower_id);
      const follower = findUserById(followerId);
      if (!follower || follower.id === user.id) return send(res, 400, { error: 'Invalid follow request' });
      if (!user.followers.includes(follower.id)) user.followers.push(follower.id);
      if (!follower.following.includes(user.id)) follower.following.push(user.id);
      return send(res, 200, { message: 'Followed successfully', user: normalizeUser(user, follower.id) });
    }

    if (parts[2] === 'unfollow' && method === 'POST') {
      const followerId = Number(req.body?.follower_id);
      const follower = findUserById(followerId);
      if (!follower || follower.id === user.id) return send(res, 400, { error: 'Invalid unfollow request' });
      user.followers = user.followers.filter((id) => id !== follower.id);
      follower.following = follower.following.filter((id) => id !== user.id);
      return send(res, 200, { message: 'Unfollowed successfully', user: normalizeUser(user, follower.id) });
    }

    if (parts[2] === 'warn' && method === 'POST') {
      user.warning_count = (user.warning_count || 0) + 1;
      state.violations.push({
        id: state.nextViolationId++,
        user_id: user.id,
        username: user.username,
        action: 'warn',
        category: 'general',
        confidence: 0.75,
        created_at: nowIso(),
      });
      if (user.warning_count >= WARNING_LIMIT && !user.is_suspended) {
        user.is_suspended = true;
        state.violations.push({
          id: state.nextViolationId++,
          user_id: user.id,
          username: user.username,
          action: 'suspend',
          category: 'general',
          confidence: 1,
          created_at: nowIso(),
        });
        return send(res, 200, { message: 'User warned and auto-suspended at 3 warnings' });
      }
      return send(res, 200, { message: 'User warned successfully' });
    }

    if (parts[2] === 'suspend' && method === 'POST') {
      user.is_suspended = true;
      state.violations.push({
        id: state.nextViolationId++,
        user_id: user.id,
        username: user.username,
        action: 'suspend',
        category: 'general',
        confidence: 0.95,
        created_at: nowIso(),
      });
      return send(res, 200, { message: 'User suspended successfully' });
    }

    if (parts[2] === 'unsuspend' && method === 'POST') {
      user.is_suspended = false;
      return send(res, 200, { message: 'User unsuspended successfully' });
    }
  }

  if (parts[0] === 'statistics' && method === 'GET') {
    const totalUsers = state.users.length;
    const suspendedUsers = state.users.filter((u) => u.is_suspended).length;
    const totalViolations = state.violations.length;
    const totalPosts = state.posts.length;
    const hateSpeechPercent = totalPosts > 0 ? Math.round((totalViolations / totalPosts) * 100) : 0;
    return send(res, 200, {
      statistics: {
        total_users: totalUsers,
        suspended_users: suspendedUsers,
        total_violations: totalViolations,
        hate_speech_percentage: hateSpeechPercent,
      },
    });
  }

  if (parts[0] === 'violations' && method === 'GET') {
    return send(res, 200, { violations: state.violations.slice().reverse(), page: 1 });
  }

  if (parts[0] === 'admin' && parts[1] === 'lexicon' && parts[2] === 'reload' && method === 'POST') {
    state.lexicon.updated_at = nowIso();
    return send(res, 200, {
      success: true,
      words_count: state.lexicon.words_count,
      phrases_count: state.lexicon.phrases_count,
      path: state.lexicon.path,
      updated_at: state.lexicon.updated_at,
      message: 'Lexicon reloaded',
      message_key: 'lexicon_reloaded',
    });
  }

  if (parts[0] === 'admin' && parts[1] === 'lexicon' && parts[2] === 'stats' && method === 'GET') {
    return send(res, 200, {
      success: true,
      words_count: state.lexicon.words_count,
      phrases_count: state.lexicon.phrases_count,
      path: state.lexicon.path,
      updated_at: state.lexicon.updated_at,
    });
  }

  if (parts[0] === 'admin' && parts[1] === 'lexicon' && parts[2] === 'update' && method === 'POST') {
    const content = String(req.body?.content || '').trim();
    const mode = req.body?.mode === 'replace' ? 'replace' : 'append';
    if (!content) return send(res, 400, { error: 'Content is required', message_key: 'lexicon_update_failed' });

    const lines = content.split(/\r?\n/).filter((line) => line.trim().length > 0);
    if (mode === 'replace') {
      state.lexicon.words_count = lines.length;
      state.lexicon.phrases_count = 0;
    } else {
      state.lexicon.words_count += lines.length;
    }
    state.lexicon.updated_at = nowIso();

    return send(res, 200, {
      success: true,
      words_count: state.lexicon.words_count,
      phrases_count: state.lexicon.phrases_count,
      path: state.lexicon.path,
      updated_at: state.lexicon.updated_at,
      message: mode === 'replace' ? 'Lexicon replaced' : 'Lexicon appended',
      message_key: mode === 'replace' ? 'lexicon_replaced' : 'lexicon_appended',
    });
  }

  return send(res, 404, { error: 'Not found', path: `/${parts.join('/')}`, method });
};
