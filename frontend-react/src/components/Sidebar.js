import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  FaHome, FaPlus, FaList, FaCheckCircle, FaSearch, 
  FaTrash, FaExclamationTriangle, FaLink, FaGasPump, 
  FaChartBar, FaFileDownload, FaBars 
} from 'react-icons/fa';

const Sidebar = ({ isOpen, setIsOpen, backendOnline }) => {
  const menuItems = [
    { path: '/', icon: FaHome, label: 'Dashboard' },
    { path: '/add-employee', icon: FaPlus, label: 'Add Employee' },
    { path: '/view-records', icon: FaList, label: 'View Records' },
    { path: '/verify-integrity', icon: FaCheckCircle, label: 'Verify Integrity' },
    { path: '/search-filter', icon: FaSearch, label: 'Search & Filter' },
    { path: '/delete-records', icon: FaTrash, label: 'Delete Records' },
    { path: '/simulate-tampering', icon: FaExclamationTriangle, label: 'Simulate Tampering' },
    { path: '/transaction-history', icon: FaLink, label: 'Transactions' },
    { path: '/gas-fee-tracker', icon: FaGasPump, label: 'Gas Tracker' },
    { path: '/analytics', icon: FaChartBar, label: 'Analytics' },
    { path: '/export-reports', icon: FaFileDownload, label: 'Export Reports' },
  ];

  return (
    <div className={`fixed left-0 top-0 h-full bg-gradient-to-b from-indigo-600 to-purple-700 text-white transition-all duration-300 ${isOpen ? 'w-64' : 'w-20'} shadow-2xl z-50`}>
      <div className="p-4 flex items-center justify-between border-b border-indigo-500">
        {isOpen && <h1 className="text-xl font-bold">🔒 Audit System</h1>}
        <button onClick={() => setIsOpen(!isOpen)} className="p-2 hover:bg-indigo-500 rounded">
          <FaBars />
        </button>
      </div>

      <nav className="mt-6">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center px-4 py-3 hover:bg-indigo-500 transition-colors ${
                isActive ? 'bg-indigo-700 border-l-4 border-white' : ''
              }`
            }
          >
            <item.icon className="text-xl" />
            {isOpen && <span className="ml-4">{item.label}</span>}
          </NavLink>
        ))}
      </nav>

      <div className="absolute bottom-0 w-full p-4 border-t border-indigo-500">
        <div className={`flex items-center ${isOpen ? 'justify-between' : 'justify-center'}`}>
          <div className={`h-3 w-3 rounded-full ${backendOnline ? 'bg-green-400' : 'bg-red-400'}`} />
          {isOpen && <span className="text-sm">{backendOnline ? 'Online' : 'Offline'}</span>}
        </div>
        {isOpen && <p className="text-xs mt-2 opacity-75">Sepolia Testnet</p>}
      </div>
    </div>
  );
};

export default Sidebar;
