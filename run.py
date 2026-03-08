from app import create_app

app = create_app()

if __name__ == '__main__':
    print("🚀 Mubeen Portfolio Backend running!")
    print("📡 API: http://localhost:5000/api")
    print("📂 Projects: http://localhost:5000/api/projects")
    print("📝 Blog: http://localhost:5000/api/blog")
    app.run(debug=True, host='0.0.0.0', port=5000)