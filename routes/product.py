from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Product

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    business_id = get_jwt_identity()
    products = Product.get_by_business(business_id)
    return jsonify(products), 200

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    business_id = get_jwt_identity()
    data = request.get_json()
    
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    if not all([name, price]):
        return jsonify({"error": "Name and price are required"}), 400

    try:
        price = float(price)
    except ValueError:
        return jsonify({"error": "Price must be a number"}), 400

    product_id = Product.create(business_id, name, description, price)
    return jsonify({"message": "Product created successfully", "product_id": product_id}), 201