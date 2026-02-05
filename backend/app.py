from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.database import init_db
from backend.routes.api import api_bp

# Load environment variables
load_dotenv()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    # Use instance/ DB by default to align with migrations and persistent storage
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///instance/hate_speech_detection.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    
    # Initialize extensions
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Initialize MongoDB (indexes, counters)
    init_db()
    print("Database initialized successfully!")
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Hate Speech Detection API',
            'version': '1.0.0',
            'endpoints': {
                'analyze': '/api/analyze',
                'users': '/api/users',
                'violations': '/api/violations',
                'statistics': '/api/statistics'
            }
        })
    
    return app

if __name__ == '__main__':
    import sys
    
    app = create_app()
    print("\n🚀 Backend API Server Starting...")
    print("📍 API available at: http://localhost:5000")
    print("📚 Endpoints:")
    print("   - POST /api/analyze - Analyze text for hate speech")
    print("   - GET  /api/users - Get all users")
    print("   - GET  /api/violations - Get all violations")
    print("   - GET  /api/statistics - Get platform statistics\n")
    
    # Test that app works
    with app.test_client() as client:
        resp = client.get('/')
        print(f"✅ App test successful: {resp.status_code}")
    
    print("✅ Server is ready! Press CTRL+C to stop.\n")
    print("🎯 Starting Flask development server...")
    sys.stdout.flush()
    
    try:
        # Use Flask's built-in server with threaded mode
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True, use_reloader=False)
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"\n❌ ERROR starting server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
