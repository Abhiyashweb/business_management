from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Invoice
from datetime import datetime

invoice_bp = Blueprint('invoice', __name__)

@invoice_bp.route('/invoices', methods=['GET'])
@jwt_required()
def get_invoices():
    business_id = get_jwt_identity()
    invoices = Invoice.get_by_business(business_id)
    return jsonify(invoices), 200

@invoice_bp.route('/invoices', methods=['POST'])
@jwt_required()
def create_invoice():
    business_id = get_jwt_identity()
    data = request.get_json()
    
    transaction_id = data.get('transaction_id')
    customer_name = data.get('customer_name')
    due_date = data.get('due_date')
    amount = data.get('amount')
    status = data.get('status', 'pending')

    if not all([customer_name, due_date, amount]):
        return jsonify({"error": "Customer name, due date, and amount are required"}), 400

    try:
        due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({"error": "Amount must be a number"}), 400

    invoice_id = Invoice.create(business_id, transaction_id, customer_name, due_date, amount, status)
    return jsonify({"message": "Invoice created successfully", "invoice_id": invoice_id}), 201