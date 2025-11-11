import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { FaExternalLinkAlt } from 'react-icons/fa';

const TransactionHistory = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const response = await apiService.getTransactions();
      setTransactions(response.data.transactions);
    } catch (error) {
      console.error('Failed to fetch transactions');
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">⛓️ Blockchain Transaction History</h1>

      <div className="bg-white p-6 rounded-xl shadow-lg">
        <p className="text-sm text-gray-600 mb-4">Total Transactions: <strong>{transactions.length}</strong></p>

        {transactions.length > 0 ? (
          <div className="space-y-3">
            {transactions.reverse().map((tx, index) => (
              <details key={index} className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                <summary className="cursor-pointer font-semibold">
                  🔗 {tx.employee_name} - {tx.timestamp?.substring(0, 19)}
                </summary>
                <div className="mt-3 grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <p><strong>Employee:</strong> {tx.employee_name}</p>
                    <p><strong>ID:</strong> {tx.employee_id}</p>
                    <p><strong>Timestamp:</strong> {tx.timestamp}</p>
                  </div>
                  <div>
                    <p><strong>Record Hash:</strong></p>
                    <code className="block bg-white p-2 rounded text-xs break-all">{tx.record_hash?.substring(0, 32)}...</code>
                    {tx.etherscan_link && (
                      <a href={tx.etherscan_link} target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:underline mt-2 inline-flex items-center gap-1">
                        View on Etherscan <FaExternalLinkAlt size={12} />
                      </a>
                    )}
                  </div>
                </div>
              </details>
            ))}
          </div>
        ) : (
          <p className="text-center text-gray-500 py-8">ℹ️ No transactions yet</p>
        )}
      </div>
    </div>
  );
};

export default TransactionHistory;
