from web3 import Web3
import os
from dotenv import load_dotenv, set_key

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

tx_hash = "0xea5e2858561d2c35ec08cc1a1aa227bf420f0af91ea3080d511e4d4b81271ad6"

print("🔧 Auto-fixing CONTRACT_ADDRESS in .env...\n")

try:
    tx = w3.eth.get_transaction(tx_hash)
    correct_address = tx['to']
    
    print(f"✅ Found contract address: {correct_address}")
    
    # Update .env file
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    set_key(env_file, 'CONTRACT_ADDRESS', correct_address)
    
    print(f"✅ Updated .env file with correct address")
    print(f"\n🔄 Please restart your backend:")
    print(f"   cd backend")
    print(f"   uvicorn main:app --reload")
    
except Exception as e:
    print(f"❌ Error: {e}")
