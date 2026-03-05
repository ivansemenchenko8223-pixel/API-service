python -m venv venv
venv/scripts/active
.\venv\Scripts\Activate.ps1

arkdown
netstat -ano | findstr :8000
taskkill /PID 23408 /F