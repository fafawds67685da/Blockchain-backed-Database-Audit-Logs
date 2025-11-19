from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Transaction hash from your successful push
tx_hash = "0xea5e2858561d2c35ec08cc1a1aa227bf420f0af91ea3080d511e4d4b81271ad6"

print(f"🔍 Analyzing transaction: {tx_hash}\n")

try:
    tx = w3.eth.get_transaction(tx_hash)
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    
    print(f"From: {tx['from']}")
    print(f"To (Contract): {tx['to']}")
    print(f"Status: {'✅ Success' if receipt['status'] == 1 else '❌ Failed'}")
    print(f"Block: {receipt['blockNumber']}")
    print(f"Gas Used: {receipt['gasUsed']}")
    
    contract_address = tx['to']
    print(f"\n📍 Contract Address: {contract_address}")
    print(f"\n🔗 View on Etherscan:")
    print(f"   Transaction: https://sepolia.etherscan.io/tx/{tx_hash}")
    print(f"   Contract: https://sepolia.etherscan.io/address/{contract_address}")
    
    # Check if this matches .env
    env_contract = os.getenv("CONTRACT_ADDRESS")
    print(f"\n🔧 Current .env CONTRACT_ADDRESS: {env_contract}")
    
    if env_contract.lower() == contract_address.lower():
        print("✅ Addresses match!")
    else:
        print("❌ MISMATCH! Update your .env file:")
        print(f"\nCONTRACT_ADDRESS={contract_address}")
        
except Exception as e:
    print(f"❌ Error: {e}")
