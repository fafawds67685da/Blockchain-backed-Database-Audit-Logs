import psycopg2
import os
from dotenv import load_dotenv
from blockchain_client import push_hash
import time

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
    
    # Get all records
    cursor.execute("SELECT id, name, record_hash FROM secure_db ORDER BY id;")
    rows = cursor.fetchall()
    
    print(f"\nFound {len(rows)} records to push to blockchain\n")
    
    for emp_id, name, record_hash in rows:
        print(f"Pushing Employee ID {emp_id}: {name}")
        print(f"Hash: {record_hash[:32]}...")
        
        try:
            receipt = push_hash(emp_id, record_hash)
            if receipt:
                tx_hash = receipt['transactionHash'].hex()
                print(f"✅ Pushed successfully! TX: {tx_hash[:16]}...")
                print(f"   View on Etherscan: https://sepolia.etherscan.io/tx/{tx_hash}\n")
                
                # Wait a bit to avoid rate limiting
                time.sleep(2)
            else:
                print(f"❌ Failed to push\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")
    
    cursor.close()
    conn.close()
    
    print("✅ All records processed!")
    print("🔄 Now refresh your dashboard to see verified records")
    
except Exception as e:
    print(f"❌ Error: {e}")
