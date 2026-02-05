from datetime import datetime
import os
from pymongo import MongoClient, ASCENDING, DESCENDING, ReturnDocument
from werkzeug.security import generate_password_hash, check_password_hash

_client = None
_db = None


def _get_db():
    """Return a singleton MongoDB client and database."""
    global _client, _db
    if _client is not None and _db is not None:
        return _client, _db

    database_url = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/hate_speech_detection')
    _client = MongoClient(database_url)
    _db = _client.get_default_database()

    if _db is None:
        _db = _client['hate_speech_detection']

    return _client, _db


def init_db():
    """Initialize collections, indexes, and counters."""
    _, db = _get_db()

    db.users.create_index([('username', ASCENDING)], unique=True)
    db.users.create_index([('email', ASCENDING)], unique=True)
    db.posts.create_index([('created_at', DESCENDING)])
    db.violations.create_index([('timestamp', DESCENDING)])
    db.violations.create_index([('category', ASCENDING)])
    db.users.create_index([('is_suspended', ASCENDING)])

    for name in ['users', 'posts', 'violations']:
        db.counters.update_one(
            {'_id': name},
            {'$setOnInsert': {'seq': 0}},
            upsert=True
        )


def _get_next_sequence(name):
    _, db = _get_db()
    counter = db.counters.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return int(counter['seq'])


def _user_to_dict(user_doc, violations_count=None):
    if not user_doc:
        return None
    return {
        'id': user_doc['id'],
        'username': user_doc['username'],
        'email': user_doc['email'],
        'warning_count': user_doc.get('warning_count', 0),
        'is_suspended': user_doc.get('is_suspended', False),
        'suspended_at': user_doc.get('suspended_at').isoformat() if user_doc.get('suspended_at') else None,
        'created_at': user_doc.get('created_at').isoformat() if user_doc.get('created_at') else None,
        'violations_count': violations_count if violations_count is not None else 0
    }


def _violation_to_dict(violation_doc, username=None):
    if not violation_doc:
        return None
    content = violation_doc.get('content', '')
    return {
        'id': violation_doc['id'],
        'user_id': violation_doc['user_id'],
        'username': username,
        'content': content[:100] + '...' if len(content) > 100 else content,
        'category': violation_doc.get('category'),
        'confidence_score': round(float(violation_doc.get('confidence_score', 0.0)), 3),
        'language': violation_doc.get('language', 'en'),
        'timestamp': violation_doc.get('timestamp').isoformat() if violation_doc.get('timestamp') else None,
        'action_taken': violation_doc.get('action_taken')
    }


def _post_to_dict(post_doc, username=None):
    if not post_doc:
        return None
    return {
        'id': post_doc['id'],
        'user_id': post_doc['user_id'],
        'username': username,
        'content': post_doc.get('content'),
        'image_url': post_doc.get('image_url'),
        'is_hate_speech': post_doc.get('is_hate_speech', False),
        'confidence_score': round(float(post_doc.get('confidence_score', 0.0)), 3),
        'likes_count': post_doc.get('likes_count', 0),
        'created_at': post_doc.get('created_at').isoformat() if post_doc.get('created_at') else None
    }


def create_user(username, email, password):
    _, db = _get_db()
    user_doc = {
        'id': _get_next_sequence('users'),
        'username': username,
        'email': email,
        'password_hash': generate_password_hash(password),
        'warning_count': 0,
        'is_suspended': False,
        'suspended_at': None,
        'created_at': datetime.utcnow()
    }
    db.users.insert_one(user_doc)
    return user_doc


def create_user_with_id(user_id, username, email, password=None):
    _, db = _get_db()
    user_doc = {
        'id': int(user_id),
        'username': username,
        'email': email,
        'password_hash': generate_password_hash(password) if password else None,
        'warning_count': 0,
        'is_suspended': False,
        'suspended_at': None,
        'created_at': datetime.utcnow()
    }
    db.users.insert_one(user_doc)
    return user_doc


def update_user(user_id, updates):
    _, db = _get_db()
    db.users.update_one({'id': int(user_id)}, {'$set': updates})
    return get_user_by_id(user_id)


def increment_user_warning(user_id, count=1):
    _, db = _get_db()
    db.users.update_one({'id': int(user_id)}, {'$inc': {'warning_count': count}})
    return get_user_by_id(user_id)


def get_user_by_id(user_id):
    _, db = _get_db()
    return db.users.find_one({'id': int(user_id)})


def get_user_by_username(username):
    _, db = _get_db()
    return db.users.find_one({'username': username})


def get_user_by_email(email):
    _, db = _get_db()
    return db.users.find_one({'email': email})


def list_users():
    _, db = _get_db()
    return list(db.users.find({}))


def count_users(filter_query=None):
    _, db = _get_db()
    return db.users.count_documents(filter_query or {})


def count_suspended_users():
    return count_users({'is_suspended': True})


def check_password(user_doc, password):
    if not user_doc or not user_doc.get('password_hash'):
        return False
    return check_password_hash(user_doc['password_hash'], password)


def create_violation(data):
    _, db = _get_db()
    violation_doc = {
        'id': _get_next_sequence('violations'),
        'user_id': int(data['user_id']),
        'content': data['content'],
        'category': data['category'],
        'confidence_score': float(data['confidence_score']),
        'language': data.get('language', 'en'),
        'timestamp': data.get('timestamp', datetime.utcnow()),
        'action_taken': data.get('action_taken')
    }
    db.violations.insert_one(violation_doc)
    return violation_doc


def list_violations(page=1, per_page=50, category=None):
    _, db = _get_db()
    query = {}
    if category:
        query['category'] = category
    total = db.violations.count_documents(query)
    cursor = db.violations.find(query).sort('timestamp', DESCENDING).skip((page - 1) * per_page).limit(per_page)
    return list(cursor), total


def list_violations_by_user(user_id):
    _, db = _get_db()
    return list(db.violations.find({'user_id': int(user_id)}).sort('timestamp', DESCENDING))


def count_violations(filter_query=None):
    _, db = _get_db()
    return db.violations.count_documents(filter_query or {})


def list_recent_violations(limit=10):
    _, db = _get_db()
    return list(db.violations.find({}).sort('timestamp', DESCENDING).limit(limit))


def get_violations_by_category():
    _, db = _get_db()
    pipeline = [{'$group': {'_id': '$category', 'count': {'$sum': 1}}}]
    return {doc['_id']: doc['count'] for doc in db.violations.aggregate(pipeline)}


def create_post(data):
    _, db = _get_db()
    post_doc = {
        'id': _get_next_sequence('posts'),
        'user_id': int(data['user_id']),
        'content': data['content'],
        'image_url': data.get('image_url'),
        'is_hate_speech': bool(data.get('is_hate_speech', False)),
        'confidence_score': float(data.get('confidence_score', 0.0)),
        'likes_count': int(data.get('likes_count', 0)),
        'created_at': data.get('created_at', datetime.utcnow())
    }
    db.posts.insert_one(post_doc)
    return post_doc


def get_post_by_id(post_id):
    _, db = _get_db()
    return db.posts.find_one({'id': int(post_id)})


def delete_post_by_id(post_id):
    _, db = _get_db()
    db.posts.delete_one({'id': int(post_id)})


def update_post(post_id, updates):
    _, db = _get_db()
    db.posts.update_one({'id': int(post_id)}, {'$set': updates})
    return get_post_by_id(post_id)


def list_posts(page=1, per_page=20, include_hate=False):
    _, db = _get_db()
    suspended_users = list(db.users.find({'is_suspended': True}, {'id': 1}))
    suspended_ids = [u['id'] for u in suspended_users]

    query = {'user_id': {'$nin': suspended_ids}}
    if not include_hate:
        query['is_hate_speech'] = False

    total = db.posts.count_documents(query)
    cursor = db.posts.find(query).sort('created_at', DESCENDING).skip((page - 1) * per_page).limit(per_page)
    return list(cursor), total


def list_posts_by_user(user_id):
    _, db = _get_db()
    return list(db.posts.find({'user_id': int(user_id)}).sort('created_at', DESCENDING))


def count_posts(filter_query=None):
    _, db = _get_db()
    return db.posts.count_documents(filter_query or {})


def to_user_dict(user_doc):
    violations_count = count_violations({'user_id': user_doc['id']}) if user_doc else 0
    return _user_to_dict(user_doc, violations_count=violations_count)


def to_violation_dict(violation_doc):
    user = get_user_by_id(violation_doc['user_id']) if violation_doc else None
    return _violation_to_dict(violation_doc, username=user['username'] if user else None)


def to_post_dict(post_doc):
    user = get_user_by_id(post_doc['user_id']) if post_doc else None
    return _post_to_dict(post_doc, username=user['username'] if user else None)
