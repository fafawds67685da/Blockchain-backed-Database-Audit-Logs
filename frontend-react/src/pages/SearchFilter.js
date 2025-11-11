import React, { useState } from 'react';
import { apiService } from '../services/api';
import { toast } from 'react-toastify';

const SearchFilter = () => {
  const [filters, setFilters] = useState({
    name: '',
    role: '',
    min_salary: '',
    max_salary: ''
  });
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSearched(true);

    const searchFilters = {};
    if (filters.name) searchFilters.name = filters.name;
    if (filters.role) searchFilters.role = filters.role;
    if (filters.min_salary) searchFilters.min_salary = parseFloat(filters.min_salary);
    if (filters.max_salary) searchFilters.max_salary = parseFloat(filters.max_salary);

    try {
      const response = await apiService.searchEmployees(searchFilters);
      setResults(response.data);
      toast.success(`Found ${response.data.length} record(s)`);
    } catch (error) {
      toast.error('Search failed');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">🔎 Search & Filter Employees</h1>

      <div className="bg-white p-6 rounded-xl shadow-lg">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">🔍 Search by Name</label>
              <input
                type="text"
                name="name"
                value={filters.name}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="John Doe"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">💼 Search by Role</label>
              <input
                type="text"
                name="role"
                value={filters.role}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="Engineer"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">💰 Min Salary</label>
              <input
                type="number"
                name="min_salary"
                value={filters.min_salary}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="50000"
                min="0"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">💰 Max Salary</label>
              <input
                type="number"
                name="max_salary"
                value={filters.max_salary}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="100000"
                min="0"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 disabled:opacity-50 font-semibold"
          >
            {loading ? 'Searching...' : '🔍 Search'}
          </button>
        </form>
      </div>

      {searched && (
        <div className="bg-white p-6 rounded-xl shadow-lg">
          {results.length > 0 ? (
            <>
              <p className="text-sm text-gray-600 mb-4">Found <strong>{results.length}</strong> matching record(s)</p>
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
                  <tbody className="bg-white divide-y divide-gray-200">
                    {results.map((emp) => (
                      <tr key={emp.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">{emp.id}</td>
                        <td className="px-6 py-4 whitespace-nowrap font-medium">{emp.name}</td>
                        <td className="px-6 py-4 whitespace-nowrap">{emp.role}</td>
                        <td className="px-6 py-4 whitespace-nowrap">${emp.salary}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          ) : (
            <p className="text-center text-gray-500 py-8">ℹ️ No matching records found</p>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchFilter;
