from web3 import Web3

# ----------------------------
# Connect to Infura Sepolia
# ----------------------------
INFURA_URL = "https://sepolia.infura.io/v3/b8493b4b87a64d9f978c6e81d46ef547"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

if not w3.is_connected():
    raise Exception("Unable to connect to Sepolia via Infura")
print("✅ Connected to Sepolia testnet")

# ----------------------------
# Contract info
# ----------------------------
CONTRACT_ADDRESS = "0xfD115a384aA50D3461650FF5aD5DB63768c5E037"  # Your Remix VM deployed contract
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "recordHash", "type": "string"}
        ],
        "name": "addHash",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string", "name": "name", "type": "string"}],
        "name": "getHash",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)

# ----------------------------
# Your Sepolia account info
# ----------------------------
ACCOUNT_ADDRESS = "0xC5b97376B9640E7E112CD9826E8B237B7bD00cDe"  # Example: "0x1234...abcd"
PRIVATE_KEY = "00a181430af4d382362c3b14064f1fdb51bcf71ae36bf2ea0b52bf3ae9f38d0c"          # Keep this secret!

account = Web3.to_checksum_address(ACCOUNT_ADDRESS)

# ----------------------------
# Push hash to blockchain
# ----------------------------
def push_hash(employee_name, record_hash):
    nonce = w3.eth.get_transaction_count(account)

    tx = contract.functions.addHash(employee_name, record_hash).build_transaction({
        'from': account,
        'nonce': nonce,
        'gas': 300000,  # adjust if needed
        'gasPrice': w3.to_wei('5', 'gwei')  # testnet, cheap gas
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"✅ Hash for {employee_name} stored on Sepolia. TX: {tx_hash.hex()}")


# ----------------------------
# Fetch hash from blockchain
# ----------------------------
def fetch_hash(employee_name):
    try:
        record_hash = contract.functions.getHash(employee_name).call()
        return record_hash
    except Exception as e:
        print(f"❌ Error fetching hash for {employee_name}: {str(e)}")
        return None
