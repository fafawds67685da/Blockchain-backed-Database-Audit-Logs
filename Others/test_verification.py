from Others.blockchain_client import fetch_hash
import psycopg2
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

print("🧪 Testing Blockchain Verification\n")

try:
    # Connect to database
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        sslmode='require'
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, role, salary, record_hash, created_at FROM secure_db ORDER BY id;")
    rows = cursor.fetchall()
    
    for row in rows:
        emp_id, name, role, salary, stored_hash, created_at = row
        
        print(f"\n{'='*80}")
        print(f"Employee ID {emp_id}: {name}")
        print(f"{'='*80}")
        
        # Compute hash
        combined_data = f"{name}{role}{salary}{created_at.isoformat()}".encode('utf-8')
        computed_hash = hashlib.sha256(combined_data).hexdigest()
        
        # Fetch from blockchain
        blockchain_hash = fetch_hash(emp_id)
        
        print(f"Stored Hash:     {stored_hash[:32]}...")
        print(f"Computed Hash:   {computed_hash[:32]}...")
        print(f"Blockchain Hash: {blockchain_hash[:32]}...")
        
        # Verify
        if stored_hash == computed_hash == blockchain_hash:
            print("✅ INTEGRITY VERIFIED - All hashes match!")
        else:
            print("⚠️ MISMATCH DETECTED!")
            if stored_hash != computed_hash:
                print("   - Stored hash ≠ Computed hash (Data was modified)")
            if blockchain_hash == "0" * 64:
                print("   - Blockchain hash not found (Not yet confirmed)")
            elif stored_hash != blockchain_hash:
                print("   - Stored hash ≠ Blockchain hash (Tampering detected)")
    
    cursor.close()
    conn.close()
    
    print(f"\n{'='*80}")
    print("✅ Verification test complete!")
    print(f"{'='*80}\n")
    
except Exception as e:
    print(f"❌ Error: {e}")
