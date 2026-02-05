"""
Production server configuration for Render deployment
Uses gunicorn as WSGI server
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.app import create_app

# Create Flask app
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    
    print("\n" + "="*70)
    print("Backend API Server Starting")
    print("="*70)
    print(f"API available at: http://localhost:{port}")
    print("Endpoints:")
    print("   - POST /api/auth/register")
    print("   - POST /api/auth/login")
    print("   - POST /api/analyze")
    print("   - GET  /api/posts")
    print("   - GET  /api/users")
    print("   - GET  /api/violations")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
