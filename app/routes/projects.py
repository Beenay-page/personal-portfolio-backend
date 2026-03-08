from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.utils.oracle_connect import get_db, row_to_dict

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
def get_projects():
    try:
        category = request.args.get('category')
        conn = get_db()
        cursor = conn.cursor()
        
        # Debug - check tables visible
        cursor.execute("""
            SELECT table_name FROM user_tables 
            WHERE table_name = 'PROJECTS'
        """)
        table_check = cursor.fetchone()
        print(f"DEBUG - Projects table found: {table_check}")
        
        # Debug - check row count
        cursor.execute("SELECT COUNT(*) FROM projects")
        count = cursor.fetchone()
        print(f"DEBUG - Projects count: {count}")
        
        if category:
            cursor.execute(
                "SELECT * FROM projects WHERE category = :1 ORDER BY display_order",
                [category]
            )
        else:
            cursor.execute(
                "SELECT * FROM projects ORDER BY display_order"
            )
        
        projects = [row_to_dict(cursor, row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({"success": True, "data": projects})
    
    except Exception as e:
        print(f"DEBUG - Full error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500


@projects_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM projects WHERE id = :1", [project_id]
        )
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return jsonify({"error": "Project not found"}), 404
        
        project = row_to_dict(cursor, row)
        conn.close()
        return jsonify({"success": True, "data": project})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@projects_bp.route('/admin/projects', methods=['POST'])
@jwt_required()
def create_project():
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO projects 
            (title, description, category, technologies,
             project_link, featured, display_order)
            VALUES (:1, :2, :3, :4, :5, :6, :7)
        """, (
            data['title'], data['description'],
            data['category'], data.get('technologies', ''),
            data.get('project_link', ''),
            1 if data.get('featured') else 0,
            data.get('display_order', 0)
        ))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Project created"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@projects_bp.route('/admin/projects/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE projects SET
            title = :1, description = :2,
            category = :3, technologies = :4,
            project_link = :5, featured = :6
            WHERE id = :7
        """, (
            data['title'], data['description'],
            data['category'], data.get('technologies', ''),
            data.get('project_link', ''),
            1 if data.get('featured') else 0,
            project_id
        ))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Project updated"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@projects_bp.route('/admin/projects/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM projects WHERE id = :1", [project_id]
        )
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Project deleted"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500