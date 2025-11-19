from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

print(f"🔗 Connecting to Sepolia...")
print(f"📍 Contract Address: {CONTRACT_ADDRESS}\n")

# Load ABI
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
abi_path = os.path.join(SCRIPT_DIR, 'contract_abi_v2.json')

with open(abi_path, 'r') as f:
    CONTRACT_ABI = json.load(f)

# Connect
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

print(f"✅ Connected: {w3.is_connected()}\n")

# Check if contract exists
code = w3.eth.get_code(CONTRACT_ADDRESS)
if code == b'' or code == b'\x00':
    print(f"❌ ERROR: No contract found at {CONTRACT_ADDRESS}")
    print("This address has no deployed contract code!")
    print("\n💡 You need to:")
    print("1. Deploy the V2 contract on Remix")
    print("2. Update CONTRACT_ADDRESS in .env with the new address")
else:
    print(f"✅ Contract exists at {CONTRACT_ADDRESS}")
    print(f"Contract code length: {len(code)} bytes\n")
    
    # Try to read hash for employee ID 1
    print("Testing getHash for Employee ID 1...")
    try:
        result = contract.functions.getHash(1).call()
        print(f"✅ Hash found: {result.hex()}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Possible issues:")
        print("1. Contract was deployed but no data was pushed to it")
        print("2. Wrong contract address in .env")
        print("3. Contract ABI doesn't match deployed contract")
        
        # Check transactions
        print(f"\n🔍 Recent transactions to this address:")
        print(f"View on Etherscan: https://sepolia.etherscan.io/address/{CONTRACT_ADDRESS}")
