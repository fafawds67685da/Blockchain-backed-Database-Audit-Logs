import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    print("🔄 Updating database schema to use manual Employee ID...\n")
    
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        sslmode='require'
    )
    
    cursor = conn.cursor()
    
    # Backup existing data
    print("📦 Backing up existing data...")
    cursor.execute("SELECT id, name, role, salary, record_hash, created_at FROM secure_db ORDER BY id;")
    backup_data = cursor.fetchall()
    print(f"✅ Backed up {len(backup_data)} records\n")
    
    # Drop old table
    print("🗑️ Dropping old table...")
    cursor.execute("DROP TABLE IF EXISTS secure_db CASCADE;")
    
    # Create new table with manual ID (no SERIAL)
    print("📝 Creating new table with manual ID...")
    cursor.execute("""
        CREATE TABLE secure_db (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT,
            salary TEXT,
            record_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Restore data
    print("📥 Restoring data...")
    for row in backup_data:
        cursor.execute("""
            INSERT INTO secure_db (id, name, role, salary, record_hash, created_at)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, row)
    
    conn.commit()
    
    print(f"✅ Restored {len(backup_data)} records")
    print("\n✅ Schema updated successfully!")
    print("🔄 Employee ID is now manually entered by users\n")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
