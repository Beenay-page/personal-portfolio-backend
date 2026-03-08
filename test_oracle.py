import oracledb

# Test different DSN connections
connections_to_try = [
    "localhost:1521/XEPDB1",
    "localhost:1521/XE",
    "localhost:1521/ORCL",
    "localhost:1521/FREE",
]

for dsn in connections_to_try:
    try:
        conn = oracledb.connect(
            user="system",
            password="123456",
            dsn=dsn
        )
        cursor = conn.cursor()
        cursor.execute("SELECT USER FROM dual")
        user = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM user_tables 
            WHERE table_name = 'PROJECTS'
        """)
        found = cursor.fetchone()[0]
        
        print(f"DSN: {dsn} → User: {user} → Projects table: {found}")
        conn.close()
        
    except Exception as e:
        print(f"DSN: {dsn} → FAILED: {str(e)}")