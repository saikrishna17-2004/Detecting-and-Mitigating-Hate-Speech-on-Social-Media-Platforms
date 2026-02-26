import requests

base = 'http://localhost:5000/api/posts'

cases = [
    ("image_only", {"user_id": "test-user", "content": "", "image_url": "data:image/png;base64,abc123"}),
    ("empty", {"user_id": "test-user", "content": "", "image_url": None}),
]

for name, payload in cases:
    try:
        r = requests.post(base, json=payload, timeout=10)
        print(name, r.status_code, r.text)
    except Exception as e:
        print(name, "EXC", str(e))
