import psycopg2
import os
from dotenv import load_dotenv
from blockchain_client import push_hash, fetch_hash, w3
import time

load_dotenv()

print("🔄 Re-pushing records to blockchain with verification\n")

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
    cursor.execute("SELECT id, name, record_hash FROM secure_db ORDER BY id;")
    rows = cursor.fetchall()
    
    # Check wallet balance first
    account = os.getenv("ACCOUNT_ADDRESS")
    balance = w3.eth.get_balance(account)
    balance_eth = w3.from_wei(balance, 'ether')
    
    print(f"💰 Wallet Balance: {balance_eth} ETH\n")
    
    if balance == 0:
        print("❌ No ETH in wallet! Get Sepolia ETH from:")
        print("   https://sepoliafaucet.com")
        print("   https://www.alchemy.com/faucets/ethereum-sepolia")
        exit(1)
    
    for emp_id, name, record_hash in rows:
        print(f"{'='*80}")
        print(f"Employee ID {emp_id}: {name}")
        
        # First check if already exists
        try:
            existing = fetch_hash(emp_id)
            if existing != "0" * 64:
                print(f"✅ Already on blockchain: {existing[:32]}...")
                print(f"Skipping...\n")
                continue
        except:
            pass
        
        # Push to blockchain
        print(f"Pushing hash: {record_hash[:32]}...")
        
        try:
            receipt = push_hash(emp_id, record_hash)
            
            if receipt and receipt['status'] == 1:
                tx_hash = receipt['transactionHash'].hex()
                print(f"✅ Success! TX: {tx_hash}")
                print(f"   Gas used: {receipt['gasUsed']}")
                print(f"   Block: {receipt['blockNumber']}")
                print(f"   Etherscan: https://sepolia.etherscan.io/tx/{tx_hash}")
                
                # Wait for confirmation
                print(f"⏳ Waiting 10 seconds for confirmation...")
                time.sleep(10)
                
                # Verify it's readable
                verified = fetch_hash(emp_id)
                if verified != "0" * 64:
                    print(f"✅ Verified on blockchain: {verified[:32]}...")
                else:
                    print(f"⚠️  Not yet readable (may need more time)")
                    
            else:
                print(f"❌ Transaction failed")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print()
        time.sleep(3)  # Rate limiting
    
    cursor.close()
    conn.close()
    
    print("✅ Process complete!")
    
except Exception as e:
    print(f"❌ Error: {e}")
