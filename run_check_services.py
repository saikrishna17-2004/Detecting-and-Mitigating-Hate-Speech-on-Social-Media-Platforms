import json
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

endpoints = {
    'backend_root': 'http://localhost:5000/',
    'backend_analyze': 'http://localhost:5000/api/analyze',
    'frontend_root': 'http://localhost:3000/'
}

results = {}

# Helper to POST JSON using urllib
import urllib.request
import urllib.error
import urllib.parse

def http_get(url, timeout=5):
    try:
        req = Request(url, headers={'User-Agent': 'health-checker'})
        with urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode('utf-8', errors='replace')
            return {'ok': True, 'status': resp.getcode(), 'body': body}
    except HTTPError as e:
        return {'ok': False, 'status': e.code, 'error': str(e)}
    except URLError as e:
        return {'ok': False, 'error': str(e)}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def http_post_json(url, payload, timeout=5):
    try:
        data = json.dumps(payload).encode('utf-8')
        req = Request(url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'health-checker'})
        with urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode('utf-8', errors='replace')
            return {'ok': True, 'status': resp.getcode(), 'body': body}
    except HTTPError as e:
        try:
            err_body = e.read().decode('utf-8', errors='replace')
        except:
            err_body = ''
        return {'ok': False, 'status': e.code, 'error': str(e), 'body': err_body}
    except URLError as e:
        return {'ok': False, 'error': str(e)}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


print('Checking services...')

# Backend root
results['backend_root'] = http_get(endpoints['backend_root'])

# Analyze (POST)
results['backend_analyze'] = http_post_json(endpoints['backend_analyze'], {'text': 'health check test'})

# Frontend root
results['frontend_root'] = http_get(endpoints['frontend_root'])

print('\nResults:')
print(json.dumps(results, indent=2))

# Exit code: 0 if backend_root ok and analyze ok, else 2
ok = results['backend_root'].get('ok') and results['backend_analyze'].get('ok')
if ok:
    print('\nAll core backend checks passed.')
    sys.exit(0)
else:
    print('\nOne or more checks failed.')
    sys.exit(2)
