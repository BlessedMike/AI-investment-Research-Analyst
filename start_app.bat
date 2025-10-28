@echo off
echo ========================================
echo AI Investment Research Analyst
echo ========================================
echo.

echo Starting FastAPI Backend...
start "FastAPI Backend" cmd /k "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak > nul

echo Starting Next.js Frontend...
start "Next.js Frontend" cmd /k "cd ai-investment-research-analyst && npm run dev"

echo.
echo ========================================
echo Both servers are starting up!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause > nul
