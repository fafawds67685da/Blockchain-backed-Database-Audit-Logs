import React, { useState } from 'react';
import { apiService } from '../services/api';
import { toast } from 'react-toastify';

const VerifyIntegrity = () => {
  const [activeTab, setActiveTab] = useState('single');
  const [employeeId, setEmployeeId] = useState('');
  const [singleResult, setSingleResult] = useState(null);
  const [batchResults, setBatchResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSingleVerify = async (e) => {
    e.preventDefault();
    if (!employeeId) {
      toast.error('Please enter employee ID');
      return;
    }

    setLoading(true);
    try {
      const response = await apiService.verifyEmployee(employeeId);
      setSingleResult(response.data);
      if (response.data.is_tampered) {
        toast.error('⚠️ Tampering detected! Email alert sent.');
      } else {
        toast.success('✅ Integrity verified!');
      }
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Employee not found');
    } finally {
      setLoading(false);
    }
  };

  const handleBatchVerify = async () => {
    setLoading(true);
    try {
      const response = await apiService.verifyAll();
      setBatchResults(response.data);
      if (response.data.tampered > 0) {
        toast.warning(`⚠️ ${response.data.tampered} tampered record(s) found!`);
      } else {
        toast.success('✅ All records verified!');
      }
    } catch (error) {
      toast.error('Failed to verify records');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">🔍 Verify Data Integrity</h1>

      {/* Tabs */}
      <div className="flex border-b border-gray-200">
        <button
          onClick={() => setActiveTab('single')}
          className={`px-6 py-3 font-medium ${activeTab === 'single' ? 'border-b-2 border-indigo-600 text-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
        >
          🔎 Single Verification
        </button>
        <button
          onClick={() => setActiveTab('batch')}
          className={`px-6 py-3 font-medium ${activeTab === 'batch' ? 'border-b-2 border-indigo-600 text-indigo-600' : 'text-gray-500 hover:text-gray-700'}`}
        >
          📊 Batch Verification
        </button>
      </div>

      {/* Single Verification */}
      {activeTab === 'single' && (
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <form onSubmit={handleSingleVerify} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Employee ID</label>
              <input
                type="number"
                value={employeeId}
                onChange={(e) => setEmployeeId(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter employee ID"
                min="1"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 disabled:opacity-50 font-semibold"
            >
              {loading ? 'Verifying...' : '🔍 Verify Integrity'}
            </button>
          </form>

          {singleResult && (
            <div className="mt-6">
              <div className={`p-6 rounded-lg ${singleResult.is_tampered ? 'bg-red-50 border-2 border-red-500' : 'bg-green-50 border-2 border-green-500'}`}>
                <h3 className="text-2xl font-bold mb-4">
                  {singleResult.is_tampered ? '⚠️ TAMPERING DETECTED!' : '✅ INTEGRITY VERIFIED'}
                </h3>
                {singleResult.is_tampered && (
                  <p className="text-red-700 mb-4">📧 Email alert has been sent to administrators!</p>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
                  <div>
                    <h4 className="font-bold mb-2">📄 Record Details</h4>
                    <div className="space-y-1 text-sm">
                      <p><strong>ID:</strong> {singleResult.id}</p>
                      <p><strong>Name:</strong> {singleResult.name}</p>
                      <p><strong>Role:</strong> {singleResult.role}</p>
                      <p><strong>Salary:</strong> ${singleResult.salary}</p>
                      <p><strong>Created:</strong> {new Date(singleResult.created_at).toLocaleString()}</p>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-bold mb-2">🔐 Hash Verification</h4>
                    <div className="space-y-2 text-xs">
                      <div>
                        <p className="text-gray-600">Stored Hash:</p>
                        <code className="block bg-gray-100 p-2 rounded break-all">{singleResult.stored_hash.substring(0, 32)}...</code>
                      </div>
                      <div>
                        <p className="text-gray-600">Computed Hash:</p>
                        <code className="block bg-gray-100 p-2 rounded break-all">{singleResult.computed_hash.substring(0, 32)}...</code>
                      </div>
                      <div>
                        <p className="text-gray-600">Blockchain Hash:</p>
                        <code className="block bg-gray-100 p-2 rounded break-all">{singleResult.blockchain_hash.substring(0, 32)}...</code>
                      </div>
                    </div>
                    {singleResult.stored_hash === singleResult.computed_hash && singleResult.computed_hash === singleResult.blockchain_hash ? (
                      <p className="mt-3 text-green-700 font-semibold">✅ All hashes match</p>
                    ) : (
                      <p className="mt-3 text-red-700 font-semibold">⚠️ Hash mismatch detected</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Batch Verification */}
      {activeTab === 'batch' && (
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <button
            onClick={handleBatchVerify}
            disabled={loading}
            className="w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 disabled:opacity-50 font-semibold mb-6"
          >
            {loading ? 'Verifying...' : '🔍 Verify All Employees'}
          </button>

          {batchResults && (
            <>
              <div className="grid grid-cols-3 gap-4 mb-6">
                <div className="bg-blue-50 p-4 rounded-lg text-center">
                  <p className="text-sm text-gray-600">Total</p>
                  <p className="text-2xl font-bold text-blue-600">{batchResults.total_records}</p>
                </div>
                <div className="bg-green-50 p-4 rounded-lg text-center">
                  <p className="text-sm text-gray-600">Verified</p>
                  <p className="text-2xl font-bold text-green-600">{batchResults.verified}</p>
                </div>
                <div className="bg-red-50 p-4 rounded-lg text-center">
                  <p className="text-sm text-gray-600">Tampered</p>
                  <p className="text-2xl font-bold text-red-600">{batchResults.tampered}</p>
                </div>
              </div>

              {batchResults.tampered > 0 && (
                <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
                  <p className="font-bold text-red-700">⚠️ {batchResults.tampered} tampered record(s) found!</p>
                  <p className="text-sm text-red-600">📧 Email alerts have been sent for all tampered records!</p>
                </div>
              )}

              <div className="space-y-2 max-h-96 overflow-y-auto">
                {batchResults.results.map((result) => (
                  <details key={result.id} className={`p-4 rounded-lg border ${result.is_tampered ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'}`}>
                    <summary className="cursor-pointer font-semibold">
                      {result.is_tampered ? '⚠️' : '✅'} {result.name} (ID: {result.id}) - {result.is_tampered ? 'TAMPERED' : 'VERIFIED'}
                    </summary>
                    <div className="mt-3 text-sm space-y-1">
                      <p><strong>Current Salary:</strong> ${result.salary}</p>
                      <p><strong>Stored Hash:</strong> <code>{result.stored_hash.substring(0, 40)}...</code></p>
                      <p><strong>Computed Hash:</strong> <code>{result.computed_hash.substring(0, 40)}...</code></p>
                      <p><strong>Blockchain Hash:</strong> <code>{result.blockchain_hash.substring(0, 40)}...</code></p>
                    </div>
                  </details>
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default VerifyIntegrity;
