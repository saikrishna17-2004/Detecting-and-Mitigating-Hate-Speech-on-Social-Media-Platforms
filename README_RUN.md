Run & development notes

Quick start (Windows PowerShell)

1) Create & activate Python virtualenv

```powershell
cd C:\Users\nakka\Desktop\pp1
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

2) (Optional) install frontend deps

```powershell
cd frontend-react
npm install
cd ..
```

3) Initialize DB (if needed)

```powershell
# Either run provided helper or rely on app to auto-create tables
python migrate_database.py
# or
python update_database.py
```

4) Start backend (recommended)

```powershell
# In a new PowerShell window (keeps server visible):
start .\start_server.bat
# Or run in current terminal for logs:
. .\.venv\Scripts\Activate.ps1
$env:RUN_BACKEND_DIRECT='1'
python run_backend.py
```

5) Start frontend

```powershell
cd frontend-react
npm start
```

6) Useful admin endpoints

- Reload lexicon (after editing `data/hate_keywords.txt`):

```powershell
Invoke-RestMethod -Method Post -Uri 'http://localhost:5000/api/admin/lexicon/reload' -ContentType 'application/json' -Body '{}'
```

- Analyze text:

```powershell
$body = @{ text = 'sample' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri 'http://localhost:5000/api/analyze' -ContentType 'application/json' -Body $body
```

Troubleshooting

- If `/api/auth/register` returns 404: you are likely running `server.py` (minimal server). Start the full app via `start_server.bat` or set `$env:RUN_BACKEND_DIRECT='1'; python run_backend.py`.
- If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Notes

- The backend uses SQLite at `instance/hate_speech_detection.db` (auto-created).
- Large lexicons may slow rule-based detection. Consider using ML models for scale.
