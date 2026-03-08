from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.oracle_connect import get_db, row_to_dict

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['POST'])
def submit_contact():
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO contact_messages
            (name, email, service_required, message)
            VALUES (:1, :2, :3, :4)
        """, (
            data['name'], data['email'],
            data['service_required'], data['message']
        ))
        conn.commit()
        conn.close()
        return jsonify({
            "success": True,
            "message": "Message sent successfully!"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@contact_bp.route('/admin/messages', methods=['GET'])
@jwt_required()
def get_messages():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM contact_messages ORDER BY created_at DESC"
        )
        messages = [row_to_dict(cursor, row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({"success": True, "data": messages})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@contact_bp.route('/admin/messages/<int:msg_id>/read', methods=['PUT'])
@jwt_required()
def mark_read(msg_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE contact_messages SET is_read = 1 WHERE id = :1",
            [msg_id]
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Marked as read"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500