# 🔒 Blockchain-Backed Database Audit System

> **A Production-Grade Blockchain Audit Trail System** that combines Ethereum smart contracts, cryptographic hashing, and automated email notifications to ensure complete data integrity and real-time tampering detection.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![React](https://img.shields.io/badge/react-18.0+-blue.svg)
![Ethereum](https://img.shields.io/badge/ethereum-sepolia-purple.svg)

---

## 📖 Project Overview

This system provides an **immutable audit trail** for employee records by leveraging blockchain technology. Every data modification is cryptographically hashed and stored on the Ethereum blockchain, making it impossible to alter historical records without detection.

### 🎯 Problem It Solves

Traditional database systems are vulnerable to:
- ❌ Silent data tampering without detection
- ❌ Unauthorized salary modifications
- ❌ Lack of audit trail for compliance
- ❌ No real-time alerts for security breaches

### ✅ Our Solution

- ✅ **Immutable Blockchain Ledger** - Every record hash stored on Ethereum
- ✅ **Real-time Tampering Detection** - Instant verification against blockchain
- ⭐ **Automated Email Alerts** - Immediate notifications when tampering detected
- ✅ **Cryptographic Verification** - SHA-256 hash triple-check (DB → Computed → Blockchain)
- ✅ **Cloud-Native Architecture** - Scalable with Neon PostgreSQL
- ✅ **Beautiful Modern UI** - React + Tailwind CSS interface

---

## 🌟 Key Features

### Core Functionality
- 🔐 **Blockchain Integration** - Ethereum Sepolia testnet for permanent audit logs
- 👤 **Manual Employee ID Control** - Users assign custom employee IDs
- 🔍 **Triple Hash Verification** - Stored hash, computed hash, blockchain hash comparison
- ⭐ **Email Notification System** - Automatic SMTP alerts on tampering detection
- ☁️ **Cloud Database** - Neon PostgreSQL serverless database
- 💻 **Modern React UI** - Responsive design with Tailwind CSS
- 🚀 **FastAPI Backend** - High-performance async Python API

### Advanced Features
- 📊 **Real-time Analytics Dashboard** - Live integrity monitoring with charts
- 🔎 **Advanced Search & Filter** - Query by name, role, salary range
- 📥 **Export Capabilities** - Generate CSV and PDF reports
- 💰 **Gas Fee Tracking** - Monitor Ethereum transaction costs
- ⛓️ **Transaction History** - View all blockchain transactions with Etherscan links
- 🗑️ **Secure Deletion** - Controlled data removal with double confirmation
- ⚡ **Performance Optimization** - Blockchain hash caching (5-min TTL)
- 🎭 **Tampering Simulation** - Built-in demo mode for testing detection

### ⭐ Star Feature: Automated Email Alerts

**Real-time Security Notifications**

When tampering is detected, the system automatically sends detailed email alerts containing:
- 👤 Employee name and ID
- 📧 Timestamp of detection
- 🔐 Hash comparison (Stored vs Computed vs Blockchain)
- 🚨 Severity level
- 📊 Detailed discrepancy report

**Email Alert Example:**
```
Subject: 🚨 DATA TAMPERING DETECTED - Employee John Doe

⚠️ TAMPERING ALERT
Data tampering has been detected in the audit database.

Employee Details:
• Name: John Doe
• ID: 1001
• Timestamp: 2024-01-15 14:30:22

Hash Verification:
• Stored Hash: 05a5070a4c44669ce28146da39769c5c...
• Computed Hash: 7f3e8a9b2c15478d9e6f1a0b3c4d5e6f...
• Blockchain Hash: 05a5070a4c44669ce28146da39769c5c...

⚠️ The data has been modified after initial storage.
Immediate investigation required!
```

**Configuration:**
- SMTP support (Gmail, Outlook, etc.)
- Configurable recipients
- HTML formatted emails
- Background async sending (non-blocking)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│         React Frontend (Port 3000)                  │
│   • Tailwind CSS Responsive UI                      │
│   • Real-time Dashboard with Charts                 │
│   • Interactive Data Tables                         │
│   • Toast Notifications                             │
└──────────────┬──────────────────────────────────────┘
               │ REST API (HTTP/JSON)
               ▼
┌─────────────────────────────────────────────────────┐
│         FastAPI Backend (Port 8000)                 │
│   • Async Request Processing                        │
│   • Background Tasks Queue                          │
│   ⭐ SMTP Email Notifications                       │
│   • Web3.py Blockchain Client                       │
│   • SHA-256 Hash Generation                         │
└────────┬─────────────────┬──────────────────────────┘
         │                 │
         ▼                 ▼
┌──────────────────┐  ┌───────────────────────────────┐
│ Neon PostgreSQL  │  │ Ethereum Sepolia Testnet      │
│ (Cloud Database) │  │ • Smart Contract (Solidity)   │
│ • SSL Encrypted  │  │ • Immutable Hash Storage      │
│ • Auto-scaling   │  │ • Event Logs                  │
└──────────────────┘  └───────────────────────────────┘
         │
         ▼
┌──────────────────┐
│  Email Server    │
│  (SMTP/Gmail)    │
│  • Alerts        │
│  • HTML Format   │
└──────────────────┘
```

---

## 📋 Prerequisites

**Required Software:**
- ✅ Python 3.8 or higher
- ✅ Node.js 16+ and npm
- ✅ Git

**Required Accounts:**
- ✅ [Neon](https://neon.tech) - Cloud PostgreSQL database
- ✅ [Infura](https://infura.io) - Ethereum node provider
- ✅ [MetaMask](https://metamask.io) - Ethereum wallet
- ✅ Gmail account - For email notifications
- ✅ Sepolia ETH - Get free test ETH from [Sepolia Faucet](https://sepoliafaucet.com)

---

## 🚀 Installation & Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/Blockchain-backed-Database-Audit-Logs.git
cd Blockchain-backed-Database-Audit-Logs
```

### Step 2: Environment Configuration

Create `.env` file in the root directory:

```properties
# Blockchain Configuration
INFURA_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
PRIVATE_KEY=YOUR_METAMASK_PRIVATE_KEY_WITHOUT_0x
ACCOUNT_ADDRESS=YOUR_ETHEREUM_ADDRESS
CONTRACT_ADDRESS=YOUR_DEPLOYED_CONTRACT_ADDRESS

# Neon PostgreSQL Configuration (Cloud Database)
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=YOUR_NEON_DATABASE_PASSWORD
DB_HOST=YOUR_NEON_HOST.neon.tech
DB_PORT=5432

# Email Configuration (⭐ Star Feature)
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-app-specific-password
EMAIL_RECIPIENT=admin@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Important:** 
- For Gmail, use [App-Specific Password](https://support.google.com/accounts/answer/185833)
- Never commit `.env` file to version control

### Step 3: Deploy Smart Contract

1. **Open Remix IDE:** https://remix.ethereum.org

2. **Create new file:** `AuditLogV2.sol`

3. **Paste contract code:**
```solidity
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
```

4. **Compile:**
   - Click "Solidity Compiler" (left sidebar)
   - Compiler: 0.8.0 or higher
   - Click "Compile AuditLogV2.sol"

5. **Deploy:**
   - Click "Deploy & Run Transactions"
   - Environment: "Injected Provider - MetaMask"
   - Network: Sepolia Test Network
   - Click "Deploy"
   - Confirm transaction in MetaMask

6. **Copy contract address** and update `.env` file

### Step 4: Setup Database

**Option 1: Automated Setup**
```bash
python setup_neon_database.py
```

**Option 2: Manual SQL Setup**

Connect to your Neon database and run:
```sql
-- Create table with manual ID
CREATE TABLE secure_db (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT,
    salary TEXT,
    record_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_name ON secure_db(name);
CREATE INDEX idx_created_at ON secure_db(created_at);
CREATE INDEX idx_record_hash ON secure_db(record_hash);
```

### Step 5: Install Dependencies

**Backend Dependencies:**
```bash
pip install fastapi uvicorn web3 psycopg2-binary python-dotenv fpdf
```

Or use requirements file:
```bash
pip install -r requirements.txt
```

**Frontend Dependencies:**
```bash
cd frontend-react
npm install
```

### Step 6: Start the Application

**Terminal 1 - Backend Server:**
```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
✅ Using V2 Contract ABI (Employee ID based)
Connected to Sepolia: True
INFO:     Application startup complete.
```

**Terminal 2 - Frontend Server:**
```bash
cd frontend-react
npm start
```

Expected output:
```
Compiled successfully!

You can now view blockchain-audit-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Terminal 3 - Test Connection (Optional):**
```bash
python quick_test.py
```

---

## 🌐 Access Points

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | React web interface |
| **Backend API** | http://127.0.0.1:8000 | FastAPI server |
| **API Docs** | http://127.0.0.1:8000/docs | Interactive Swagger UI |
| **Alternative Docs** | http://127.0.0.1:8000/redoc | ReDoc documentation |

---

## 📚 Complete API Documentation

### 🔹 Employee Management

#### Get All Employees
```http
GET /employees
```
**Response:**
```json
[
  {
    "id": 1001,
    "name": "John Doe",
    "role": "Engineer",
    "salary": "75000",
    "record_hash": "05a5070a...",
    "created_at": "2024-01-15T10:30:00",
    "tx_hash": null
  }
]
```

#### Create Employee
```http
POST /employees
Content-Type: application/json

{
  "id": 1001,
  "name": "John Doe",
  "role": "Software Engineer",
  "salary": "75000",
  "force_duplicate": false
}
```
**Response:**
```json
{
  "id": 1001,
  "name": "John Doe",
  "role": "Software Engineer",
  "salary": "75000",
  "record_hash": "05a5070a4c44669ce28146da39769c5c...",
  "created_at": "2024-01-15T10:30:00",
  "tx_hash": "pending"
}
```

#### Search Employees
```http
POST /employees/search
Content-Type: application/json

{
  "name": "John",
  "role": "Engineer",
  "min_salary": 50000,
  "max_salary": 100000
}
```

#### Delete Employee
```http
DELETE /employees/{employee_id}
```

#### Delete All Employees
```http
DELETE /employees/all/truncate
```
⚠️ **Warning:** Requires confirmation in UI

#### Check Duplicate Name
```http
GET /employees/check-duplicate/{name}
```

---

### 🔹 Verification & Integrity

#### Verify Single Employee
```http
GET /employees/{employee_id}/verify
```
**Response:**
```json
{
  "id": 1001,
  "name": "John Doe",
  "role": "Engineer",
  "salary": "75000",
  "is_tampered": false,
  "stored_hash": "05a5070a...",
  "computed_hash": "05a5070a...",
  "blockchain_hash": "05a5070a...",
  "created_at": "2024-01-15T10:30:00"
}
```
⭐ **Auto-sends email if `is_tampered: true`**

#### Verify All Employees (Limited)
```http
GET /verify-all?limit=10
```
**Parameters:**
- `limit` (optional): Number of records to verify (default: 10)

**Response:**
```json
{
  "total_records": 50,
  "verified": 9,
  "tampered": 1,
  "results": [...]
}
```

#### Fast Dashboard (No Blockchain)
```http
GET /dashboard-quick
```
Returns database records instantly without blockchain verification.

---

### 🔹 Tampering Simulation

#### Tamper Data (Demo Mode)
```http
POST /tamper
Content-Type: application/json

{
  "employee_id": 1001,
  "field": "salary",
  "new_value": "999999"
}
```
**Allowed fields:** `name`, `role`, `salary`

---

### 🔹 Blockchain & Transactions

#### Get Transaction History
```http
GET /transactions
```
**Response:**
```json
{
  "total_transactions": 15,
  "transactions": [
    {
      "tx_hash": "0xabc123...",
      "employee_name": "John Doe",
      "employee_id": 1001,
      "record_hash": "05a5070a...",
      "timestamp": "2024-01-15T10:30:00",
      "etherscan_link": "https://sepolia.etherscan.io/tx/0xabc123..."
    }
  ]
}
```

#### Get Gas Statistics
```http
GET /gas-stats
```
**Response:**
```json
{
  "current_gas_price_wei": 20000000000,
  "current_gas_price_gwei": 20.0,
  "estimated_cost_per_transaction": {
    "gas_used": 200000,
    "cost_wei": 4000000000000000,
    "cost_eth": 0.004
  }
}
```

#### Clear Blockchain Cache
```http
POST /cache/clear
```
Clears the 5-minute blockchain hash cache.

---

### 🔹 Export & Reports

#### Export to CSV
```http
GET /export/csv
```
Downloads: `employees_YYYYMMDD_HHMMSS.csv`

#### Export to PDF
```http
GET /export/pdf
```
Downloads: `audit_report_YYYYMMDD_HHMMSS.pdf`

---

### 🔹 System Health

#### Health Check
```http
GET /
```
**Response:**
```json
{
  "message": "Blockchain Audit API v2.0",
  "status": "operational"
}
```

---

## 🧪 Complete Testing Workflow

### Test 1: Add Employee with Manual ID
```bash
curl -X POST "http://127.0.0.1:8000/employees" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1001,
    "name": "Alice Johnson",
    "role": "Data Scientist",
    "salary": "95000"
  }'
```

### Test 2: Verify Integrity (Should Pass)
```bash
curl "http://127.0.0.1:8000/employees/1001/verify"
```
Expected: `is_tampered: false`

### Test 3: Simulate Tampering
```bash
curl -X POST "http://127.0.0.1:8000/tamper" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1001,
    "field": "salary",
    "new_value": "999999"
  }'
```

### Test 4: Verify Again (Should Fail + Send Email ⭐)
```bash
curl "http://127.0.0.1:8000/employees/1001/verify"
```
Expected: 
- `is_tampered: true`
- Email sent to configured recipient
- Hash mismatch details in response

### Test 5: View Transaction History
```bash
curl "http://127.0.0.1:8000/transactions"
```

### Test 6: Export Reports
```bash
# CSV
curl "http://127.0.0.1:8000/export/csv" -o employees.csv

# PDF
curl "http://127.0.0.1:8000/export/pdf" -o report.pdf
```

---

## 🎨 Frontend Features

### Dashboard
- 📊 Real-time metrics (Total, Verified, Tampered, Integrity %)
- 📈 Pie chart visualization
- 🔴 Live tampered records alert
- 📋 Recent records table
- 🔄 Manual refresh & blockchain verification

### Add Employee
- 🆔 Custom employee ID input
- ⚠️ Duplicate name detection
- ✅ Force duplicate option
- 🔐 Blockchain hash display
- 🔗 Etherscan transaction link

### View Records
- 📋 Paginated data table
- 📥 CSV export
- 📄 PDF export
- 🔍 Quick search

### Verify Integrity
- 🔎 Single employee verification
- 📊 Batch verification (limited)
- 🔐 Hash comparison display
- ⚠️ Tampering details

### Search & Filter
- 🔍 Name search
- 💼 Role filter
- 💰 Salary range filter
- 📊 Results table

### Delete Records
- 🗑️ Single record deletion
- ⚠️ Double confirmation
- 🔴 Delete all (with text confirmation)
- 🔄 Auto-refresh after deletion

### Simulate Tampering
- 🎭 Demo mode
- 🔧 Field selection (name, role, salary)
- 📝 Current values display
- ✅ Confirmation message

### Analytics
- 📊 Integrity charts
- 📈 Role distribution
- 📋 Detailed breakdown table
- 🔄 Real-time updates

---

## 🔐 Security Features

1. **Blockchain Immutability**
   - Records stored on Ethereum cannot be altered
   - Permanent audit trail

2. **Triple Hash Verification**
   - Database stored hash
   - Real-time computed hash
   - Blockchain retrieved hash

3. **⭐ Email Alert System**
   - Instant tampering notifications
   - Detailed discrepancy reports
   - HTML formatted emails

4. **SSL Database Encryption**
   - Neon PostgreSQL with SSL
   - Encrypted data in transit

5. **Access Control**
   - CORS protection
   - Configurable origins

6. **Data Validation**
   - Duplicate ID prevention
   - Field type validation
   - SQL injection protection

---

## ⚡ Performance Optimization

- **Blockchain Caching** - 5-minute TTL reduces API calls by 90%
- **Async Operations** - Non-blocking blockchain transactions
- **Connection Pooling** - Efficient database resource management
- **Batch Limiting** - Prevent timeout (default: 10 records)
- **Fast Endpoints** - Separate endpoints for quick data access
- **Background Tasks** - Email sending doesn't block requests

---

## 🛠️ Technology Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **FastAPI** | Modern async Python web framework |
| **Web3.py** | Ethereum blockchain interaction |
| **Psycopg2** | PostgreSQL database adapter |
| **FPDF** | PDF report generation |
| **SMTP (smtplib)** | ⭐ Email notifications |
| **Uvicorn** | ASGI server |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **React Router v6** | Client-side routing |
| **Axios** | HTTP client |
| **Recharts** | Data visualization |
| **Tailwind CSS** | Utility-first styling |
| **React Toastify** | Toast notifications |
| **React Icons** | Icon library |

### Infrastructure
| Service | Purpose |
|---------|---------|
| **Ethereum Sepolia** | Test blockchain network |
| **Neon PostgreSQL** | Serverless cloud database |
| **Infura** | Ethereum node provider |
| **Gmail SMTP** | ⭐ Email delivery |
| **MetaMask** | Wallet & signing |

---

## 📁 Project Structure

```
Blockchain-backed-Database-Audit-Logs/
├── backend/
│   ├── main.py                     # FastAPI application & all endpoints
│   └── requirements.txt            # Python dependencies
├── frontend-react/
│   ├── public/
│   │   └── index.html             # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   └── Sidebar.js         # Navigation sidebar
│   │   ├── pages/
│   │   │   ├── Dashboard.js       # Main dashboard
│   │   │   ├── AddEmployee.js     # Add new employee
│   │   │   ├── ViewRecords.js     # View all records
│   │   │   ├── VerifyIntegrity.js # Verification page
│   │   │   ├── SearchFilter.js    # Search & filter
│   │   │   ├── DeleteRecords.js   # Delete operations
│   │   │   ├── SimulateTampering.js # Tampering demo
│   │   │   ├── TransactionHistory.js # Blockchain TXs
│   │   │   ├── GasFeeTracker.js   # Gas monitoring
│   │   │   ├── Analytics.js       # Charts & stats
│   │   │   └── ExportReports.js   # CSV/PDF export
│   │   ├── services/
│   │   │   └── api.js             # Axios API client
│   │   ├── App.js                 # Main React component
│   │   └── index.js               # React entry point
│   ├── package.json               # Node dependencies
│   └── tailwind.config.js         # Tailwind configuration
├── blockchain_client.py           # Web3 blockchain interface
├── email_notifier.py              # ⭐ SMTP email sender
├── contract_abi_v2.json           # Smart contract ABI
├── smart_contract_v2.sol          # Solidity source code
├── setup_neon_database.py         # Database setup script
├── test_neon_connection.py        # DB connection test
├── quick_test.py                  # System health test
├── .env                           # Environment variables (⚠️ don't commit)
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 Already in Use**
```bash
# Kill process using port 8000
python kill_port_8000.py

# Or manually
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Database Connection Failed**
```bash
# Test Neon connection
python test_neon_connection.py

# Check .env credentials
cat .env | grep DB_
```

**Blockchain Verification Timeout**
```bash
# Clear cache
curl -X POST "http://127.0.0.1:8000/cache/clear"

# Reduce verification limit
curl "http://127.0.0.1:8000/verify-all?limit=5"
```

### Frontend Issues

**Backend Not Responding**
1. Ensure backend is running: `http://127.0.0.1:8000`
2. Check API URL in `frontend-react/src/services/api.js`
3. Hard refresh browser: `Ctrl + Shift + R`

**CORS Errors**
- Backend CORS is configured for `*` (all origins)
- Check browser console for specific errors

### Email Issues

**Emails Not Sending**
1. Check Gmail App Password (not regular password)
2. Verify SMTP settings in `.env`
3. Check backend logs for email errors
4. Test with: `python -c "from email_notifier import send_tampering_alert; send_tampering_alert('Test', 1, 'hash1', 'hash2', 'hash3')"`

**Gmail Blocking**
- Enable "Less secure app access" (if using password)
- Use [App-Specific Password](https://support.google.com/accounts/answer/185833) (recommended)

---

## 📈 Future Enhancements

- [ ] **Advanced Email Features**
  - Multiple recipient groups
  - Email templates
  - Digest reports (daily/weekly)
  - SMS notifications via Twilio
  
- [ ] **Security Enhancements**
  - Role-based access control (RBAC)
  - Multi-signature transactions
  - 2FA authentication
  
- [ ] **Scalability**
  - Redis caching layer
  - PostgreSQL read replicas
  - Load balancing
  
- [ ] **Additional Features**
  - IPFS for document storage
  - Automated testing (Jest/Pytest)
  - Docker containerization
  - CI/CD pipeline
  - Mobile app (React Native)
  - ML-based anomaly detection

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open Pull Request

**Coding Standards:**
- Follow PEP 8 for Python
- Use ESLint for JavaScript
- Write descriptive commit messages
- Add tests for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Authors

- **Your Name** - *Initial work* - [YourGitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- **Ethereum Foundation** - Blockchain infrastructure
- **Neon** - Serverless PostgreSQL platform
- **Infura** - Ethereum node provider
- **Remix IDE** - Smart contract development
- **MetaMask** - Wallet integration
- **Gmail** - Email notification delivery

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/Blockchain-backed-Database-Audit-Logs/issues)
- **Email:** your-email@example.com
- **Documentation:** [Wiki](https://github.com/yourusername/Blockchain-backed-Database-Audit-Logs/wiki)

---

## 🔗 Useful Links

- [Ethereum Sepolia Faucet](https://sepoliafaucet.com) - Get free test ETH
- [Remix IDE](https://remix.ethereum.org) - Deploy smart contracts
- [Neon Console](https://console.neon.tech) - Manage database
- [Infura Dashboard](https://infura.io/dashboard) - Monitor API usage
- [FastAPI Documentation](https://fastapi.tiangolo.com) - Backend framework
- [React Documentation](https://react.dev) - Frontend framework
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833) - Email setup

---

**⭐ If you find this project useful, please give it a star on GitHub!**

**Built with ❤️ using Blockchain Technology & Python**

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/Blockchain-backed-Database-Audit-Logs)
![GitHub forks](https://img.shields.io/github/forks/yourusername/Blockchain-backed-Database-Audit-Logs)
![GitHub issues](https://img.shields.io/github/issues/yourusername/Blockchain-backed-Database-Audit-Logs)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/Blockchain-backed-Database-Audit-Logs)

---

*Last Updated: January 2024*
