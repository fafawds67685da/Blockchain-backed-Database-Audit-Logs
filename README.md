# Blockchain-Backed Database Audit Logs

## 📌 Project Overview

This project secures organizational data by integrating a traditional PostgreSQL database with blockchain immutability. Instead of storing sensitive data directly on-chain, cryptographic **hashes** of records are stored in a smart contract on Ethereum testnets (Ganache or Sepolia). This ensures:

* **Data Integrity:** Database entries can be verified against blockchain hashes.
* **Tamper Detection:** Any modification in the database can be detected.
* **Transparency:** Immutable records provide audit-ready evidence.

---

## 🏗 Architecture & Workflow

**1. PostgreSQL Database**

* Stores employee information (`secure_db` table) with fields: `name`, `role`, `salary`.
* Hashes are **not stored** in the database; they exist only on blockchain.

**2. Python Backend**

* `check.py` handles:

  * Adding new employees
  * Recomputing SHA-256 hash for each employee record
  * Verifying integrity by comparing DB hash with blockchain hash
* `blockchain_client.py` handles:

  * Connecting to blockchain (Ganache or Sepolia)
  * Pushing hashes to smart contract
  * Fetching hashes from smart contract
* `export_live_csv.py`:

  * Continuously exports DB content to a CSV (`employees_live.csv`)
  * Updates every 10 seconds to reflect live changes

**3. Smart Contract (`smart_contract.sol`)**

* Written in Solidity.
* Stores a mapping of `employeeName → recordHash`.
* Functions:

  * `addHash(name, recordHash)` → Adds or updates hash
  * `getHash(name)` → Retrieves hash for verification

**4. Workflow Summary**

1. Add a new employee via `check.py`.
2. Python recomputes the SHA-256 hash.
3. Hash is pushed to blockchain using `blockchain_client.py`.
4. Export script (`export_live_csv.py`) updates CSV dynamically from DB.
5. Data integrity can be verified by comparing DB hash with blockchain hash.

---

## 🗂 File Structure

```
Blockchain-backed-Database-Audit-Logs/
│
├─ Database/
│  ├─ employees.sql           # Table creation and sample updates
│  └─ employees_live.csv      # Dynamically generated CSV
│
├─ blockchain_client.py       # Connects to blockchain & handles hash push/fetch
├─ check.py                   # Main Python script for DB operations & verification
├─ export_live_csv.py         # Continuously exports DB table to CSV
├─ hash_blockchain.py         # Old blockchain test script (local Ganache)
├─ smart_contract.sol         # Solidity smart contract
├─ README.md                  # Project documentation
```

---

## ⚙ Installation & Setup

### 1. PostgreSQL Database

1. Open terminal or psql CLI.
2. Create database:

   ```sql
   CREATE DATABASE audit_logs;
   ```
3. Switch to database:

   ```sql
   \c audit_logs
   ```
4. Run the SQL script to create table:

   ```sql
   \i D:/Blockchain-backed-Database-Audit-Logs/Database/employees.sql
   ```
5. Confirm table creation:

   ```sql
   SELECT * FROM secure_db;
   ```

---

### 2. Python Dependencies

```bash
pip install psycopg2 pandas web3 eth-account
```

---

### 3. Run `export_live_csv.py`

Continuously exports the table contents to CSV dynamically:

```bash
python export_live_csv.py
```

* The CSV file will update every 10 seconds with the latest DB records.

---

### 4. Deploy Smart Contract

**Option 1: Ganache (local blockchain)**

* Run Ganache.
* Deploy `smart_contract.sol` using Remix IDE or Truffle.
* Copy contract address & ABI to `blockchain_client.py`.

**Option 2: Sepolia Testnet**

* Connect `blockchain_client.py` to Sepolia via Infura (update `INFURA_URL`, `ACCOUNT_ADDRESS`, `PRIVATE_KEY`).
* Deploy contract on Sepolia and use its address in `CONTRACT_ADDRESS`.

---

### 5. Add Employee & Verify

```bash
python check.py
```

* Interactive menu:

  1. Add new employee → automatically pushes hash to blockchain.
  2. Verify integrity → recomputes hash from DB and compares with blockchain hash.
  3. Exit.

---

### 6. Optional: Test `hash_blockchain.py` (Ganache Only)

```bash
python hash_blockchain.py
```

* Used to test blockchain operations locally.

---

## 🔗 How It Works End-to-End

1. User adds employee data in DB via `check.py`.
2. Backend computes SHA-256 hash of `(name + role + salary)`.
3. Hash is sent to Ethereum smart contract.
4. `export_live_csv.py` writes DB content into CSV.
5. Integrity checks recompute hash and compare with blockchain hash.
6. Alerts shown if hashes mismatch → tampering detected.

---

## 📝 Notes

* Ensure Ganache accounts have sufficient balance for gas.
* Always use the correct `ACCOUNT_ADDRESS` and `PRIVATE_KEY` for transactions.
* For live testing, Sepolia network requires small test ETH from Sepolia faucet.
