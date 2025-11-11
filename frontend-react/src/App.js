import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import AddEmployee from './pages/AddEmployee';
import ViewRecords from './pages/ViewRecords';
import VerifyIntegrity from './pages/VerifyIntegrity';
import SearchFilter from './pages/SearchFilter';
import DeleteRecords from './pages/DeleteRecords';
import SimulateTampering from './pages/SimulateTampering';
import TransactionHistory from './pages/TransactionHistory';
import GasFeeTracker from './pages/GasFeeTracker';
import Analytics from './pages/Analytics';
import ExportReports from './pages/ExportReports';

import { apiService } from './services/api';

function App() {
  const [backendOnline, setBackendOnline] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    checkBackendHealth();
    const interval = setInterval(checkBackendHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkBackendHealth = async () => {
    try {
      await apiService.checkHealth();
      setBackendOnline(true);
    } catch (error) {
      setBackendOnline(false);
    }
  };

  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        <Sidebar isOpen={sidebarOpen} setIsOpen={setSidebarOpen} backendOnline={backendOnline} />
        
        <div className={`flex-1 flex flex-col overflow-hidden transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-20'}`}>
          <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/add-employee" element={<AddEmployee />} />
              <Route path="/view-records" element={<ViewRecords />} />
              <Route path="/verify-integrity" element={<VerifyIntegrity />} />
              <Route path="/search-filter" element={<SearchFilter />} />
              <Route path="/delete-records" element={<DeleteRecords />} />
              <Route path="/simulate-tampering" element={<SimulateTampering />} />
              <Route path="/transaction-history" element={<TransactionHistory />} />
              <Route path="/gas-fee-tracker" element={<GasFeeTracker />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/export-reports" element={<ExportReports />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>

        <ToastContainer position="top-right" autoClose={3000} />
      </div>
    </Router>
  );
}

export default App;
