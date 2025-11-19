from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("🧪 Comprehensive Blockchain Test\n")
print(f"Contract: {CONTRACT_ADDRESS}")
print(f"Network: Sepolia Testnet\n")

# Load ABI
with open(os.path.join(SCRIPT_DIR, 'contract_abi_v2.json'), 'r') as f:
    ABI = json.load(f)

# Connect
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

print(f"✅ Connected: {w3.is_connected()}\n")

# Test each employee
for emp_id in [1, 2, 3]:
    print(f"{'='*80}")
    print(f"Testing Employee ID: {emp_id}")
    print(f"{'='*80}")
    
    try:
        # Method 1: Direct call
        result = contract.functions.getHash(emp_id).call()
        print(f"✅ Raw result: {result}")
        print(f"✅ Hex: {result.hex()}")
        print(f"✅ Length: {len(result)} bytes")
        
        if result == b'\x00' * 32:
            print("⚠️  Hash is all zeros (not found or not confirmed)")
        else:
            print(f"✅ Hash found on blockchain!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e)}")
        
        # Try to get more details
        try:
            # Check if function exists
            print(f"\n🔍 Checking contract functions...")
            print(f"Available functions: {[fn.fn_name for fn in contract.all_functions()]}")
        except:
            pass
    
    print()

# Check recent transactions to this contract
print(f"\n{'='*80}")
print("Recent Transactions to Contract")
print(f"{'='*80}")
print(f"View on Etherscan:")
print(f"https://sepolia.etherscan.io/address/{CONTRACT_ADDRESS}#internaltx")
print()

# Verify contract bytecode exists
code = w3.eth.get_code(CONTRACT_ADDRESS)
print(f"Contract code length: {len(code)} bytes")
if len(code) < 100:
    print("⚠️  Warning: Contract might not be deployed properly")
else:
    print("✅ Contract is deployed")
