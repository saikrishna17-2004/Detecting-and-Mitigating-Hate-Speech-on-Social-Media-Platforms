from flask import Blueprint, request, jsonify
from backend.database import db, User, Violation, Post
from backend.models.detector import detector
from backend.utils.email_service import email_service
from datetime import datetime
import os
from sqlalchemy import func

api_bp = Blueprint('api', __name__)

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
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'user': user.to_dict()}), 201
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
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check if suspended
        if user.is_suspended:
            return jsonify({'error': 'Account is suspended'}), 403
        
        return jsonify({'success': True, 'user': user.to_dict()}), 200
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
def analyze_text():
    """Analyze text for hate speech"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text']
        user_id = data.get('user_id')
        username = data.get('username', f'user_{user_id}')
        
        # Analyze text
        result = detector.analyze(text)
        
        # Get or create user
        user = None
        if user_id:
            user = User.query.filter_by(id=user_id).first()
            if not user:
                user = User(
                    id=user_id,
                    username=username,
                    email=f"{username}@example.com"
                )
                db.session.add(user)
                db.session.commit()
        
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
            'user_status': user.to_dict() if user else None,
            'message': get_action_message(action_taken, user.warning_count if user else 0)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    try:
        users = User.query.all()
        return jsonify({
            'success': True,
            'users': [user.to_dict() for user in users],
            'total': len(users)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user details"""
    try:
        user = User.query.get_or_404(user_id)
        violations = Violation.query.filter_by(user_id=user_id).order_by(Violation.timestamp.desc()).all()
        
        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'violations': [v.to_dict() for v in violations]
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
        
        user = User.query.get_or_404(user_id)
        user.warning_count += 1

        # Check for suspension
        should_suspend = user.warning_count >= MAX_WARNINGS
        
        if should_suspend:
            user.is_suspended = True
            user.suspended_at = datetime.utcnow()

        db.session.commit()

        # Send email notification
        if should_suspend:
            email_service.send_suspension_email(
                user_email=user.email,
                username=user.username,
                violation_count=user.warning_count,
                final_violation_content=content,
                category=reason
            )
        else:
            email_service.send_warning_email(
                user_email=user.email,
                username=user.username,
                warning_count=user.warning_count,
                max_warnings=MAX_WARNINGS,
                violation_content=content,
                category=reason
            )

        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'message': f'User {user.username} has been warned. Email notification sent.',
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
        
        user = User.query.get_or_404(user_id)
        user.is_suspended = True
        user.suspended_at = datetime.utcnow()
        
        # Get violation count
        violation_count = Violation.query.filter_by(user_id=user_id).count()
        if violation_count == 0:
            violation_count = user.warning_count
        
        db.session.commit()
        
        # Send suspension email
        email_service.send_suspension_email(
            user_email=user.email,
            username=user.username,
            violation_count=violation_count,
            final_violation_content=content,
            category=reason
        )
        
        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'message': f'User {user.username} has been suspended. Email notification sent.'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/<int:user_id>/unsuspend', methods=['POST'])
def unsuspend_user(user_id):
    """Unsuspend a user"""
    try:
        user = User.query.get_or_404(user_id)
        user.is_suspended = False
        user.suspended_at = None
        user.warning_count = 0
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'message': f'User {user.username} has been unsuspended'
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
        
        query = Violation.query
        
        if category:
            query = query.filter_by(category=category)
        
        violations = query.order_by(Violation.timestamp.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'violations': [v.to_dict() for v in violations.items],
            'total': violations.total,
            'page': page,
            'pages': violations.pages
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get platform statistics"""
    try:
        total_users = User.query.count()
        suspended_users = User.query.filter_by(is_suspended=True).count()
        total_violations = Violation.query.count()
        total_posts = Post.query.count()
        hate_speech_posts = Post.query.filter_by(is_hate_speech=True).count()
        
        # Violations by category
        violations_by_category = db.session.query(
            Violation.category,
            func.count(Violation.id)
        ).group_by(Violation.category).all()
        
        # Recent violations
        recent_violations = Violation.query.order_by(
            Violation.timestamp.desc()
        ).limit(10).all()
        
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
            'violations_by_category': dict(violations_by_category),
            'recent_violations': [v.to_dict() for v in recent_violations]
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
        
        # Join with User table to filter out posts from suspended users
        posts = Post.query.join(User).filter(
            Post.is_hate_speech == False,
            User.is_suspended == False
        ).order_by(
            Post.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'posts': [post.to_dict() for post in posts.items],
            'total': posts.total,
            'page': page,
            'pages': posts.pages
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
        
        user = User.query.get_or_404(user_id)
        
        # Check if user is suspended
        if user.is_suspended:
            return jsonify({'error': 'Your account is suspended'}), 403
        
        # Analyze content for hate speech
        analysis = detector.analyze(content)
        
        # Only block posts that are high-confidence hate speech. Lower-confidence
        # detections are treated as warnings: the post is created but the analysis
        # is returned for the UI to display (and moderators can take action).
        if analysis['is_hate_speech'] and analysis['confidence'] >= BLOCK_CONFIDENCE:
            violation = Violation(
                user_id=user_id,
                content=content,
                category=analysis['category'],
                confidence_score=analysis['confidence'],
                language=analysis['language'],
                action_taken='warning'
            )
            db.session.add(violation)

            user.warning_count += 1

            # Check for suspension
            should_suspend = user.warning_count >= MAX_WARNINGS and not user.is_suspended

            if should_suspend:
                user.is_suspended = True
                user.suspended_at = datetime.utcnow()
                violation.action_taken = 'suspension'

            db.session.commit()

            # Send email notification
            if should_suspend:
                email_service.send_suspension_email(
                    user_email=user.email,
                    username=user.username,
                    violation_count=user.warning_count,
                    final_violation_content=content,
                    category=analysis['category']
                )
            else:
                email_service.send_warning_email(
                    user_email=user.email,
                    username=user.username,
                    warning_count=user.warning_count,
                    max_warnings=MAX_WARNINGS,
                    violation_content=content,
                    category=analysis['category']
                )

            return jsonify({
                'success': False,
                'error': 'Post contains high-confidence hate speech and was blocked',
                'analysis': analysis,
                'user_status': user.to_dict(),
                'email_sent': True
            }), 400

        # Create post (clean content only)
        post = Post(
            user_id=user_id,
            content=content,
            image_url=image_url,
            is_hate_speech=False,
            confidence_score=analysis['confidence']
        )
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'post': post.to_dict(),
            'analysis': analysis,
            'user_status': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post"""
    try:
        post = Post.query.get_or_404(post_id)

        # Require the requesting user's id in the request body so we can
        # verify ownership. This project uses simple user_id passing from
        # the frontend (no token/session middleware here).
        data = request.get_json(silent=True) or {}
        requesting_user_id = data.get('user_id')

        if not requesting_user_id:
            return jsonify({'error': 'user_id is required to delete a post'}), 400

        # Ensure only the owner can delete their post
        if post.user_id != requesting_user_id:
            return jsonify({'error': 'You are not authorized to delete this post'}), 403

        db.session.delete(post)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Post deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    """Like a post"""
    try:
        post = Post.query.get_or_404(post_id)
        post.likes_count += 1
        db.session.commit()
        
        return jsonify({
            'success': True,
            'likes_count': post.likes_count
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/posts/<int:post_id>/unlike', methods=['POST'])
def unlike_post(post_id):
    """Unlike a post"""
    try:
        post = Post.query.get_or_404(post_id)
        if post.likes_count > 0:
            post.likes_count -= 1
        db.session.commit()
        
        return jsonify({
            'success': True,
            'likes_count': post.likes_count
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/users/<int:user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """Get posts by a specific user"""
    try:
        user = User.query.get_or_404(user_id)
        posts = Post.query.filter_by(user_id=user_id).order_by(
            Post.created_at.desc()
        ).all()
        
        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'posts': [post.to_dict() for post in posts]
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
