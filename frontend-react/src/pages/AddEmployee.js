import React, { useState } from 'react';
import { apiService } from '../services/api';
import { toast } from 'react-toastify';

const AddEmployee = () => {
  const [formData, setFormData] = useState({ id: '', name: '', role: '', salary: '' });
  const [duplicateWarning, setDuplicateWarning] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setDuplicateWarning(null);
  };

  const checkDuplicate = async () => {
    if (!formData.name) return;
    try {
      const response = await apiService.checkDuplicateName(formData.name);
      if (response.data.exists) {
        setDuplicateWarning(response.data);
      }
    } catch (error) {
      console.error('Error checking duplicate:', error);
    }
  };

  const handleSubmit = async (e, forceDuplicate = false) => {
    e.preventDefault();
    
    if (!formData.id || !formData.name || !formData.role || !formData.salary) {
      toast.error('Please fill all fields including Employee ID');
      return;
    }

    // Validate ID is a positive number
    if (parseInt(formData.id) <= 0) {
      toast.error('Employee ID must be a positive number');
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.createEmployee({
        id: parseInt(formData.id),
        ...formData,
        force_duplicate: forceDuplicate
      });
      setResult(response.data);
      toast.success(`Employee ${formData.name} (ID: ${formData.id}) added successfully!`);
      setFormData({ id: '', name: '', role: '', salary: '' });
      setDuplicateWarning(null);
    } catch (error) {
      if (error.response?.status === 409) {
        if (error.response.data.detail.includes('ID')) {
          toast.error(error.response.data.detail);
        } else {
          await checkDuplicate();
        }
      } else {
        toast.error(error.response?.data?.detail || 'Failed to add employee');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">➕ Add New Employee</h1>

      <div className="bg-white p-8 rounded-xl shadow-lg">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🆔 Employee ID <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                name="id"
                value={formData.id}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Enter unique ID (e.g., 1001)"
                min="1"
                required
              />
              <p className="text-xs text-gray-500 mt-1">Enter a unique positive number</p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">👤 Employee Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                onBlur={checkDuplicate}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="John Doe"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">💼 Role/Position</label>
              <input
                type="text"
                name="role"
                value={formData.role}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Software Engineer"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">💰 Salary</label>
              <input
                type="number"
                name="salary"
                value={formData.salary}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="75000"
              />
            </div>
          </div>

          {duplicateWarning && (
            <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4">
              <p className="font-bold text-yellow-700">⚠️ Employee name '{formData.name}' already exists!</p>
              <ul className="mt-2 text-sm text-yellow-600">
                {duplicateWarning.employees.map(emp => (
                  <li key={emp.id}>ID {emp.id}: {emp.name} ({emp.role})</li>
                ))}
              </ul>
              <button
                type="button"
                onClick={(e) => handleSubmit(e, true)}
                className="mt-3 bg-yellow-600 text-white px-4 py-2 rounded hover:bg-yellow-700"
              >
                Continue Anyway (Force Duplicate)
              </button>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 disabled:opacity-50 font-semibold"
          >
            {loading ? 'Adding...' : '✅ Add Employee & Push to Blockchain'}
          </button>
        </form>

        {result && (
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-bold mb-2">Employee Details</h3>
              <pre className="text-sm">{JSON.stringify({ id: result.id, name: result.name, role: result.role, salary: result.salary }, null, 2)}</pre>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-bold mb-2">🔐 Blockchain Info</h3>
              <p className="text-sm break-all">Hash: {result.record_hash.substring(0, 32)}...</p>
              {result.tx_hash && result.tx_hash !== 'pending' && (
                <a href={`https://sepolia.etherscan.io/tx/${result.tx_hash}`} target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:underline text-sm">
                  View on Etherscan →
                </a>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AddEmployee;
