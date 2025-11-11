import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';

const GasFeeTracker = () => {
  const [gasStats, setGasStats] = useState(null);

  useEffect(() => {
    fetchGasStats();
  }, []);

  const fetchGasStats = async () => {
    try {
      const response = await apiService.getGasStats();
      setGasStats(response.data);
    } catch (error) {
      console.error('Failed to fetch gas stats');
    }
  };

  if (!gasStats) return <div className="flex justify-center items-center h-full"><div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div></div>;

  const ethPrice = 2000; // Approximate
  const costUSD = gasStats.estimated_cost_per_transaction.cost_eth * ethPrice;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">💰 Gas Fee Tracker</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 p-6 rounded-xl shadow-lg text-white">
          <p className="text-sm opacity-90">⛽ Current Gas Price</p>
          <p className="text-3xl font-bold mt-2">{gasStats.current_gas_price_gwei.toFixed(2)} Gwei</p>
        </div>

        <div className="bg-gradient-to-r from-green-500 to-green-600 p-6 rounded-xl shadow-lg text-white">
          <p className="text-sm opacity-90">💰 Cost per TX</p>
          <p className="text-3xl font-bold mt-2">{gasStats.estimated_cost_per_transaction.cost_eth.toFixed(6)} ETH</p>
        </div>

        <div className="bg-gradient-to-r from-purple-500 to-purple-600 p-6 rounded-xl shadow-lg text-white">
          <p className="text-sm opacity-90">💵 Cost (USD)</p>
          <p className="text-3xl font-bold mt-2">${costUSD.toFixed(4)}</p>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl shadow-lg">
        <h3 className="text-xl font-bold mb-4">📊 Transaction Cost Breakdown</h3>
        <div className="space-y-2 text-sm">
          <p><strong>Gas Used per Transaction:</strong> {gasStats.estimated_cost_per_transaction.gas_used.toLocaleString()}</p>
          <p><strong>Gas Price:</strong> {gasStats.current_gas_price_wei.toLocaleString()} Wei</p>
          <p><strong>Total Cost:</strong> {gasStats.estimated_cost_per_transaction.cost_wei.toLocaleString()} Wei</p>
        </div>
        <p className="text-xs text-gray-500 mt-4">ℹ️ Gas fees are estimated based on current network conditions</p>
      </div>
    </div>
  );
};

export default GasFeeTracker;
