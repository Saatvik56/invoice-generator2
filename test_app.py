#!/usr/bin/env python3
"""
Simple test script to verify the Flask application works correctly.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    try:
        import flask
        print("OK Flask imported successfully")
    except ImportError:
        print("ERROR Flask not found. Install with: pip install flask")
        return False
    
    try:
        import playwright
        print("OK Playwright imported successfully")
    except ImportError:
        print("ERROR Playwright not found. Install with: pip install playwright")
        return False
    
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import Flow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaIoBaseUpload
        print("OK Google API libraries imported successfully")
    except ImportError:
        print("ERROR Google API libraries not found. Install with: pip install google-auth google-auth-oauthlib google-api-python-client")
        return False
    
    try:
        from dotenv import load_dotenv
        print("OK python-dotenv imported successfully")
    except ImportError:
        print("ERROR python-dotenv not found. Install with: pip install python-dotenv")
        return False
    
    try:
        from PIL import Image
        print("OK Pillow imported successfully")
    except ImportError:
        print("ERROR Pillow not found. Install with: pip install Pillow")
        return False
    
    return True

def test_files():
    """Test if all required files exist."""
    required_files = [
        'app.py',
        'config.py',
        'requirements.txt',
        'client_secret.json',
        'templates/base.html',
        'templates/index.html',
        'templates/invoice_form.html',
        'templates/preview.html',
        'templates/invoice_pdf.html',
        'static/logo.png'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"OK {file_path} exists")
        else:
            print(f"ERROR {file_path} missing")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def test_app_creation():
    """Test if the Flask app can be created without errors."""
    try:
        from app import app
        print("OK Flask app created successfully")
        return True
    except Exception as e:
        print(f"ERROR Error creating Flask app: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Flask Invoice Generator Application")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("File Existence Tests", test_files),
        ("App Creation Test", test_app_creation)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        result = test_func()
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("OK All tests passed! The application is ready to run.")
        print("\nTo start the application:")
        print("  python app.py")
        print("\nTo install Playwright browsers:")
        print("  playwright install chromium")
    else:
        print("ERROR Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
