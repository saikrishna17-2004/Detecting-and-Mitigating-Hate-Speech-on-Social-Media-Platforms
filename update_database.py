"""
Update database.py to add password field and authentication methods
"""

with open('backend/database.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add werkzeug import at the top
if 'from werkzeug.security' not in content:
    content = content.replace(
        'from datetime import datetime\nfrom flask_sqlalchemy import SQLAlchemy',
        'from datetime import datetime\nfrom flask_sqlalchemy import SQLAlchemy\nfrom werkzeug.security import generate_password_hash, check_password_hash'
    )

# Add password_hash field
if 'password_hash' not in content:
    content = content.replace(
        "email = db.Column(db.String(120), unique=True, nullable=False)",
        "email = db.Column(db.String(120), unique=True, nullable=False)\n    password_hash = db.Column(db.String(255), nullable=True)  # Nullable for existing users"
    )

# Add set_password method
if 'def set_password' not in content:
    content = content.replace(
        "# Relationship\n    violations = db.relationship('Violation', backref='user', lazy=True, cascade='all, delete-orphan')",
        '''# Relationship
    violations = db.relationship('Violation', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if password matches"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)'''
    )

# Write back
with open('backend/database.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('✅ database.py updated with password field and auth methods')
