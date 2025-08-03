from flask_mysqldb import MySQL
from flask import current_app

mysql = MySQL()

def init_db(app):
    app.config['MYSQL_HOST'] = app.config.get('MYSQL_HOST', '127.0.0.1')
    app.config['MYSQL_USER'] = app.config.get('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = app.config.get('MYSQL_PASSWORD', 'abhi20024')
    app.config['MYSQL_DB'] = app.config.get('MYSQL_DB', 'business_management')
    app.config['MYSQL_PORT'] = 3306
    
    mysql.init_app(app)
    with app.app_context():
        try:
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            print("Database connection successful!")
        except Exception as e:
            print(f"Database connection failed: {str(e)}")
            raise RuntimeError("Failed to connect to database") from e


def get_db():
    return mysql.connection