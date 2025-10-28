Write-Host "========================================" -ForegroundColor Cyan
Write-Host "AI Investment Research Analyst" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Starting FastAPI Backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

Write-Host ""
Write-Host "Waiting 3 seconds for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "Starting Next.js Frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd ai-investment-research-analyst; npm run dev"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Both servers are starting up!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Blue
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Blue
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
