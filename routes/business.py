from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Business

business_bp = Blueprint('business', __name__)

@business_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    business_id = get_jwt_identity()
    business = Business.get_by_id(business_id)
    
    if not business:
        return jsonify({"error": "Business not found"}), 404

    return jsonify({
        "id": business['id'],
        "first_name": business['first_name'],
        "last_name": business['last_name'],
        "email": business['email']
    }), 200