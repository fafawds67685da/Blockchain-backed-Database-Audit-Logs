from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
INFURA_URL = os.getenv("INFURA_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load ABI - try v2 first, fallback to v1
try:
    abi_path_v2 = os.path.join(SCRIPT_DIR, 'contract_abi_v2.json')
    with open(abi_path_v2, 'r') as f:
        CONTRACT_ABI = json.load(f)
    print("✅ Using V2 Contract ABI (Employee ID based)")
except FileNotFoundError:
    try:
        abi_path_v1 = os.path.join(SCRIPT_DIR, 'contract_abi.json')
        with open(abi_path_v1, 'r') as f:
            CONTRACT_ABI = json.load(f)
        print("⚠️ Using V1 Contract ABI (Name based)")
    except FileNotFoundError:
        print("❌ ERROR: No contract ABI file found!")
        print(f"Looking for files in: {SCRIPT_DIR}")
        print("Please ensure contract_abi_v2.json or contract_abi.json exists")
        raise

# Connect to blockchain
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

print(f"Connected to Sepolia: {w3.is_connected()}")

def push_hash(employee_id: int, record_hash: str):
    """Push hash to blockchain using employee ID as key"""
    try:
        # Convert hash string to bytes32
        if record_hash.startswith('0x'):
            hash_bytes = bytes.fromhex(record_hash[2:])
        else:
            hash_bytes = bytes.fromhex(record_hash)
        
        # Build transaction
        nonce = w3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        txn = contract.functions.addHash(employee_id, hash_bytes).build_transaction({
            'chainId': 11155111,
            'gas': 200000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })
        
        # Sign and send
        signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        # Wait for confirmation
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"✅ Hash pushed to blockchain for Employee ID {employee_id}. Tx: {tx_hash.hex()}")
        return receipt
    except Exception as e:
        print(f"❌ Error pushing hash: {e}")
        return None

def fetch_hash(employee_id: int) -> str:
    """Fetch hash from blockchain using employee ID"""
    try:
        hash_bytes = contract.functions.getHash(employee_id).call()
        # Return hex string or empty hash if not found
        if hash_bytes == b'\x00' * 32:
            return "0" * 64  # Not found in blockchain
        return hash_bytes.hex()
    except Exception as e:
        print(f"❌ Error fetching hash for ID {employee_id}: {e}")
        return "0" * 64  # Return empty hash on error
