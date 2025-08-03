from flask import Flask
from flask_jwt_extended import JWTManager
from utils.database import get_db, init_db
from models import Business, Customer, Product, Invoice
from routes.auth import auth_bp
from routes.business import business_bp
from routes.customer import customer_bp
from routes.product import product_bp
from routes.invoice import invoice_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    
    init_db(app)
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(business_bp, url_prefix='/api/business')
    app.register_blueprint(customer_bp, url_prefix='/api/customers')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(invoice_bp, url_prefix='/api/invoices')

    
    with app.app_context():
        try:
            conn = get_db()
            if conn is None:
                raise Exception("Failed to connect to database")
                
            Business.create_table()
            Customer.create_table()
            Product.create_table()
            Invoice.create_table()
            print("All tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {str(e)}")
            # Don't raise here so the server can still start for testing
    
    return app

    
    
    

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)