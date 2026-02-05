"""
Add authentication endpoints to api.py
"""

auth_code = '''
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

'''

# Read the current api.py
with open('backend/routes/api.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the right place to insert (after imports and before first route)
lines = content.split('\n')
insert_index = 0

for i, line in enumerate(lines):
    if line.startswith('api_bp = Blueprint'):
        insert_index = i + 1
        break

# Insert auth endpoints
lines.insert(insert_index, auth_code)

# Write back
with open('backend/routes/api.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('✅ Authentication endpoints added to api.py')
