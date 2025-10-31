@echo off
echo ========================================
echo Binance Trading Bot - Vercel Deployment
echo ========================================
echo.

echo Step 1: Checking Git repository...
if not exist .git (
    echo Initializing Git repository...
    git init
    echo Git repository initialized.
) else (
    echo Git repository already exists.
)

echo.
echo Step 2: Adding files to Git...
git add .

echo.
echo Step 3: Creating commit...
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Update: Ready for deployment

git commit -m "%commit_msg%"

echo.
echo ========================================
echo Next Steps:
echo ========================================
echo.
echo 1. Create a GitHub repository at: https://github.com/new
echo.
echo 2. Run these commands:
echo    git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Go to Vercel: https://vercel.com
echo    - Click "Add New Project"
echo    - Import your GitHub repository
echo    - Add environment variables:
echo      * API_KEY = Your Binance API Key
echo      * API_SECRET = Your Binance API Secret
echo    - Click Deploy
echo.
echo ========================================
echo For detailed instructions, see VERCEL_DEPLOYMENT.md
echo ========================================
pause
