from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Customer

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    business_id = get_jwt_identity()
    customers = Customer.get_by_business(business_id)
    return jsonify(customers), 200

@customer_bp.route('/customers', methods=['POST'])
@jwt_required()
def create_customer():
    business_id = get_jwt_identity()
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    address = data.get('address')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    customer_id = Customer.create(business_id, name, email, address)
    return jsonify({"message": "Customer created successfully", "customer_id": customer_id}), 201