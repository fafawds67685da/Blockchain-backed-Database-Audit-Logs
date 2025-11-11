import psycopg2

try:
    conn = psycopg2.connect(
        "postgresql://neondb_owner:npg_YFqTmsx8vwc9@ep-tiny-poetry-ahhtzm5d-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
    )
    
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS secure_db (
            id SERIAL PRIMARY KEY,
            name TEXT,
            role TEXT,
            salary TEXT,
            record_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    print("✅ Table created successfully!")
    
    # Check existing records
    cursor.execute("SELECT COUNT(*) FROM secure_db;")
    count = cursor.fetchone()[0]
    print(f"📊 Current records: {count}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
