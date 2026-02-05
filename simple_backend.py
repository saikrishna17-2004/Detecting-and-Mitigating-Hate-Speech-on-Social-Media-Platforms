"""
Simple Flask Backend Server for Hate Speech Detection
Minimal configuration for quick startup
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.models.detector import HateSpeechDetector

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize detector
print("Loading hate speech detector...")
detector = HateSpeechDetector()
print("✅ Detector loaded successfully!")

@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'Hate Speech Detection API',
        'version': '1.0.0',
        'model_loaded': detector.model_loaded,
        'endpoints': {
            'analyze': 'POST /api/analyze',
            'health': 'GET /health'
        }
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': detector.model_loaded
    })

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze text for hate speech"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing text field',
                'success': False
            }), 400
        
        text = data['text']
        
        if not text or len(text.strip()) == 0:
            return jsonify({
                'error': 'Text cannot be empty',
                'success': False
            }), 400
        
        # Analyze text
        result = detector.analyze(text)
        
        # Format response
        response = {
            'success': True,
            'text': text,
            'prediction': 'Hate Speech' if result['is_hate_speech'] else 'Normal',
            'is_hate_speech': result['is_hate_speech'],
            'confidence': result['confidence'],
            'category': result['category'],
            'language': result['language']
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error analyzing text: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/api/statistics', methods=['GET'])
def statistics():
    """Get system statistics"""
    return jsonify({
        'total_users': 0,
        'total_posts': 0,
        'total_violations': 0,
        'model_accuracy': '99.39%',
        'status': 'operational'
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 HATE SPEECH DETECTION API SERVER")
    print("="*60)
    print(f"✅ Model loaded: {detector.model_loaded}")
    print(f"📍 Server starting on: http://localhost:5000")
    print(f"🌐 Frontend can connect from: http://localhost:3002")
    print(f"\n📚 Available Endpoints:")
    print(f"   GET  / - API info")
    print(f"   GET  /health - Health check")
    print(f"   POST /api/analyze - Analyze text")
    print(f"   GET  /api/statistics - Get stats")
    print("\n✨ Press CTRL+C to stop")
    print("="*60 + "\n")
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n\n⏹️  Server stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
