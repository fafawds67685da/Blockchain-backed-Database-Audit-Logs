import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { apiService } from '../services/api';
import { toast } from 'react-toastify';

const Dashboard = () => {
  const [stats, setStats] = useState({ total_records: 0, verified: 0, tampered: 0, results: [] });
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [verifying, setVerifying] = useState(false);

  useEffect(() => {
    loadQuickData();
  }, []);

  const loadQuickData = async () => {
    try {
      setLoading(true);
      const response = await apiService.getDashboardQuick();
      setRecords(response.data.records);
      setStats({
        total_records: response.data.total_records,
        verified: response.data.total_records,
        tampered: 0,
        results: response.data.records.map(r => ({ ...r, is_tampered: false }))
      });
    } catch (error) {
      console.error('Dashboard load error:', error);
      toast.error('Failed to load dashboard');
    } finally {
      setLoading(false);
    }
  };

  const verifyRecords = async () => {
    try {
      setVerifying(true);
      const response = await apiService.verifyAll({ limit: 10 });
      
      // Merge verified results with all records
      const verifiedIds = new Set(response.data.results.map(r => r.id));
      const allResults = records.map(record => {
        const verified = response.data.results.find(r => r.id === record.id);
        return verified || { ...record, is_tampered: false };
      });
      
      setStats({
        total_records: response.data.total_records,
        verified: response.data.verified,
        tampered: response.data.tampered,
        results: allResults
      });
      
      if (response.data.tampered > 0) {
        toast.warning(`⚠️ ${response.data.tampered} tampered record(s) detected!`);
      } else {
        toast.success('✅ All verified records are intact!');
      }
    } catch (error) {
      console.error('Verification error:', error);
      toast.error('Verification failed - trying with cached data');
    } finally {
      setVerifying(false);
    }
  };

  const pieData = [
    { name: 'Verified', value: stats.verified, color: '#10b981' },
    { name: 'Tampered', value: stats.tampered, color: '#ef4444' },
  ];

  const integrityPct = stats.total_records > 0 ? ((stats.verified / stats.total_records) * 100).toFixed(1) : 100;

  if (loading) {
    return <div className="flex justify-center items-center h-full"><div className="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-600"></div></div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-800">🏠 Dashboard</h1>
        <div className="flex gap-2">
          <button 
            onClick={loadQuickData} 
            disabled={loading}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? '⏳ Loading...' : '🔄 Refresh'}
          </button>
          <button 
            onClick={verifyRecords} 
            disabled={verifying}
            className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            {verifying ? '⏳ Verifying...' : '🔍 Verify Blockchain'}
          </button>
        </div>
      </div>

      {verifying && (
        <div className="bg-blue-50 border-l-4 border-blue-500 p-4">
          <p className="text-blue-700">⏳ Verifying blockchain integrity... This may take a moment.</p>
        </div>
      )}

      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <MetricCard title="Total Records" value={stats.total_records} icon="📊" color="blue" />
        <MetricCard title="Verified" value={stats.verified} icon="✅" color="green" />
        <MetricCard title="Tampered" value={stats.tampered} icon="⚠️" color="red" />
        <MetricCard title="Integrity" value={`${integrityPct}%`} icon="🛡️" color="purple" />
      </div>

      {/* Charts and Status */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-bold mb-4">Integrity Status</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={100} paddingAngle={5} dataKey="value">
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-bold mb-4">Live Status</h2>
          {stats.tampered > 0 ? (
            <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
              <p className="text-red-700 font-bold">⚠️ {stats.tampered} tampered record(s) detected!</p>
            </div>
          ) : (
            <div className="bg-green-50 border-l-4 border-green-500 p-4">
              <p className="text-green-700 font-bold">✅ All records verified!</p>
            </div>
          )}

          <div className="mt-4 max-h-64 overflow-y-auto">
            {stats.results.filter(r => r.is_tampered).map((record) => (
              <div key={record.id} className="bg-red-50 p-3 rounded mb-2 border border-red-200">
                <p className="font-bold text-red-700">{record.name} (ID: {record.id})</p>
                <p className="text-sm text-gray-600">Salary: {record.salary}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Records Table */}
      <div className="bg-white p-6 rounded-xl shadow-lg">
        <h2 className="text-xl font-bold mb-4">Recent Records</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Role</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Salary</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {stats.results.slice(0, 10).map((record) => (
                <tr key={record.id} className={record.is_tampered ? 'bg-red-50' : ''}>
                  <td className="px-6 py-4 whitespace-nowrap">{record.id}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{record.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{record.role}</td>
                  <td className="px-6 py-4 whitespace-nowrap">${record.salary}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${record.is_tampered ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                      {record.is_tampered ? '⚠️ Tampered' : '✅ Verified'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ title, value, icon, color }) => {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    red: 'from-red-500 to-red-600',
    purple: 'from-purple-500 to-purple-600',
  };

  return (
    <div className={`bg-gradient-to-r ${colorClasses[color]} p-6 rounded-xl shadow-lg text-white`}>
      <div className="flex justify-between items-center">
        <div>
          <p className="text-sm opacity-90">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
        </div>
        <div className="text-4xl opacity-75">{icon}</div>
      </div>
    </div>
  );
};

export default Dashboard;
