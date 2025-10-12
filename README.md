
# Blockchain-Backed Database Audit Logs

## Overview
This project secures organizational data by combining a traditional PostgreSQL database with blockchain immutability. 
Instead of storing raw data on-chain, cryptographic hashes of database entries are stored on the blockchain to provide proof-of-existence and ensure data integrity.

## Architecture & Workflow

### Components
1. **PostgreSQL Database (`secure_db`)**: Stores employee records (name, role, salary).
2. **Python Scripts**:
   - `hash_blockchain.py` / `check.py`: Add employees, compute hashes, push to blockchain, verify integrity.
   - `export_live_csv.py`: Continuously exports DB table to a CSV file.
3. **Blockchain**:
   - Smart contract (`smart_contract.sol`) deployed on Ethereum Sepolia testnet.
   - Stores SHA-256 hashes of employee records keyed by employee name.
   - Immutable proof-of-existence: Any tampering in the DB is detectable by mismatch of hashes.
4. **CSV Export**: Real-time export of DB to CSV for external use or backup.

### Workflow
1. Add employee through Python script → Hash generated → Hash stored on blockchain → Employee record saved in DB.
2. Verify integrity → Recompute hash from DB → Compare with blockchain hash → Alert if mismatch.
3. Export live CSV → Periodically fetch DB records → Overwrite CSV file with updated content.

### Blockchain Details
- **Network**: Sepolia testnet via Infura.
- **Smart Contract**:
  - `addHash(name, recordHash)`: Adds/updates hash for a given employee.
  - `getHash(name)`: Fetches hash from blockchain to verify integrity.
- **Security**:
  - Only hashes are stored on-chain (not sensitive data).
  - Data tampering in the DB will be detected since recomputed hash won’t match blockchain hash.
  - Gas-efficient solution: Minimal storage cost while ensuring verifiability.
- **Web3 Python Integration**:
  - `web3.py` used to connect to Sepolia, sign, and send transactions.
  - Nonce, gas, and gas price managed per transaction.

## How to Run

### 1. Setup PostgreSQL
```bash
# Start PostgreSQL terminal
psql -U postgres

# Create database
CREATE DATABASE audit_logs;

# Connect to DB
\c audit_logs

# Create table (if not exists)
CREATE TABLE IF NOT EXISTS secure_db (
    name TEXT PRIMARY KEY,
    role TEXT,
    salary TEXT
);
```

### 2. Install Python Dependencies
```bash
python -m pip install web3 psycopg2-binary pandas
```

### 3. Run the Blockchain Audit Script
```bash
python hash_blockchain.py
# Follow menu to add employees or verify integrity
```

### 4. Run CSV Export Script
```bash
python export_live_csv.py
# The script continuously exports DB to CSV at set intervals
```

### 5. Verify Blockchain Data
- Hashes are stored on Sepolia. Use `blockchain_client.py` functions:
  - `push_hash(name, hash)`: Push hash to blockchain
  - `fetch_hash(name)`: Fetch hash for verification

## Notes
- Only hashes are on blockchain; no raw sensitive data is exposed.
- Any tampering in DB (manual updates, SQL injection, etc.) will be detectable by integrity verification.

## Folder Structure
```
Blockchain-backed-Database-Audit-Logs/
├─ Database/
│  ├─ employees.sql
│  ├─ employees_live.csv
├─ blockchain_client.py
├─ check.py / hash_blockchain.py
├─ export_live_csv.py
├─ smart_contract.sol
├─ README.md
```
