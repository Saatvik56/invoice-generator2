# Flask Invoice Generator with PDF & Google Drive Upload

A professional web application built with Flask that allows users to generate invoices, preview them, download as PDFs, and upload directly to Google Drive.

## Features

- **Dynamic Invoice Creation**: Create invoices with multiple items, GST calculations, and professional formatting
- **PDF Generation**: Generate high-quality PDFs using Playwright
- **Google Drive Integration**: Upload invoices directly to Google Drive with OAuth 2.0 authentication
- **Professional Templates**: Clean, professional invoice layouts
- **Automatic Calculations**: GST calculations, discounts, and amount in words
- **Preview & Edit**: Preview invoices before generating PDFs

## Technologies Used

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS, Bootstrap 5
- **PDF Generation**: Playwright (Python library)
- **Google Drive Integration**: Google API Python Client
- **Web Server**: Gunicorn (for deployment)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd invoice-generator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

5. **Set up Google Drive API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Google Drive API
   - Create OAuth 2.0 credentials (Web application)
   - Download the `client_secret.json` file and replace the placeholder in the project root
   - Add your redirect URIs:
     - `http://localhost:5000/oauth2callback` (for local development)
     - `https://your-domain.com/oauth2callback` (for production)

6. **Configure environment variables**
   - Set `SECRET_KEY` environment variable or update it in `config.py`
   - Update the `client_secret.json` with your Google API credentials

7. **Add your company logo**
   - Replace `static/logo.png` with your company logo
   - The logo should be in PNG format and reasonably sized (recommended: 200x100px)

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the application**
   - Open your browser and go to `http://localhost:5000`

3. **Create an invoice**
   - Click "New Invoice"
   - Fill in the invoice details
   - Add items dynamically using the "Add Item" button
   - Click "Preview Invoice"

4. **Preview and manage**
   - Review the invoice preview
   - Edit if needed using "Go Back & Edit"
   - Download PDF using "Download PDF"
   - Upload to Google Drive using "Upload to Drive"

## Google Drive Setup

1. **Enable Google Drive API**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Select your project
   - Go to "APIs & Services" > "Library"
   - Search for "Google Drive API" and enable it

2. **Create OAuth 2.0 credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Web application"
   - Add authorized redirect URIs:
     - `http://localhost:5000/oauth2callback`
     - `https://your-domain.com/oauth2callback`
   - Download the JSON file and save as `client_secret.json`

## Deployment

### Using Gunicorn

1. **Install Gunicorn**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

### Environment Variables for Production

Set these environment variables in your production environment:

```bash
export SECRET_KEY="your-very-secure-secret-key"
export FLASK_ENV="production"
```

## File Structure

```
invoice-generator/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── client_secret.json    # Google API credentials
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Home page
│   ├── invoice_form.html # Invoice creation form
│   ├── preview.html     # Invoice preview page
│   └── invoice_pdf.html # PDF invoice template
├── static/              # Static files
│   └── logo.png        # Company logo
└── README.md           # This file
```

## API Endpoints

- `GET /` - Home page
- `GET /new-invoice` - Invoice creation form
- `POST /create-invoice` - Process invoice data
- `GET /preview/<invoice_no>` - Preview invoice
- `GET /edit-invoice/<invoice_no>` - Edit existing invoice
- `GET /generate-pdf/<invoice_no>` - Download PDF
- `GET /authorize` - Google OAuth authorization
- `GET /oauth2callback` - Google OAuth callback
- `GET /upload-to-drive/<invoice_no>` - Upload to Google Drive

## Features Explained

### Dynamic Item Management
- Add/remove invoice items dynamically
- Each item includes description, HSN code, quantity, rate, and tax rates
- Automatic calculation of item amounts

### GST Calculations
- Support for CGST, SGST, and IGST
- Automatic tax calculations based on rates
- Proper handling of interstate vs intrastate transactions

### PDF Generation
- Uses Playwright for high-quality PDF generation
- Maintains professional formatting
- Print-ready output with proper margins and styling

### Google Drive Integration
- Secure OAuth 2.0 authentication
- Direct upload to user's Google Drive
- Automatic file naming with invoice number and date

## Troubleshooting

### Common Issues

1. **Playwright browser not found**
   ```bash
   playwright install chromium
   ```

2. **Google Drive upload fails**
   - Check if `client_secret.json` is properly configured
   - Verify redirect URIs match your application URL
   - Ensure Google Drive API is enabled

3. **PDF generation fails**
   - Check if Playwright is properly installed
   - Verify the invoice template renders correctly
   - Check for any HTML/CSS issues in the template

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository.
