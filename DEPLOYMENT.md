# Deployment Guide for Invoice Generator

## Option 1: Heroku Deployment (Recommended - Free Tier Available)

### Prerequisites
1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Create a Heroku account: https://heroku.com

### Steps to Deploy

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**
   ```bash
   heroku create your-invoice-app-name
   ```

3. **Set environment variables**
   ```bash
   heroku config:set SECRET_KEY=your-super-secret-key-here
   heroku config:set FLASK_ENV=production
   ```

4. **Install Playwright dependencies**
   ```bash
   heroku run playwright install chromium
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

6. **Open your app**
   ```bash
   heroku open
   ```

## Option 2: Railway Deployment

### Prerequisites
1. Create Railway account: https://railway.app
2. Connect your GitHub repository

### Steps
1. Go to Railway.app
2. Create new project from GitHub
3. Select your repository
4. Add environment variables in Railway dashboard
5. Deploy automatically

## Option 3: Render Deployment

### Prerequisites
1. Create Render account: https://render.com
2. Connect your GitHub repository

### Steps
1. Go to Render.com
2. Create new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt && playwright install chromium`
5. Set start command: `gunicorn app:app`
6. Add environment variables
7. Deploy

## Environment Variables Needed

- `SECRET_KEY`: A random secret key for Flask sessions
- `FLASK_ENV`: Set to `production` for production deployment

## Important Notes

1. **Playwright Installation**: The app uses Playwright for PDF generation. Make sure to install Chromium:
   ```bash
   playwright install chromium
   ```

2. **Google Drive Integration**: If you want to use Google Drive upload feature:
   - Set up Google Cloud Console project
   - Enable Google Drive API
   - Create OAuth 2.0 credentials
   - Update `client_secret.json` with your credentials

3. **File Storage**: Currently uses in-memory storage. For production, consider:
   - Adding a database (PostgreSQL)
   - Using Redis for caching
   - File storage service (AWS S3, Google Cloud Storage)

4. **Security**: 
   - Change the SECRET_KEY to a random value
   - Use HTTPS in production
   - Consider adding authentication if needed

## Testing Locally Before Deployment

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. Run the app:
   ```bash
   python app.py
   ```

3. Test PDF generation and all features

## Troubleshooting

- If PDF generation fails, ensure Playwright is installed
- Check logs: `heroku logs --tail` (for Heroku)
- Verify all environment variables are set
- Ensure `client_secret.json` is present for Google Drive features
