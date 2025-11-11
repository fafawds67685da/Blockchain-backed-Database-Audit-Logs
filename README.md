# 🔒 Blockchain-Backed Database Audit System

A comprehensive blockchain-powered audit trail system that ensures data integrity through Ethereum smart contracts, cryptographic hashing, and real-time tampering detection.

---

## 🌟 Features

### Core Functionality
- ✅ **Blockchain Integration** - Ethereum Sepolia testnet for immutable audit logs
- ✅ **Manual Employee ID Assignment** - Users control employee IDs for better organization
- ✅ **Real-time Tampering Detection** - Instant hash verification against blockchain
- ✅ **Email Notifications** - Automated alerts when data tampering is detected
- ✅ **Cloud Database** - Neon PostgreSQL for scalable, cloud-native storage
- ✅ **Modern React UI** - Beautiful, responsive frontend with Tailwind CSS
- ✅ **RESTful API** - FastAPI backend with comprehensive endpoints

### Advanced Features
- 🔐 **SHA-256 Cryptographic Hashing** - Secure data fingerprinting
- ⛓️ **Smart Contract V2** - Employee ID-based blockchain storage
- 📊 **Analytics Dashboard** - Real-time integrity monitoring and charts
- 🔍 **Search & Filter** - Advanced employee record filtering
- 📥 **Export Capabilities** - CSV and PDF report generation
- 💰 **Gas Fee Tracking** - Monitor Ethereum transaction costs
- 🗑️ **Secure Deletion** - Controlled data removal with confirmations
- ⚡ **Performance Optimization** - Blockchain hash caching (5-min TTL)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────┐
│   React Frontend (Port 3000)                │
│   - Tailwind CSS UI                         │
│   - Real-time Dashboard                     │
│   - Interactive Charts (Recharts)           │
│   - Toast Notifications                     │
└──────────────┬──────────────────────────────┘
               │ HTTP/REST API
               ▼
┌─────────────────────────────────────────────┐
│   FastAPI Backend (Port 8000)               │
│   - Async Processing                        │
│   - Background Tasks                        │
│   - Email Notifications (SMTP)              │
│   - Blockchain Client (Web3.py)             │
└──────┬────────────────┬─────────────────────┘
       │                │
       ▼                ▼
┌──────────────┐  ┌────────────────────────┐
│ Neon         │  │ Ethereum Sepolia       │
│ PostgreSQL   │  │ Smart Contract V2      │
│ (Cloud)      │  │ (Immutable Ledger)     │
└──────────────┘  └────────────────────────┘
```

---

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **PostgreSQL** (or Neon cloud account)
- **MetaMask** wallet
- **Ethereum Sepolia** test ETH
- **Gmail** account (for email alerts)

---

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/Blockchain-backed-Database-Audit-Logs.git
cd Blockchain-backed-Database-Audit-Logs
```

### 2. Environment Setup

Create `.env` file:
```properties
# Blockchain Configuration
INFURA_URL=https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID
PRIVATE_KEY=YOUR_METAMASK_PRIVATE_KEY
ACCOUNT_ADDRESS=YOUR_ETHEREUM_ADDRESS
CONTRACT_ADDRESS=YOUR_DEPLOYED_CONTRACT_ADDRESS

# Neon PostgreSQL Configuration
DB_NAME=neondb
DB_USER=neondb_owner
DB_PASSWORD=YOUR_NEON_PASSWORD
DB_HOST=YOUR_NEON_HOST
DB_PORT=5432

# Email Configuration
EMAIL_SENDER=your-email@gmail.com
EMAIL_PASSWORD=your-app-specific-password
EMAIL_RECIPIENT=admin@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

### 3. Deploy Smart Contract

1. Go to [Remix IDE](https://remix.ethereum.org)
2. Create `AuditLogV2.sol`:
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
3. Compile with Solidity 0.8.0+
4. Deploy to Sepolia testnet
5. Copy contract address to `.env`

### 4. Database Setup

Run database setup:
```bash
python setup_neon_database.py
```

Or manually create table:
```sql
CREATE TABLE secure_db (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT,
    salary TEXT,
    record_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_name ON secure_db(name);
CREATE INDEX idx_created_at ON secure_db(created_at);
```

### 5. Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend-react
npm install
```

### 6. Start Application

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend-react
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

---

## 📚 API Endpoints

### Employee Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/employees` | Get all employees |
| POST | `/employees` | Create new employee |
| GET | `/employees/{id}/verify` | Verify single employee |
| DELETE | `/employees/{id}` | Delete employee |
| POST | `/employees/search` | Search/filter employees |

### Verification
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/verify-all?limit=10` | Verify multiple employees |
| GET | `/dashboard-quick` | Fast dashboard (no blockchain) |

### Tampering Simulation
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tamper` | Simulate data tampering |

### Utilities
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/transactions` | Get blockchain transactions |
| GET | `/gas-stats` | Get current gas prices |
| GET | `/export/csv` | Export to CSV |
| GET | `/export/pdf` | Export to PDF |
| POST | `/cache/clear` | Clear blockchain cache |

---

## 🧪 Testing Workflow

### 1. Add Employee
```bash
curl -X POST "http://127.0.0.1:8000/employees" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1001,
    "name": "John Doe",
    "role": "Engineer",
    "salary": "75000"
  }'
```

### 2. Verify Integrity
```bash
curl "http://127.0.0.1:8000/employees/1001/verify"
```

### 3. Simulate Tampering
```bash
curl -X POST "http://127.0.0.1:8000/tamper" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1001,
    "field": "salary",
    "new_value": "999999"
  }'
```

### 4. Detect Tampering
```bash
curl "http://127.0.0.1:8000/employees/1001/verify"
# Should return is_tampered: true
```

---

## 🔐 Security Features

1. **Immutable Blockchain Storage** - Records can't be altered once on-chain
2. **Cryptographic Hashing (SHA-256)** - Secure data fingerprinting
3. **Triple Hash Verification** - Stored, Computed, Blockchain comparison
4. **Email Alerts** - Real-time tampering notifications
5. **SSL Database Connection** - Encrypted Neon PostgreSQL communication
6. **CORS Protection** - Configurable origin restrictions

---

## 📊 Performance Optimization

- **Blockchain Hash Caching** - 5-minute TTL reduces redundant calls
- **Async Background Tasks** - Non-blocking blockchain operations
- **Database Connection Pooling** - Efficient resource management
- **Limited Batch Verification** - Prevents timeout (default: 10 records)
- **Fast Dashboard Endpoint** - Instant load without blockchain calls

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Web3.py** - Ethereum blockchain interaction
- **Psycopg2** - PostgreSQL database adapter
- **FPDF** - PDF report generation
- **SMTP** - Email notifications

### Frontend
- **React 18** - UI framework
- **React Router v6** - Navigation
- **Axios** - HTTP client
- **Recharts** - Data visualization
- **Tailwind CSS** - Styling
- **React Toastify** - Notifications

### Infrastructure
- **Ethereum Sepolia** - Test blockchain network
- **Neon PostgreSQL** - Serverless cloud database
- **Infura** - Ethereum node provider
- **MetaMask** - Wallet integration

---

## 📁 Project Structure

```
Blockchain-backed-Database-Audit-Logs/
├── backend/
│   ├── main.py                 # FastAPI application
│   └── requirements.txt        # Python dependencies
├── frontend-react/
│   ├── src/
│   │   ├── components/
│   │   │   └── Sidebar.js      # Navigation sidebar
│   │   ├── pages/
│   │   │   ├── Dashboard.js
│   │   │   ├── AddEmployee.js
│   │   │   ├── ViewRecords.js
│   │   │   ├── VerifyIntegrity.js
│   │   │   ├── SimulateTampering.js
│   │   │   └── Analytics.js
│   │   ├── services/
│   │   │   └── api.js          # API client
│   │   └── App.js              # Main app component
│   └── package.json            # Node dependencies
├── blockchain_client.py        # Web3 blockchain interface
├── email_notifier.py          # SMTP email handler
├── contract_abi_v2.json       # Smart contract ABI
├── smart_contract_v2.sol      # Solidity source code
├── .env                       # Environment variables
└── README.md                  # This file
```

---

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is in use
python kill_port_8000.py

# Restart backend
cd backend
uvicorn main:app --reload
```

### Database Connection Fails
```bash
# Test connection
python test_neon_connection.py
```

### Blockchain Verification Timeout
```bash
# Clear cache
curl -X POST "http://127.0.0.1:8000/cache/clear"

# Reduce verification limit
curl "http://127.0.0.1:8000/verify-all?limit=5"
```

### Frontend Shows "Backend Not Responding"
1. Check backend is running on port 8000
2. Verify `API_BASE` in `frontend-react/src/services/api.js`
3. Hard refresh browser (Ctrl+Shift+R)

---

## 📈 Future Enhancements

- [ ] Role-based access control (RBAC)
- [ ] Multi-signature blockchain transactions
- [ ] IPFS integration for large file storage
- [ ] Automated testing suite (Jest/Pytest)
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Mobile app (React Native)
- [ ] Advanced analytics (ML-based anomaly detection)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Authors

- **Your Name** - Initial work - [YourGitHub](https://github.com/yourusername)

---

## 🙏 Acknowledgments

- **Ethereum Foundation** - Blockchain infrastructure
- **Neon** - Serverless PostgreSQL platform
- **Infura** - Ethereum node provider
- **Remix IDE** - Smart contract development
- **MetaMask** - Wallet integration

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/Blockchain-backed-Database-Audit-Logs/issues)
- **Email:** your-email@example.com
- **Documentation:** [Wiki](https://github.com/yourusername/Blockchain-backed-Database-Audit-Logs/wiki)

---

**⭐ If you find this project useful, please give it a star on GitHub!**

---

## 🔗 Useful Links

- [Ethereum Sepolia Faucet](https://sepoliafaucet.com)
- [Remix IDE](https://remix.ethereum.org)
- [Neon Console](https://console.neon.tech)
- [Infura Dashboard](https://infura.io/dashboard)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [React Documentation](https://react.dev)

---

**Built with ❤️ using Blockchain Technology**
