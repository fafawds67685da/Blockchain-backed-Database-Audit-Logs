from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Your successful transaction hash
tx_hash = "0xea5e2858561d2c35ec08cc1a1aa227bf420f0af91ea3080d511e4d4b81271ad6"

print("🔍 Getting correct contract address...\n")

tx = w3.eth.get_transaction(tx_hash)
contract_address = tx['to']

print(f"✅ Correct Contract Address: {contract_address}")
print(f"\nUpdate your .env file:")
print(f"CONTRACT_ADDRESS={contract_address}")
print(f"\nView on Etherscan: https://sepolia.etherscan.io/address/{contract_address}")
