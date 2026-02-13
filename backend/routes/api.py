from flask import Blueprint, request, jsonify
from backend.database import (
    create_user,
    create_user_with_id,
    get_user_by_username,
    get_user_by_email,
    get_user_by_id,
    list_users,
    to_user_dict,
    check_password,
    update_user,
    increment_user_warning,
    create_violation,
    list_violations,
    list_violations_by_user,
    count_violations,
    list_recent_violations,
    get_violations_by_category,
    count_users,
    count_suspended_users,
    count_posts,
    list_posts,
    create_post as create_post_doc,
    get_post_by_id,
    update_post,
    delete_post_by_id,
    list_posts_by_user,
    to_violation_dict,
    to_post_dict
)
from backend.models.detector import detector
from backend.utils.email_service import email_service
from backend.utils.api_keys import (
    create_api_key,
    validate_api_key,
    track_api_call,
    get_api_usage,
    list_user_api_keys
)
from datetime import datetime
import os
from functools import wraps

api_bp = Blueprint('api', __name__)

# API Key authentication decorator (optional - for external API access)
def require_api_key_optional(f):
    """Optional API key check - tracks usage if key provided"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if api_key:
            # Validate and track if API key provided
            is_valid, key_doc, error = validate_api_key(api_key)
            if not is_valid:
                return jsonify({'error': error}), 401
            
            # Track API call
            track_api_call(api_key)
            
            # Add key info to request context
            request.api_key_tier = key_doc.get('tier')
        else:
            # No API key - allow for internal/frontend use
            request.api_key_tier = None
        
        return f(*args, **kwargs)
    return decorated_function

# Authentication endpoints
@api_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not all([username, email, password]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Check if username already exists
        if get_user_by_username(username):
            return jsonify({'error': 'Username already exists'}), 400
        
        # Check if email already exists
        if get_user_by_email(email):
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = create_user(username=username, email=email, password=password)
        
        return jsonify({'success': True, 'user': to_user_dict(user)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not all([username, password]):
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Find user
        user = get_user_by_username(username)
        
        if not user or not check_password(user, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check if suspended
        if user.get('is_suspended'):
            return jsonify({'error': 'Account is suspended'}), 403
        
        return jsonify({'success': True, 'user': to_user_dict(user)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/auth/logout', methods=['POST'])
def logout():
    """Logout user"""
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200



# Configuration
MAX_WARNINGS = 3
# Minimum confidence required to block a post automatically (0.0-1.0)
# Read from environment so it can be tuned without code changes
try:
    BLOCK_CONFIDENCE = float(os.environ.get('BLOCK_CONFIDENCE', '0.8'))
except Exception:
    BLOCK_CONFIDENCE = 0.8

@api_bp.route('/analyze', methods=['POST'])
@require_api_key_optional
def analyze_text():
    """
    Analyze text for hate speech with multi-language support
    
    Headers:
        X-API-Key: Optional API key for external access
    
    Body:
        {
            "text": "Text to analyze",
            "user_id": "optional_user_id",
            "username": "optional_username"
        }
    
    Response:
        {
            "success": true,
            "result": {
                "is_hate_speech": false,
                "confidence": 0.95,
                "category": "none",
                "language": "en",
                "translated": false
            },
            "action_taken": "none",
            "api_tier": "free"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text']
        user_id = data.get('user_id')
        username = data.get('username', f'user_{user_id}')
        
        # Analyze text (now with multi-language support)
        result = detector.analyze(text)
        
        # Get or create user
        user = None
        if user_id:
            user = get_user_by_id(user_id)
            if not user:
                user = create_user_with_id(
                    user_id=user_id,
                    username=username,
                    email=f"{username}@example.com"
                )
        
        # Analysis endpoint should be side-effect free: do not modify DB.
        # Only suggest an action based on detection. We consider a 'block' action
        # only when the detector reports hate speech with high confidence.
        if result['is_hate_speech'] and result['confidence'] >= BLOCK_CONFIDENCE:
            action_taken = 'block'
        elif result['is_hate_speech']:
            action_taken = 'warning'
        else:
            action_taken = 'none'
        
        return jsonify({
            'success': True,
            'result': result,
            'action_taken': action_taken,
            'user_status': to_user_dict(user) if user else None,
            'message': get_action_message(action_taken, user.get('warning_count', 0) if user else 0),
            'api_tier': request.api_key_tier  # Show which tier was used
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = list_users()
        return jsonify({
            'success': True,
            'users': [to_user_dict(user) for user in users],
            'total': len(users)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details"""
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        violations = list_violations_by_user(user_id)
        
        return jsonify({
            'success': True,
            'user': to_user_dict(user),
            'violations': [to_violation_dict(v) for v in violations]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/<int:user_id>/warn', methods=['POST'])
def warn_user(user_id):
    """Manually warn a user"""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'Community guidelines violation')
        content = data.get('content', 'Manual warning by administrator')

        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user = increment_user_warning(user_id, 1)

        # Check for suspension
        should_suspend = user.get('warning_count', 0) >= MAX_WARNINGS
        
        if should_suspend:
            user = update_user(user_id, {
                'is_suspended': True,
                'suspended_at': datetime.utcnow()
            })

        # Send email notification
        if should_suspend:
            email_service.send_suspension_email(
                user_email=user.get('email'),
                username=user.get('username'),
                violation_count=user.get('warning_count', 0),
                final_violation_content=content,
                category=reason
            )
        else:
            email_service.send_warning_email(
                user_email=user.get('email'),
                username=user.get('username'),
                warning_count=user.get('warning_count', 0),
                max_warnings=MAX_WARNINGS,
                violation_content=content,
                category=reason
            )

        return jsonify({
            'success': True,
            'user': to_user_dict(user),
            'message': f"User {user.get('username')} has been warned. Email notification sent.",
            'suspended': should_suspend
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/<int:user_id>/suspend', methods=['POST'])
def suspend_user(user_id):
    """Manually suspend a user"""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'Community guidelines violation')
        content = data.get('content', 'Manual suspension by administrator')

        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user = update_user(user_id, {
            'is_suspended': True,
            'suspended_at': datetime.utcnow()
        })

        # Get violation count
        violation_count = count_violations({'user_id': int(user_id)})
        if violation_count == 0:
            violation_count = user.get('warning_count', 0)
        
        # Send suspension email
        email_service.send_suspension_email(
            user_email=user.get('email'),
            username=user.get('username'),
            violation_count=violation_count,
            final_violation_content=content,
            category=reason
        )
        
        return jsonify({
            'success': True,
            'user': to_user_dict(user),
            'message': f"User {user.get('username')} has been suspended. Email notification sent."
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/<int:user_id>/unsuspend', methods=['POST'])
def unsuspend_user(user_id):
    """Unsuspend a user"""
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        user = update_user(user_id, {
            'is_suspended': False,
            'suspended_at': None,
            'warning_count': 0
        })
        
        return jsonify({
            'success': True,
            'user': to_user_dict(user),
            'message': f"User {user.get('username')} has been unsuspended"
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/violations', methods=['GET'])
def get_violations():
    """Get all violations"""
    try:
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        category = request.args.get('category', None)

        violations, total = list_violations(page=page, per_page=per_page, category=category)
        pages = (total + per_page - 1) // per_page

        return jsonify({
            'success': True,
            'violations': [to_violation_dict(v) for v in violations],
            'total': total,
            'page': page,
            'pages': pages
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get platform statistics"""
    try:
        total_users = count_users()
        suspended_users = count_suspended_users()
        total_violations = count_violations()
        total_posts = count_posts()
        hate_speech_posts = count_posts({'is_hate_speech': True})

        # Violations by category
        violations_by_category = get_violations_by_category()

        # Recent violations
        recent_violations = list_recent_violations(limit=10)
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_users': total_users,
                'suspended_users': suspended_users,
                'active_users': total_users - suspended_users,
                'total_violations': total_violations,
                'total_posts': total_posts,
                'hate_speech_posts': hate_speech_posts,
                'clean_posts': total_posts - hate_speech_posts,
                'hate_speech_percentage': round((hate_speech_posts / total_posts * 100) if total_posts > 0 else 0, 2)
            },
            'violations_by_category': violations_by_category,
            'recent_violations': [to_violation_dict(v) for v in recent_violations]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin: Reload lexicon without restarting the server
@api_bp.route('/admin/lexicon/reload', methods=['POST'])
def reload_lexicon():
    """Reload offensive lexicon from data/hate_keywords.txt (or provided path)."""
    try:
        data = request.get_json(silent=True) or {}
        path = data.get('path', 'data/hate_keywords.txt')

        detector.load_offensive_lexicon(path)

        return jsonify({
            'success': True,
            'path': path,
            'words_count': len(detector.offensive_keywords),
            'phrases_count': len(detector.offensive_phrases)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Posts endpoints
@api_bp.route('/posts', methods=['GET'])
def get_posts():
    """Get all posts (feed)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 20

        posts, total = list_posts(page=page, per_page=per_page, include_hate=False)
        pages = (total + per_page - 1) // per_page

        return jsonify({
            'success': True,
            'posts': [to_post_dict(post) for post in posts],
            'total': total,
            'page': page,
            'pages': pages
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admin: Lexicon utilities
@api_bp.route('/admin/lexicon/stats', methods=['GET'])
def get_lexicon_stats():
    """Return current lexicon stats and default path."""
    try:
        return jsonify({
            'success': True,
            'path': 'data/hate_keywords.txt',
            'words_count': len(detector.offensive_keywords),
            'phrases_count': len(detector.offensive_phrases)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/admin/lexicon/update', methods=['POST'])
def update_lexicon():
    """Append or replace lexicon content and reload.
    Body JSON: { content: string, mode: 'append'|'replace', path?: string }
    """
    try:
        data = request.get_json() or {}
        content = (data.get('content') or '').strip()
        mode = (data.get('mode') or 'append').lower()
        path = data.get('path', 'data/hate_keywords.txt')

        if not content:
            return jsonify({'error': 'content is required'}), 400
        if mode not in ('append', 'replace'):
            return jsonify({'error': "mode must be 'append' or 'replace'"}), 400

        # Ensure directory exists
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if mode == 'replace' and os.path.exists(path):
            # Backup existing
            import shutil
            shutil.copy2(path, path + '.bak')

        # Normalize newlines
        normalized = '\n'.join([line.strip() for line in content.splitlines() if line.strip()]) + '\n'

        if mode == 'append' and os.path.exists(path):
            with open(path, 'a', encoding='utf-8') as f:
                f.write(normalized)
        else:
            with open(path, 'w', encoding='utf-8') as f:
                # Keep a brief header for guidance
                f.write('# Hate/offensive keywords and phrases\n')
                f.write('# One per line; lines starting with # are comments\n')
                f.write(normalized)

        # Reload
        detector.load_offensive_lexicon(path)

        return jsonify({
            'success': True,
            'path': path,
            'mode': mode,
            'words_count': len(detector.offensive_keywords),
            'phrases_count': len(detector.offensive_phrases)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/posts', methods=['POST'])
def create_post():
    """Create a new post"""
    try:
        data = request.get_json()
        content = data.get('content')
        user_id = data.get('user_id')
        image_url = data.get('image_url')
        
        if not content or not user_id:
            return jsonify({'error': 'Content and user_id are required'}), 400
        
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if user is suspended
        if user.get('is_suspended'):
            return jsonify({'error': 'Your account is suspended'}), 403
        
        # Analyze content for hate speech
        analysis = detector.analyze(content)
        
        # Only block posts that are high-confidence hate speech. Lower-confidence
        # detections are treated as warnings: the post is created but the analysis
        # is returned for the UI to display (and moderators can take action).
        if analysis['is_hate_speech'] and analysis['confidence'] >= BLOCK_CONFIDENCE:
            user = increment_user_warning(user_id, 1)

            # Check for suspension
            should_suspend = user.get('warning_count', 0) >= MAX_WARNINGS and not user.get('is_suspended')
            action_taken = 'suspension' if should_suspend else 'warning'

            if should_suspend:
                user = update_user(user_id, {
                    'is_suspended': True,
                    'suspended_at': datetime.utcnow()
                })

            create_violation({
                'user_id': user_id,
                'content': content,
                'category': analysis['category'],
                'confidence_score': analysis['confidence'],
                'language': analysis['language'],
                'action_taken': action_taken
            })

            # Send email notification
            if should_suspend:
                email_service.send_suspension_email(
                    user_email=user.get('email'),
                    username=user.get('username'),
                    violation_count=user.get('warning_count', 0),
                    final_violation_content=content,
                    category=analysis['category']
                )
            else:
                email_service.send_warning_email(
                    user_email=user.get('email'),
                    username=user.get('username'),
                    warning_count=user.get('warning_count', 0),
                    max_warnings=MAX_WARNINGS,
                    violation_content=content,
                    category=analysis['category']
                )

            return jsonify({
                'success': False,
                'error': 'Post contains high-confidence hate speech and was blocked',
                'analysis': analysis,
                'user_status': to_user_dict(user),
                'email_sent': True
            }), 400

        # Create post (clean content only)
        post = create_post_doc({
            'user_id': user_id,
            'content': content,
            'image_url': image_url,
            'is_hate_speech': False,
            'confidence_score': analysis['confidence']
        })
        
        return jsonify({
            'success': True,
            'post': to_post_dict(post),
            'analysis': analysis,
            'user_status': to_user_dict(user)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post"""
    try:
        post = get_post_by_id(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404

        # Require the requesting user's id in the request body so we can
        # verify ownership. This project uses simple user_id passing from
        # the frontend (no token/session middleware here).
        data = request.get_json(silent=True) or {}
        requesting_user_id = data.get('user_id')

        if not requesting_user_id:
            return jsonify({'error': 'user_id is required to delete a post'}), 400

        # Ensure only the owner can delete their post
        if post.get('user_id') != requesting_user_id:
            return jsonify({'error': 'You are not authorized to delete this post'}), 403

        delete_post_by_id(post_id)

        return jsonify({
            'success': True,
            'message': 'Post deleted successfully'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    """Like a post"""
    try:
        post = get_post_by_id(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        likes_count = int(post.get('likes_count', 0)) + 1
        post = update_post(post_id, {'likes_count': likes_count})
        
        return jsonify({
            'success': True,
            'likes_count': post.get('likes_count', likes_count)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/posts/<int:post_id>/unlike', methods=['POST'])
def unlike_post(post_id):
    """Unlike a post"""
    try:
        post = get_post_by_id(post_id)
        if not post:
            return jsonify({'error': 'Post not found'}), 404
        likes_count = max(0, int(post.get('likes_count', 0)) - 1)
        post = update_post(post_id, {'likes_count': likes_count})
        
        return jsonify({
            'success': True,
            'likes_count': post.get('likes_count', likes_count)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """Get posts by a specific user"""
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        posts = list_posts_by_user(user_id)
        
        return jsonify({
            'success': True,
            'user': to_user_dict(user),
            'posts': [to_post_dict(post) for post in posts]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Email service endpoints
@api_bp.route('/admin/email/test', methods=['POST'])
def test_email():
    """Test email configuration"""
    try:
        data = request.get_json() or {}
        recipient_email = data.get('email')
        
        if not recipient_email:
            return jsonify({'error': 'Email address is required'}), 400
        
        # Check if email service is configured
        if not email_service.enabled:
            return jsonify({
                'success': False,
                'message': 'Email service is not configured. Set SMTP credentials in .env file.',
                'configured': False
            }), 200
        
        # Send test email
        success = email_service.send_test_email(recipient_email)
        
        return jsonify({
            'success': success,
            'message': 'Test email sent successfully!' if success else 'Failed to send test email',
            'configured': True
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/admin/email/status', methods=['GET'])
def email_status():
    """Check email service configuration status"""
    try:
        return jsonify({
            'success': True,
            'configured': email_service.enabled,
            'smtp_server': email_service.smtp_server if email_service.enabled else 'Not configured',
            'sender_email': email_service.sender_email if email_service.enabled else 'Not configured'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_action_message(action, warning_count):
    """Get user-friendly message based on action taken"""
    if action == 'suspended':
        return f"⛔ Your account has been suspended due to repeated violations of community guidelines."
    elif action == 'warning':
        return f"⚠️ Warning {warning_count}/{MAX_WARNINGS}: Your content contains hate speech. Further violations will result in suspension."
    else:
        return "✅ Content is appropriate."

# =============================================================================
# API Key Management Endpoints (SaaS Features)
# =============================================================================

@api_bp.route('/api-keys/generate', methods=['POST'])
def generate_api_key():
    """
    Generate a new API key for a user
    
    Body:
        {
            "user_id": "user123",
            "tier": "free"  // free, pro, or enterprise
        }
    
    Response:
        {
            "success": true,
            "api_key": "xxx",  // Show once!
            "tier": "free",
            "calls_limit": 1000
        }
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        tier = data.get('tier', 'free')
        
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        if tier not in ['free', 'pro', 'enterprise']:
            return jsonify({'error': 'Invalid tier. Must be free, pro, or enterprise'}), 400
        
        # Create API key
        key_info = create_api_key(user_id, tier)
        
        return jsonify({
            'success': True,
            'api_key': key_info['api_key'],
            'tier': key_info['tier'],
            'calls_limit': key_info['calls_limit'],
            'message': '⚠️ Save this API key! It will not be shown again.'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api-keys/usage', methods=['GET'])
def check_api_usage():
    """
    Check API key usage statistics
    
    Headers:
        X-API-Key: Your API key
    
    Response:
        {
            "tier": "free",
            "calls_used": 45,
            "calls_limit": 1000,
            "calls_remaining": 955
        }
    """
    try:
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({'error': 'X-API-Key header required'}), 401
        
        usage = get_api_usage(api_key)
        
        if not usage:
            return jsonify({'error': 'Invalid API key'}), 401
        
        return jsonify({
            'success': True,
            **usage
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api-keys/list/<user_id>', methods=['GET'])
def list_api_keys(user_id):
    """
    List all API keys for a user
    
    Response:
        {
            "success": true,
            "api_keys": [...]
        }
    """
    try:
        keys = list_user_api_keys(user_id)
        
        return jsonify({
            'success': True,
            'api_keys': keys
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# =============================================================================
# Social Media Integration Endpoints (Webhook Support)
# =============================================================================

@api_bp.route('/webhook/analyze', methods=['POST'])
@require_api_key_optional
def webhook_analyze():
    """
    Webhook endpoint for external social media platforms
    
    Headers:
        X-API-Key: Your API key (required for webhooks)
        X-Callback-URL: Optional callback URL to POST results
    
    Body:
        {
            "text": "Content to analyze",
            "platform": "twitter",
            "post_id": "123456",
            "user_id": "user123"
        }
    
    Response:
        {
            "success": true,
            "result": {...},
            "should_block": true/false
        }
    """
    try:
        # Require API key for webhooks
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'error': 'API key required for webhook access'}), 401
        
        data = request.get_json()
        text = data.get('text')
        platform = data.get('platform', 'unknown')
        post_id = data.get('post_id')
        
        if not text:
            return jsonify({'error': 'text required'}), 400
        
        # Analyze
        result = detector.analyze(text)
        
        # Determine if should block
        should_block = result['is_hate_speech'] and result['confidence'] >= 0.8
        
        response = {
            'success': True,
            'result': result,
            'should_block': should_block,
            'platform': platform,
            'post_id': post_id,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Optional: Send callback
        callback_url = request.headers.get('X-Callback-URL')
        if callback_url:
            # TODO: Implement async callback posting
            pass
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
