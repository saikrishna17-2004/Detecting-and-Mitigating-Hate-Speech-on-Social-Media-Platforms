const nowIso = () => new Date().toISOString();

const state = {
  users: [
    {
      id: 1,
      username: 'admin',
      email: 'admin@demo.app',
      password: 'admin123',
      isAdmin: true,
      is_suspended: false,
      warning_count: 0,
      followers: [],
      following: [],
    },
    {
      id: 2,
      username: 'demo',
      email: 'demo@demo.app',
      password: 'demo123',
      isAdmin: false,
      is_suspended: false,
      warning_count: 0,
      followers: [1],
      following: [1],
    },
  ],
  posts: [
    {
      id: 1,
      user_id: 2,
      username: 'demo',
      content: 'Welcome to the installable PWA app!',
      image_url: null,
      likes: [1],
      comments: [
        { id: 1, user_id: 1, username: 'admin', text: 'Great start!', created_at: nowIso() },
      ],
      created_at: nowIso(),
    },
  ],
  violations: [],
  lexicon: {
    words_count: 5,
    phrases_count: 2,
    path: 'in-memory://fallback-lexicon',
    updated_at: nowIso(),
  },
  nextUserId: 3,
  nextPostId: 2,
  nextCommentId: 2,
  nextViolationId: 1,
};

function send(res, status, payload) {
  res.status(status).json(payload);
}

function normalizeUser(user, viewerId) {
  const viewer = Number(viewerId);
  return {
    id: user.id,
    username: user.username,
    email: user.email,
    isAdmin: !!user.isAdmin,
    is_suspended: !!user.is_suspended,
    warning_count: user.warning_count || 0,
    followers_count: user.followers.length,
    following_count: user.following.length,
    is_following: Number.isFinite(viewer) ? user.followers.includes(viewer) : false,
  };
}

function findUserById(id) {
  return state.users.find((u) => u.id === Number(id));
}

function findUserByUsername(username) {
  return state.users.find((u) => u.username.toLowerCase() === String(username || '').toLowerCase());
}

function classifyText(text) {
  const hay = String(text || '').toLowerCase();
  const blockedWords = ['kill yourself', 'die', 'worthless', 'subhuman', 'hate you'];
  const warnWords = ['idiot', 'stupid', 'trash'];

  const blocked = blockedWords.some((w) => hay.includes(w));
  const warning = !blocked && warnWords.some((w) => hay.includes(w));

  if (blocked) {
    return {
      is_hate_speech: true,
      confidence: 0.93,
      category: 'general',
      action_taken: 'block',
      message: 'Post blocked due to high-confidence hate speech.',
      message_key: 'post_blocked_high_confidence_hate_speech',
      message_params: {},
    };
  }

  if (warning) {
    return {
      is_hate_speech: true,
      confidence: 0.68,
      category: 'general',
      action_taken: 'warn',
      message: 'Potentially harmful language detected.',
      message_key: 'content_flagged_hate_speech',
      message_params: {},
    };
  }

  return {
    is_hate_speech: false,
    confidence: 0.02,
    category: 'none',
    action_taken: 'allow',
    message: 'Content looks safe.',
    message_key: 'content_safe',
    message_params: {},
  };
}

function toClientPost(post, viewerId) {
  const viewer = Number(viewerId);
  const author = findUserById(post.user_id);
  return {
    id: post.id,
    user_id: post.user_id,
    username: post.username,
    content: post.content,
    image_url: post.image_url,
    comments: post.comments,
    likes_count: post.likes.length,
    isLiked: Number.isFinite(viewer) ? post.likes.includes(viewer) : false,
    is_following: Number.isFinite(viewer) && author ? author.followers.includes(viewer) : false,
    created_at: post.created_at,
  };
}

module.exports = {
  state,
  send,
  nowIso,
  normalizeUser,
  findUserById,
  findUserByUsername,
  classifyText,
  toClientPost,
};
