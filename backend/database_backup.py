from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User model for tracking social media users"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    warning_count = db.Column(db.Integer, default=0)
    is_suspended = db.Column(db.Boolean, default=False)
    suspended_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    violations = db.relationship('Violation', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'warning_count': self.warning_count,
            'is_suspended': self.is_suspended,
            'suspended_at': self.suspended_at.isoformat() if self.suspended_at else None,
            'created_at': self.created_at.isoformat(),
            'violations_count': len(self.violations)
        }

class Violation(db.Model):
    """Violation model for tracking hate speech incidents"""
    __tablename__ = 'violations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # racial, gender, religious, etc.
    confidence_score = db.Column(db.Float, nullable=False)
    language = db.Column(db.String(10), default='en')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    action_taken = db.Column(db.String(20))  # warning, suspension, none
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'content': self.content[:100] + '...' if len(self.content) > 100 else self.content,
            'category': self.category,
            'confidence_score': round(self.confidence_score, 3),
            'language': self.language,
            'timestamp': self.timestamp.isoformat(),
            'action_taken': self.action_taken
        }

class Post(db.Model):
    """Post model for storing analyzed content"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_hate_speech = db.Column(db.Boolean, default=False)
    confidence_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'is_hate_speech': self.is_hate_speech,
            'confidence_score': round(self.confidence_score, 3),
            'created_at': self.created_at.isoformat()
        }
