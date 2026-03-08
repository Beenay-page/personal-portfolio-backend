from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.utils.oracle_connect import get_db, row_to_dict
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE email = :1", [email]
        )
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return jsonify({"error": "Invalid credentials"}), 401
        
        user = row_to_dict(cursor, row)
        conn.close()
        
        if bcrypt.checkpw(
            password.encode('utf-8'),
            user['password'].encode('utf-8')
        ):
            token = create_access_token(identity=str(user['id']))
            return jsonify({
                "success": True,
                "token": token,
                "user": {
                    "email": user['email'],
                    "username": user['username']
                }
            })
        
        return jsonify({"error": "Invalid credentials"}), 401
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500