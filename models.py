from flask import current_app
from utils.database import get_db

class Business:
    @staticmethod
    def create_table():
        cur = get_db().cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS business (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
        """)
        get_db().commit()

    @staticmethod
    def create(first_name, last_name, email, password):
        cur = get_db().cursor()
        cur.execute(
            "INSERT INTO business (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
            (first_name, last_name, email, password)
        )
        get_db().commit()
        return cur.lastrowid

    @staticmethod
    def get_by_email(email):
        cur = get_db().cursor()
        cur.execute("SELECT * FROM business WHERE email = %s", (email,))
        return cur.fetchone()


class Customer:
    @staticmethod
    def create_table():
        cur = get_db().cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS customer (
            id INT AUTO_INCREMENT PRIMARY KEY,
            business_id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            address TEXT,
            FOREIGN KEY (business_id) REFERENCES business(id) ON DELETE CASCADE
        )
        """)
        get_db().commit()

    @staticmethod
    def create(business_id, name, email, address):
        cur = get_db().cursor()
        cur.execute(
            "INSERT INTO customer (business_id, name, email, address) VALUES (%s, %s, %s, %s)",
            (business_id, name, email, address)
        )
        get_db().commit()
        return cur.lastrowid

    @staticmethod
    def get_by_business(business_id):
        cur = get_db().cursor()
        cur.execute("SELECT * FROM customer WHERE business_id = %s", (business_id,))
        return cur.fetchall()


class Product:
    @staticmethod
    def create_table():
        cur = get_db().cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS product (
            id INT AUTO_INCREMENT PRIMARY KEY,
            business_id INT NOT NULL,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (business_id) REFERENCES business(id) ON DELETE CASCADE
        )
        """)
        get_db().commit()

    @staticmethod
    def create(business_id, name, description, price):
        cur = get_db().cursor()
        cur.execute(
            "INSERT INTO product (business_id, name, description, price) VALUES (%s, %s, %s, %s)",
            (business_id, name, description, price)
        )
        get_db().commit()
        return cur.lastrowid

    @staticmethod
    def get_by_business(business_id):
        cur = get_db().cursor()
        cur.execute("SELECT * FROM product WHERE business_id = %s", (business_id,))
        return cur.fetchall()


class Invoice:
    @staticmethod
    def create_table():
        cur = get_db().cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS invoice (
            id INT AUTO_INCREMENT PRIMARY KEY,
            business_id INT NOT NULL,
            transaction_id VARCHAR(100),
            customer_name VARCHAR(100) NOT NULL,
            due_date DATE NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            FOREIGN KEY (business_id) REFERENCES business(id) ON DELETE CASCADE
        )
        """)
        get_db().commit()

    @staticmethod
    def create(business_id, transaction_id, customer_name, due_date, amount, status='pending'):
        cur = get_db().cursor()
        cur.execute(
            """INSERT INTO invoice (business_id, transaction_id, customer_name, due_date, amount, status) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (business_id, transaction_id, customer_name, due_date, amount, status)
        )
        get_db().commit()
        return cur.lastrowid

    @staticmethod
    def get_by_business(business_id):
        cur = get_db().cursor()
        cur.execute("SELECT * FROM invoice WHERE business_id = %s", (business_id,))
        return cur.fetchall()