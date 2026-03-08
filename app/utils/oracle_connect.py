import oracledb
import os
from dotenv import load_dotenv

load_dotenv()

def get_db():
    user = os.getenv("ORACLE_USER")
    password = os.getenv("ORACLE_PASSWORD")
    dsn = os.getenv("ORACLE_DSN")
    
    connection = oracledb.connect(
        user=user,
        password=password,
        dsn=dsn
    )
    return connection

def row_to_dict(cursor, row):
    columns = [col[0].lower() for col in cursor.description]
    result = {}
    for col, val in zip(columns, row):
        # Convert Oracle LOB (CLOB) to string
        if hasattr(val, 'read'):
            result[col] = val.read()
        else:
            result[col] = val
    return result