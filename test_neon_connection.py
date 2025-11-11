import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    print("Connecting to Neon PostgreSQL...")
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        sslmode='require'
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"✅ Connected successfully!")
    print(f"PostgreSQL version: {version[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM secure_db;")
    count = cursor.fetchone()[0]
    print(f"Records in secure_db: {count}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
