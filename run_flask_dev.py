"""Run Flask development server with all endpoints"""
from backend.app import create_app

if __name__ == '__main__':
    app = create_app()
    print("\n" + "="*70)
    print("Backend API Server Starting (Flask Development Mode)...")
    print("="*70)
    print("API available at: http://localhost:5000")
    print("\nEndpoints:")
    print("   - POST /api/auth/register")
    print("   - POST /api/auth/login")
    print("   - POST /api/analyze")
    print("   - GET  /api/users")
    print("   - GET  /api/posts")
    print("   - POST /api/posts")
    print("   - GET  /api/violations")
    print("   - GET  /api/statistics")
    print("="*70 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
