import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { toast } from 'react-toastify';

const SimulateTampering = () => {
  const [employees, setEmployees] = useState([]);
  const [formData, setFormData] = useState({
    employee_id: '',
    field: 'salary',
    new_value: ''
  });
  const [result, setResult] = useState(null);
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

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.employee_id || !formData.new_value) {
      toast.error('Please fill all fields');
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.tamperData({
        employee_id: parseInt(formData.employee_id),
        field: formData.field,
        new_value: formData.new_value
      });
      setResult(response.data);
      toast.success('Data tampered successfully (for demo)');
      fetchEmployees();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to tamper data');
    } finally {
      setLoading(false);
    }
  };

  const selectedEmployee = employees.find(e => e.id === parseInt(formData.employee_id));

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">⚠️ Simulate Data Tampering</h1>

      <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4">
        <p className="font-bold text-yellow-700">⚠️ This feature is for demonstration purposes only!</p>
        <p className="text-sm text-yellow-600 mt-2">Demonstrates tampering detection, email notifications, and blockchain immutability.</p>
      </div>

      {/* Employee List */}
      {employees.length > 0 && (
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="font-bold mb-4">Current Employees ({employees.length})</h3>
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

      {/* Tamper Form */}
      <div className="bg-white p-6 rounded-xl shadow-lg">
        <h3 className="text-xl font-bold mb-4">🔧 Tamper Employee Data</h3>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Employee ID</label>
              <input
                type="number"
                name="employee_id"
                value={formData.employee_id}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                min="1"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Field to Modify</label>
              <select
                name="field"
                value={formData.field}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              >
                <option value="salary">💰 Salary</option>
                <option value="name">👤 Name</option>
                <option value="role">💼 Role</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">New Value</label>
              <input
                type="text"
                name="new_value"
                value={formData.new_value}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter new value"
              />
            </div>
          </div>

          {selectedEmployee && (
            <div className="bg-blue-50 p-4 rounded-lg">
              <p className="font-bold mb-2">Current Values for ID {selectedEmployee.id}:</p>
              <div className="grid grid-cols-3 gap-4 text-sm">
                <p><strong>Name:</strong> {selectedEmployee.name}</p>
                <p><strong>Role:</strong> {selectedEmployee.role}</p>
                <p><strong>Salary:</strong> ${selectedEmployee.salary}</p>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 disabled:opacity-50 font-semibold"
          >
            {loading ? 'Tampering...' : '💥 Tamper Data (Demo)'}
          </button>
        </form>

        {result && (
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h4 className="font-bold mb-2">📝 Updated Record</h4>
              <pre className="text-sm">{JSON.stringify({ id: result.employee_id, name: result.name, role: result.role, salary: result.salary }, null, 2)}</pre>
            </div>
            <div className="bg-yellow-50 p-4 rounded-lg">
              <h4 className="font-bold mb-2">⚠️ Change Made</h4>
              <p className="text-sm"><strong>Field:</strong> {result.updated_field}</p>
              <p className="text-sm"><strong>New Value:</strong> {result.new_value}</p>
              <p className="text-sm text-blue-600 mt-3">📧 Go to "Verify Integrity" to detect tampering!</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SimulateTampering;
