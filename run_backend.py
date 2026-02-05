"""
Deprecated direct launcher.

Use start_server.bat to run the backend in a separate PowerShell window
so the process persists outside VS Code terminals and avoids encoding
issues. If you really want to run directly from this script, set the
environment variable RUN_BACKEND_DIRECT=1 before invocation.
"""

import os
import sys

if __name__ == '__main__':
    if not os.environ.get('RUN_BACKEND_DIRECT'):
        print("\nNOTE: This launcher is deprecated.")
        print("Please run the backend using start_server.bat instead:")
        print("  C:\\Users\\nakka\\Desktop\\pp1\\start_server.bat\n")
        sys.exit(1)

    # Direct mode (advanced): run the full Flask app with all routes
    from backend.app import create_app

    app = create_app()
    print("\nBackend API Server Starting (Flask Development)...")
    print("API available at: http://localhost:5000")
    print("Endpoints:")
    print("   - POST /api/auth/register")
    print("   - POST /api/auth/login")
    print("   - POST /api/analyze")
    print("   - GET  /api/users")
    print("   - GET  /api/posts")
    print("   - GET  /api/violations")
    print("   - GET  /api/statistics\n")
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
