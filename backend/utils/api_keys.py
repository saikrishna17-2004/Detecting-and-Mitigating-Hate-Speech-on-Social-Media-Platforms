"""
API Key Management for SaaS Model
Handles API key generation, validation, and usage tracking
"""
import secrets
import hashlib
from datetime import datetime
from backend.database import db

# API Tier limits (calls per month)
TIER_LIMITS = {
    'free': 1000,
    'pro': 50000,
    'enterprise': float('inf')  # Unlimited
}

def generate_api_key():
    """Generate a secure API key"""
    return secrets.token_urlsafe(32)

def hash_api_key(api_key):
    """Hash API key for secure storage"""
    return hashlib.sha256(api_key.encode()).hexdigest()

def create_api_key(user_id, tier='free'):
    """
    Create a new API key for a user
    
    Args:
        user_id: User ID
        tier: 'free', 'pro', or 'enterprise'
    
    Returns:
        dict: API key information (includes unhashed key - show once!)
    """
    api_key = generate_api_key()
    hashed_key = hash_api_key(api_key)
    
    key_doc = {
        'hashed_key': hashed_key,
        'user_id': user_id,
        'tier': tier,
        'calls_used': 0,
        'calls_limit': TIER_LIMITS.get(tier, 1000),
        'created_at': datetime.utcnow(),
        'is_active': True,
        'last_used': None
    }
    
    result = db.api_keys.insert_one(key_doc)
    
    return {
        'api_key': api_key,  # Return unhashed - show to user once!
        'key_id': str(result.inserted_id),
        'tier': tier,
        'calls_limit': key_doc['calls_limit']
    }

def validate_api_key(api_key):
    """
    Validate API key and check usage limits
    
    Returns:
        tuple: (is_valid: bool, key_doc: dict or None, error_message: str or None)
    """
    if not api_key:
        return False, None, 'API key required'
    
    hashed_key = hash_api_key(api_key)
    key_doc = db.api_keys.find_one({'hashed_key': hashed_key})
    
    if not key_doc:
        return False, None, 'Invalid API key'
    
    if not key_doc.get('is_active', True):
        return False, None, 'API key is inactive'
    
    # Check usage limit
    calls_used = key_doc.get('calls_used', 0)
    calls_limit = key_doc.get('calls_limit', TIER_LIMITS['free'])
    
    if calls_used >= calls_limit:
        return False, None, f'API usage limit exceeded ({calls_limit} calls/month)'
    
    return True, key_doc, None

def track_api_call(api_key):
    """
    Track an API call (increment counter)
    """
    hashed_key = hash_api_key(api_key)
    
    db.api_keys.update_one(
        {'hashed_key': hashed_key},
        {
            '$inc': {'calls_used': 1},
            '$set': {'last_used': datetime.utcnow()}
        }
    )

def get_api_usage(api_key):
    """
    Get usage statistics for an API key
    
    Returns:
        dict: Usage statistics
    """
    hashed_key = hash_api_key(api_key)
    key_doc = db.api_keys.find_one({'hashed_key': hashed_key})
    
    if not key_doc:
        return None
    
    return {
        'tier': key_doc.get('tier'),
        'calls_used': key_doc.get('calls_used', 0),
        'calls_limit': key_doc.get('calls_limit'),
        'calls_remaining': key_doc.get('calls_limit', 0) - key_doc.get('calls_used', 0),
        'created_at': key_doc.get('created_at'),
        'last_used': key_doc.get('last_used')
    }

def reset_monthly_usage():
    """
    Reset monthly usage counters (run via cron job monthly)
    """
    result = db.api_keys.update_many(
        {},
        {'$set': {'calls_used': 0}}
    )
    
    return result.modified_count

def deactivate_api_key(api_key):
    """Deactivate an API key"""
    hashed_key = hash_api_key(api_key)
    
    result = db.api_keys.update_one(
        {'hashed_key': hashed_key},
        {'$set': {'is_active': False}}
    )
    
    return result.modified_count > 0

def list_user_api_keys(user_id):
    """List all API keys for a user (hashed)"""
    keys = db.api_keys.find({'user_id': user_id})
    
    return [{
        'tier': k.get('tier'),
        'calls_used': k.get('calls_used', 0),
        'calls_limit': k.get('calls_limit'),
        'created_at': k.get('created_at'),
        'last_used': k.get('last_used'),
        'is_active': k.get('is_active', True)
    } for k in keys]
