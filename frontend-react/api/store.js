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
  const hay = String(text || '').toLowerCase().trim();
  const normalized = hay.replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();

  // High severity phrases generally mapped to direct threats / extreme abuse.
  const blockedPatterns = [
    /\bkill yourself\b/,
    /\byou should die\b/,
    /\bdeserve to die\b/,
    /\bgo die\b/,
    /\bhang yourself\b/,
    /\bsubhuman\b/,
  ];

  // Slurs and targeted hate terms.
  const slurPatterns = [
    /\bnigger\b/,
    /\bnigga\b/,
    /\bfaggot\b/,
    /\bdyke\b/,
    /\bchink\b/,
    /\bwetback\b/,
    /\braghead\b/,
    /\bcoon\b/,
    /\btranny\b/,
    /\bmuzzie\b/,
  ];

  // Lower severity abusive/profane language.
  const abusivePatterns = [
    /\bbitch\b/,
    /\bhoes?\b/,
    /\bpussy\b/,
    /\bretard(ed)?\b/,
    /\btrash\b/,
    /\bidiot\b/,
    /\bstupid\b/,
    /\bscum\b/,
  ];

  const hasBlocked = blockedPatterns.some((p) => p.test(normalized));
  const hasSlur = slurPatterns.some((p) => p.test(normalized));
  const hasAbuse = abusivePatterns.some((p) => p.test(normalized));

  let score = 0;
  if (hasBlocked) score += 3;
  if (hasSlur) score += 2;
  if (hasAbuse) score += 1;

  if (score >= 3) {
    return {
      is_hate_speech: true,
      confidence: Math.min(0.99, 0.55 + score * 0.1),
      category: hasSlur ? 'hate' : 'general',
      action_taken: 'block',
      message: 'Post blocked due to high-confidence hate speech.',
      message_key: 'post_blocked_high_confidence_hate_speech',
      message_params: {},
    };
  }

  if (score > 0) {
    return {
      is_hate_speech: true,
      confidence: Math.min(0.89, 0.45 + score * 0.12),
      category: hasSlur ? 'hate' : 'abusive',
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
