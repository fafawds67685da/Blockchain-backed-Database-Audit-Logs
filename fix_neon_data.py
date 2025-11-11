import psycopg2
import hashlib
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

try:
    print("🔗 Connecting to Neon PostgreSQL...")
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        sslmode='require'
    )
    
    cursor = conn.cursor()
    
    # Get existing records
    cursor.execute("SELECT id, name, role, salary FROM secure_db ORDER BY id;")
    rows = cursor.fetchall()
    
    print(f"Found {len(rows)} records. Updating hashes and timestamps...\n")
    
    for row in rows:
        emp_id, name, role, salary = row
        
        # Generate proper timestamp
        timestamp = datetime.now().isoformat()
        
        # Generate proper hash
        data_to_hash = f"{name}{role}{salary}{timestamp}".encode('utf-8')
        record_hash = hashlib.sha256(data_to_hash).hexdigest()
        
        # Update the record
        cursor.execute("""
            UPDATE secure_db 
            SET record_hash = %s, created_at = %s 
            WHERE id = %s
        """, (record_hash, timestamp, emp_id))
        
        print(f"✅ Updated ID {emp_id}: {name}")
        print(f"   Hash: {record_hash[:32]}...")
        print(f"   Timestamp: {timestamp}\n")
    
    conn.commit()
    
    # Verify
    cursor.execute("SELECT id, name, record_hash, created_at FROM secure_db ORDER BY id;")
    updated_rows = cursor.fetchall()
    
    print("=" * 80)
    print("Updated Records:")
    print("=" * 80)
    for row in updated_rows:
        print(f"ID: {row[0]}, Name: {row[1]}")
        print(f"Hash: {row[2][:32]}...")
        print(f"Created: {row[3]}\n")
    
    cursor.close()
    conn.close()
    
    print("✅ All records updated successfully!")
    print("🔄 Now restart your backend: uvicorn backend.main:app --reload")
    
except Exception as e:
    print(f"❌ Error: {e}")
