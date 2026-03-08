from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.oracle_connect import get_db, row_to_dict

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/blog', methods=['GET'])
def get_posts():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM blog_posts WHERE published = 1 ORDER BY created_at DESC"
        )
        posts = [row_to_dict(cursor, row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({"success": True, "data": posts})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@blog_bp.route('/blog/<slug>', methods=['GET'])
def get_post(slug):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM blog_posts WHERE slug = :1", [slug]
        )
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return jsonify({"error": "Post not found"}), 404
        
        post = row_to_dict(cursor, row)
        conn.close()
        return jsonify({"success": True, "data": post})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@blog_bp.route('/admin/blog', methods=['POST'])
@jwt_required()
def create_post():
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO blog_posts
            (title, slug, content, excerpt,
             category, tags, published)
            VALUES (:1, :2, :3, :4, :5, :6, :7)
        """, (
            data['title'], data['slug'],
            data['content'], data.get('excerpt', ''),
            data['category'], data.get('tags', ''),
            1 if data.get('published') else 0
        ))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Post created"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@blog_bp.route('/admin/blog/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM blog_posts WHERE id = :1", [post_id]
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Post deleted"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500