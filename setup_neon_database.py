import psycopg2
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
    
    # Drop existing table (if you want fresh start)
    print("🗑️ Dropping existing table (if exists)...")
    cursor.execute("DROP TABLE IF EXISTS secure_db CASCADE;")
    
    # Create table with proper structure
    print("📝 Creating secure_db table...")
    cursor.execute("""
        CREATE TABLE secure_db (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            role TEXT,
            salary TEXT,
            record_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Create indexes for performance
    print("⚡ Creating indexes...")
    cursor.execute("CREATE INDEX idx_name ON secure_db(name);")
    cursor.execute("CREATE INDEX idx_created_at ON secure_db(created_at);")
    cursor.execute("CREATE INDEX idx_record_hash ON secure_db(record_hash);")
    
    # Insert sample data
    print("📊 Inserting sample data...")
    cursor.execute("""
        INSERT INTO secure_db (name, role, salary, record_hash) 
        VALUES 
            ('Alice', 'Engineer', '70000', 'sample_hash_alice'),
            ('Bob', 'Manager', '80000', 'sample_hash_bob'),
            ('Charlie', 'Developer', '65000', 'sample_hash_charlie');
    """)
    
    conn.commit()
    
    # Verify setup
    cursor.execute("SELECT COUNT(*) FROM secure_db;")
    count = cursor.fetchone()[0]
    
    cursor.execute("SELECT * FROM secure_db ORDER BY id;")
    rows = cursor.fetchall()
    
    print(f"\n✅ Setup completed successfully!")
    print(f"📊 Total records: {count}\n")
    
    print("Records in database:")
    print("-" * 80)
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Role: {row[2]}, Salary: ${row[3]}")
    print("-" * 80)
    
    cursor.close()
    conn.close()
    
    print("\n🚀 Your Neon database is ready!")
    print("You can now start your backend with: uvicorn backend.main:app --reload")
    
except Exception as e:
    print(f"❌ Setup failed: {e}")
