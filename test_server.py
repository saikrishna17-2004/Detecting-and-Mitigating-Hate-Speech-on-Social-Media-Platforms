"""
Simple test to see if Flask works
"""
from flask import Flask, jsonify
from flask_cors import CORS
import requests

# The URL of the file you want to download
url = 'https://example.com/path/to/your/file.zip'
# The local filename to save it as
local_filename = 'downloaded_file.zip'

print(f"Attempting to download {url}...")

try:
    # Make the web request
    with requests.get(url, stream=True) as r:
        r.raise_for_status() # This will raise an error for bad responses (4xx or 5xx)
        
        # Open the local file in binary write mode
        with open(local_filename, 'wb') as f:
            # Write the content in chunks
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
                
    print(f"✅ Successfully downloaded and saved to {local_filename}")

except requests.exceptions.RequestException as e:
    print(f"❌ Error downloading file: {e}")
import requests

# The URL of the file you want to download
url = 'https://example.com/path/to/your/file.zip'
# The local filename to save it as
local_filename = 'downloaded_file.zip'

print(f"Attempting to download {url}...")

try:
    # Make the web request
    with requests.get(url, stream=True) as r:
        r.raise_for_status() # This will raise an error for bad responses (4xx or 5xx)
        
        # Open the local file in binary write mode
        with open(local_filename, 'wb') as f:
            # Write the content in chunks
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
                
    print(f"✅ Successfully downloaded and saved to {local_filename}")

except requests.exceptions.RequestException as e:
    print(f"❌ Error downloading file: {e}")
import requests

# The URL of the file you want to download
url = 'https://example.com/path/to/your/file.zip'
# The local filename to save it as
local_filename = 'downloaded_file.zip'

print(f"Attempting to download {url}...")

try:
    # Make the web request
    with requests.get(url, stream=True) as r:
        r.raise_for_status() # This will raise an error for bad responses (4xx or 5xx)
        
        # Open the local file in binary write mode
        with open(local_filename, 'wb') as f:
            # Write the content in chunks
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
                
    print(f"✅ Successfully downloaded and saved to {local_filename}")

except requests.exceptions.RequestException as e:
    print(f"❌ Error downloading file: {e}")
import requests

# The URL of the file you want to download
url = 'https://example.com/path/to/your/file.zip'
# The local filename to save it as
local_filename = 'downloaded_file.zip'

print(f"Attempting to download {url}...")

try:
    # Make the web request
    with requests.get(url, stream=True) as r:
        r.raise_for_status() # This will raise an error for bad responses (4xx or 5xx)
        
        # Open the local file in binary write mode
        with open(local_filename, 'wb') as f:
            # Write the content in chunks
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
                
    print(f"✅ Successfully downloaded and saved to {local_filename}")

except requests.exceptions.RequestException as e:
    print(f"❌ Error downloading file: {e}")
from waitress import serve

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({'message': 'Server is working!'})

@app.route('/test')
def test():
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    print("Starting test server on port 5001...")
    # app.run() is for development and shows a warning.
    # Using a production WSGI server like waitress avoids this.
    serve(app, host="127.0.0.1", port=5001)
