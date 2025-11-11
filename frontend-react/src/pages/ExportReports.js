import React from 'react';
import { apiService } from '../services/api';
import { toast } from 'react-toastify';
import { FaFileCsv, FaFilePdf } from 'react-icons/fa';

const ExportReports = () => {
  const handleExportCSV = async () => {
    try {
      const response = await apiService.exportCSV();
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `employees_${new Date().getTime()}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('✅ CSV exported successfully!');
    } catch (error) {
      toast.error('❌ Failed to export CSV');
    }
  };

  const handleExportPDF = async () => {
    try {
      const response = await apiService.exportPDF();
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `audit_report_${new Date().getTime()}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('✅ PDF exported successfully!');
    } catch (error) {
      toast.error('❌ Failed to export PDF');
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">📥 Export Audit Reports</h1>

      <p className="text-gray-600">Download comprehensive audit reports in various formats</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-8 rounded-xl shadow-lg text-center">
          <FaFileCsv className="text-6xl text-green-600 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">CSV Export</h3>
          <p className="text-sm text-gray-600 mb-6">Raw data export for analysis</p>
          <button
            onClick={handleExportCSV}
            className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 font-semibold"
          >
            📥 Download CSV
          </button>
        </div>

        <div className="bg-white p-8 rounded-xl shadow-lg text-center">
          <FaFilePdf className="text-6xl text-red-600 mx-auto mb-4" />
          <h3 className="text-xl font-bold mb-2">PDF Export</h3>
          <p className="text-sm text-gray-600 mb-6">Professional audit report</p>
          <button
            onClick={handleExportPDF}
            className="w-full bg-red-600 text-white py-3 rounded-lg hover:bg-red-700 font-semibold"
          >
            📥 Download PDF
          </button>
        </div>
      </div>
    </div>
  );
};

export default ExportReports;
