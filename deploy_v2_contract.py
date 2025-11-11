from web3 import Web3
import json
import os
from dotenv import load_dotenv, set_key
from solcx import compile_source, install_solc

load_dotenv()

print("🚀 Deploying V2 Contract to Sepolia...\n")

# Install Solidity compiler
install_solc('0.8.0')

# Contract source code
contract_source = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AuditLogV2 {
    mapping(uint256 => bytes32) private recordHashes;
    
    event HashAdded(uint256 indexed employeeId, bytes32 recordHash, uint256 timestamp);
    
    function addHash(uint256 employeeId, bytes32 recordHash) public {
        require(employeeId > 0, "Employee ID must be greater than 0");
        require(recordHash != bytes32(0), "Hash cannot be empty");
        
        recordHashes[employeeId] = recordHash;
        emit HashAdded(employeeId, recordHash, block.timestamp);
    }
    
    function getHash(uint256 employeeId) public view returns (bytes32) {
        return recordHashes[employeeId];
    }
    
    function hashExists(uint256 employeeId) public view returns (bool) {
        return recordHashes[employeeId] != bytes32(0);
    }
}
"""

# Compile
compiled = compile_source(contract_source, output_values=['abi', 'bin'])
contract_id, contract_interface = compiled.popitem()
bytecode = contract_interface['bin']
abi = contract_interface['abi']

# Connect to Sepolia
w3 = Web3(Web3.HTTPProvider(os.getenv("INFURA_URL")))
account = os.getenv("ACCOUNT_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

# Deploy
Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(account)

tx = Contract.constructor().build_transaction({
    'chainId': 11155111,
    'gas': 2000000,
    'gasPrice': w3.eth.gas_price,
    'nonce': nonce,
})

signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print(f"⏳ Deploying... TX: {tx_hash.hex()}")
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

contract_address = receipt.contractAddress
print(f"\n✅ Contract deployed!")
print(f"📍 Address: {contract_address}")
print(f"🔗 Etherscan: https://sepolia.etherscan.io/address/{contract_address}")

# Update .env
env_file = '.env'
set_key(env_file, 'CONTRACT_ADDRESS', contract_address)
print(f"\n✅ Updated .env with new contract address")

# Save ABI
with open('contract_abi_v2.json', 'w') as f:
    json.dump(abi, f, indent=2)
print(f"✅ Saved ABI to contract_abi_v2.json")
