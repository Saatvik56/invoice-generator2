import os
import base64
import json
import io
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from config import Config

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

# In-memory cache for invoice data (in production, use Redis or database)
invoice_cache = {}

def encode_image_to_base64(image_path):
    """Encode image file to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return f"data:image/png;base64,{encoded_string}"
    except FileNotFoundError:
        return None

def number_to_words(number):
    """Convert number to words in Indian numbering system"""
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    
    def convert_hundreds(n):
        result = ""
        if n > 99:
            result += ones[n // 100] + " Hundred "
            n %= 100
        if n > 19:
            result += tens[n // 10] + " "
            n %= 10
        elif n > 9:
            result += teens[n - 10] + " "
            return result
        if n > 0:
            result += ones[n] + " "
        return result
    
    if number == 0:
        return "Zero"
    
    result = ""
    if number >= 10000000:  # Crores
        result += convert_hundreds(number // 10000000) + "Crore "
        number %= 10000000
    if number >= 100000:  # Lakhs
        result += convert_hundreds(number // 100000) + "Lakh "
        number %= 100000
    if number >= 1000:  # Thousands
        result += convert_hundreds(number // 1000) + "Thousand "
        number %= 1000
    if number > 0:
        result += convert_hundreds(number)
    
    return result.strip() + " Rupees Only"

def calculate_invoice_totals(items, discount_amount):
    """Calculate invoice totals"""
    subtotal = 0
    for item in items:
        item['amount'] = item['quantity'] * item['rate']
        subtotal += item['amount']
    
    discounted_subtotal = subtotal - discount_amount
    if discounted_subtotal < 0:
        discounted_subtotal = 0
    
    # Calculate taxes based on global rates (all items have same rates)
    cgst_total = 0
    sgst_total = 0
    igst_total = 0
    
    if items:  # Check if there are items
        # Use the first item's rates (since all items have same rates now)
        cgst_rate = items[0]['cgst_rate']
        sgst_rate = items[0]['sgst_rate']
        igst_rate = items[0]['igst_rate']
        
        if cgst_rate > 0 and sgst_rate > 0:
            # Use CGST + SGST for same state
            cgst_total = (discounted_subtotal * cgst_rate) / 100
            sgst_total = (discounted_subtotal * sgst_rate) / 100
        elif igst_rate > 0:
            # Use IGST for different states
            igst_total = (discounted_subtotal * igst_rate) / 100
    
    grand_total = discounted_subtotal + cgst_total + sgst_total + igst_total
    round_off = int(grand_total) - grand_total
    final_total = int(grand_total)
    
    return {
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'discounted_subtotal': discounted_subtotal,
        'cgst_total': cgst_total,
        'sgst_total': sgst_total,
        'igst_total': igst_total,
        'grand_total': grand_total,
        'round_off': round_off,
        'final_total': final_total,
        'amount_in_words': number_to_words(final_total)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new-invoice')
def new_invoice():
    return render_template('invoice_form.html')

@app.route('/create-invoice', methods=['POST'])
def create_invoice():
    try:
        # Extract form data
        invoice_data = {
            'invoice_number': request.form.get('invoice_number'),
            'invoice_date': request.form.get('invoice_date'),
            'date_of_supply': request.form.get('date_of_supply'),
            'vehicle_no': request.form.get('vehicle_no'),
            'gr_rr_no': request.form.get('gr_rr_no'),
            'electronic_ref_no': request.form.get('electronic_ref_no'),
            'billed_to': {
                'name': request.form.get('billed_to_name'),
                'place_of_supply': request.form.get('billed_to_address'),
                'state': request.form.get('billed_to_state'),
                'state_code': request.form.get('billed_to_state_code'),
                'gstin': request.form.get('billed_to_gstin')
            },
            'invoice_items': []
        }
        
        # Extract items data
        descriptions = request.form.getlist('item_description')
        hsn_codes = request.form.getlist('item_hsn')
        quantities = request.form.getlist('item_quantity')
        uoms = request.form.getlist('item_uom')
        rates = request.form.getlist('item_rate')
        
        # Extract global GST rates
        try:
            cgst_rate = float(request.form.get('cgst_rate', 0) or 0)
            sgst_rate = float(request.form.get('sgst_rate', 0) or 0)
            igst_rate = float(request.form.get('igst_rate', 0) or 0)
        except ValueError:
            cgst_rate = sgst_rate = igst_rate = 0
        
        for i in range(len(descriptions)):
            if descriptions[i]:  # Only add non-empty items
                try:
                    item = {
                        'description': descriptions[i],
                        'hsn_code': hsn_codes[i] if hsn_codes[i] else '',
                        'quantity': float(quantities[i]) if quantities[i] and quantities[i].strip() else 0,
                        'uom': uoms[i] if uoms[i] else '',
                        'rate': float(rates[i]) if rates[i] and rates[i].strip() else 0,
                        'cgst_rate': cgst_rate,
                        'sgst_rate': sgst_rate,
                        'igst_rate': igst_rate
                    }
                    invoice_data['invoice_items'].append(item)
                except ValueError as e:
                    flash(f'Invalid number format in item {i+1}: {str(e)}', 'error')
                    return redirect(url_for('new_invoice'))
        
        try:
            discount_amount = float(request.form.get('discount_amount', 0) or 0)
        except ValueError:
            discount_amount = 0
        
        # Validate that at least one item is provided
        if not invoice_data['invoice_items']:
            flash('At least one item is required to create an invoice', 'error')
            return redirect(url_for('new_invoice'))
        
        # Calculate totals
        totals = calculate_invoice_totals(invoice_data['invoice_items'], discount_amount)
        invoice_data.update(totals)
        
        # Store in cache
        invoice_cache[invoice_data['invoice_number']] = invoice_data
        
        return redirect(url_for('preview_invoice', invoice_no=invoice_data['invoice_number']))
        
    except Exception as e:
        flash(f'Error creating invoice: {str(e)}', 'error')
        return redirect(url_for('new_invoice'))

@app.route('/preview/<invoice_no>')
def preview_invoice(invoice_no):
    if invoice_no not in invoice_cache:
        flash('Invoice not found', 'error')
        return redirect(url_for('new_invoice'))
    
    invoice_data = invoice_cache[invoice_no]
    logo_base64 = encode_image_to_base64('static/logo.png')
    
    # Render the invoice HTML
    invoice_html = render_template('invoice_pdf.html', invoice=invoice_data, logo_base64=logo_base64)
    
    return render_template('preview.html', invoice=invoice_data, invoice_html=invoice_html)

@app.route('/edit-invoice/<invoice_no>')
def edit_invoice(invoice_no):
    if invoice_no not in invoice_cache:
        flash('Invoice not found', 'error')
        return redirect(url_for('new_invoice'))
    
    invoice_data = invoice_cache[invoice_no]
    return render_template('invoice_form.html', invoice=invoice_data)

@app.route('/generate-pdf/<invoice_no>')
def generate_pdf(invoice_no):
    if invoice_no not in invoice_cache:
        flash('Invoice not found', 'error')
        return redirect(url_for('new_invoice'))
    
    invoice_data = invoice_cache[invoice_no]
    logo_base64 = encode_image_to_base64('static/logo.png')
    
    # Render invoice HTML
    invoice_html = render_template('invoice_pdf.html', invoice=invoice_data, logo_base64=logo_base64)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_content(invoice_html)
            
            # Generate PDF
            pdf_content = page.pdf(
                format='A4',
                print_background=True
            )
            
            browser.close()
        
        # Create response
        response = make_response(pdf_content)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={invoice_no}_{invoice_data["invoice_date"]}.pdf'
        
        return response
        
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'error')
        return redirect(url_for('preview_invoice', invoice_no=invoice_no))

if __name__ == '__main__':
    app.run(debug=True)
