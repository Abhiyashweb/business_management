from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
from models import Business

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    if not all([first_name, last_name, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    # Check if email already exists
    if Business.get_by_email(email):
        return jsonify({"error": "Email already registered"}), 400

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Create business
    business_id = Business.create(first_name, last_name, email, hashed_password.decode('utf-8'))

    return jsonify({"message": "Business registered successfully", "business_id": business_id}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    business = Business.get_by_email(email)
    if not business:
        return jsonify({"error": "Invalid credentials"}), 401

    # Verify password
    if not bcrypt.checkpw(password.encode('utf-8'), business['password'].encode('utf-8')):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create JWT token
    access_token = create_access_token(identity=business['id'])

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "business": {
            "id": business['id'],
            "first_name": business['first_name'],
            "last_name": business['last_name'],
            "email": business['email']
        }
    }), 200