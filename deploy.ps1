# Deployment Preparation Script for NGO Website (Windows)
# Run this script before deploying to production

Write-Host "🚀 NGO Website Deployment Preparation" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

# Check if .env exists
if (!(Test-Path .env)) {
    Write-Host "📋 Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ .env file created. Please edit it with your actual values." -ForegroundColor Green
} else {
    Write-Host "✅ .env file already exists." -ForegroundColor Green
}

# Install production dependencies
Write-Host "📦 Installing production dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run migrations
Write-Host "🗄️ Running database migrations..." -ForegroundColor Yellow
python manage.py migrate

# Collect static files
Write-Host "📂 Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput --clear

# Create superuser (optional)
$createSuperuser = Read-Host "👤 Do you want to create a superuser? (y/n)"
if ($createSuperuser -eq "y" -or $createSuperuser -eq "Y") {
    python manage.py createsuperuser
}

Write-Host ""
Write-Host "🎉 Preparation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your production values" -ForegroundColor White
Write-Host "2. Test locally: python manage.py runserver" -ForegroundColor White
Write-Host "3. Deploy to your chosen platform (see DEPLOYMENT_GUIDE.md)" -ForegroundColor White
Write-Host ""
Write-Host "For Heroku deployment:" -ForegroundColor Cyan
Write-Host "  heroku create your-app-name" -ForegroundColor White
Write-Host "  git push heroku main" -ForegroundColor White
Write-Host ""
Write-Host "For other platforms, follow the guide in DEPLOYMENT_GUIDE.md" -ForegroundColor White