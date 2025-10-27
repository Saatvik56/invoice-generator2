# Deployment Guide for Invoice Generator

## 🚂 **Railway Deployment (Recommended)**

Railway is the easiest and most reliable option for your invoice generator. It offers:
- Free tier with generous limits
- Automatic deployments from GitHub
- Built-in environment variable management
- No CLI installation required

### Steps to Deploy

1. **Push your code to GitHub**
   ```bash
   # Create a repository on GitHub first, then:
   git remote add origin https://github.com/yourusername/invoice-generator.git
   git push -u origin master
   ```

2. **Deploy on Railway**
   - Go to https://railway.app
   - Sign up with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your invoice-generator repository
   - Railway will automatically detect it's a Python app

3. **Set Environment Variables**
   - Go to your project dashboard
   - Click on "Variables" tab
   - Add these variables:
     - `SECRET_KEY`: Generate one with: `python -c "import secrets; print(secrets.token_hex(32))"`
     - `FLASK_ENV`: `production`

4. **Install Playwright**
   - Go to "Deployments" tab
   - Click on your deployment
   - Open the console/terminal
   - Run: `playwright install chromium`

5. **Your app is live!**
   - Railway will provide you with a URL
   - Your invoice generator is now accessible worldwide

## 🎨 **Alternative: Render**

If you prefer Render:

1. Go to https://render.com
2. Sign up and connect GitHub
3. Create new Web Service
4. Select your repository
5. Set these settings:
   - **Build Command**: `pip install -r requirements.txt && playwright install chromium`
   - **Start Command**: `gunicorn app:app`
6. Add environment variables:
   - `SECRET_KEY`: Generate a random key
   - `FLASK_ENV`: `production`
7. Deploy

## 🔧 **Local Testing Before Deployment**

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

2. **Run locally:**
   ```bash
   python app.py
   ```

3. **Test all features:**
   - Create invoice
   - Preview invoice
   - Download PDF
   - Edit invoice

## 📋 **Environment Variables**

Only two variables needed:
- `SECRET_KEY`: A random secret key for Flask sessions
- `FLASK_ENV`: Set to `production` for production deployment

## 🚀 **Features Ready for Production**

✅ Invoice creation and editing  
✅ PDF generation and download  
✅ Preview functionality  
✅ Responsive design  
✅ Professional invoice layout  
✅ GST calculations  
✅ All custom styling and branding  

## 🔍 **Troubleshooting**

- **PDF generation fails**: Ensure Playwright is installed with `playwright install chromium`
- **App won't start**: Check environment variables are set correctly
- **Styling issues**: Verify all static files are included in deployment

## 💡 **Why Railway?**

- **Easiest setup**: No CLI installation required
- **Automatic deployments**: Push to GitHub = automatic deployment
- **Free tier**: Generous limits for personal/small business use
- **Built-in monitoring**: Easy to see logs and performance
- **Custom domains**: Easy to add your own domain later
