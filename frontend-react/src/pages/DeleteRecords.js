import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { toast } from 'react-toastify';

const DeleteRecords = () => {
  const [activeTab, setActiveTab] = useState('single');
  const [employees, setEmployees] = useState([]);
  const [deleteId, setDeleteId] = useState('');
  const [confirmText, setConfirmText] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      const response = await apiService.getAllEmployees();
      setEmployees(response.data);
    } catch (error) {
      console.error('Failed to fetch employees');
    }
  };

  const handleDeleteSingle = async () => {
    if (!deleteId) {
      toast.error('Please enter employee ID');
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.deleteEmployee(deleteId);
      toast.success(response.data.message);
      setDeleteId('');
      fetchEmployees();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to delete employee');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAll = async () => {
    if (confirmText !== 'DELETE ALL') {
      toast.error('Please type "DELETE ALL" to confirm');
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.deleteAllEmployees();
      toast.success(response.data.message);
      setConfirmText('');
      fetchEmployees();
    } catch (error) {
      toast.error('Failed to delete all employees');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">🗑️ Delete Employee Records</h1>
      
      <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4">
        <p className="font-bold text-yellow-700">⚠️ Warning: Deletion is permanent and cannot be undone!</p>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200">
        <button
          onClick={() => setActiveTab('single')}
          className={`px-6 py-3 font-medium ${activeTab === 'single' ? 'border-b-2 border-indigo-600 text-indigo-600' : 'text-gray-500'}`}
        >
          🗑️ Delete Single Record
        </button>
        <button
          onClick={() => setActiveTab('all')}
          className={`px-6 py-3 font-medium ${activeTab === 'all' ? 'border-b-2 border-red-600 text-red-600' : 'text-gray-500'}`}
        >
          ⚠️ Delete All Records
        </button>
      </div>

      {/* Single Delete */}
      {activeTab === 'single' && (
        <div className="space-y-6">
          {employees.length > 0 && (
            <div className="bg-white p-6 rounded-xl shadow-lg">
              <h3 className="font-bold mb-4">Current Employees</h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Role</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Salary</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {employees.map((emp) => (
                      <tr key={emp.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4">{emp.id}</td>
                        <td className="px-6 py-4 font-medium">{emp.name}</td>
                        <td className="px-6 py-4">{emp.role}</td>
                        <td className="px-6 py-4">${emp.salary}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <div className="bg-white p-6 rounded-xl shadow-lg">
            <label className="block text-sm font-medium text-gray-700 mb-2">Employee ID to Delete</label>
            <input
              type="number"
              value={deleteId}
              onChange={(e) => setDeleteId(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 mb-4"
              placeholder="Enter employee ID"
              min="1"
            />
            <button
              onClick={handleDeleteSingle}
              disabled={loading}
              className="w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 disabled:opacity-50 font-semibold"
            >
              {loading ? 'Deleting...' : '🗑️ Delete Employee'}
            </button>
          </div>
        </div>
      )}

      {/* Delete All */}
      {activeTab === 'all' && (
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <div className="bg-red-50 border-2 border-red-500 p-6 rounded-lg mb-6">
            <h3 className="text-xl font-bold text-red-700 mb-4">🚨 DANGER ZONE</h3>
            <p className="text-red-600 mb-2">This will delete ALL employee records permanently!</p>
            <ul className="list-disc list-inside text-sm text-red-600 space-y-1">
              <li>Delete all employee records from the database</li>
              <li>Reset the ID counter</li>
              <li>NOT remove blockchain hashes (they remain immutable)</li>
            </ul>
          </div>

          <label className="block text-sm font-medium text-gray-700 mb-2">
            Type <code className="bg-gray-200 px-2 py-1 rounded">DELETE ALL</code> to confirm:
          </label>
          <input
            type="text"
            value={confirmText}
            onChange={(e) => setConfirmText(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 mb-4"
            placeholder="DELETE ALL"
          />
          <button
            onClick={handleDeleteAll}
            disabled={loading || confirmText !== 'DELETE ALL'}
            className="w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 disabled:opacity-50 font-semibold"
          >
            {loading ? 'Deleting...' : '⚠️ DELETE ALL RECORDS'}
          </button>
        </div>
      )}
    </div>
  );
};

export default DeleteRecords;
