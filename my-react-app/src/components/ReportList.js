// src/components/ReportList.js
import React, { useState, useEffect } from 'react';
import ReportCard from './ReportCard';
import axios from 'axios'; // For HTTP requests

const ReportList = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/api/reports')  // Adjust the URL to match your backend
      .then((response) => {
        setReports(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching reports:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div className="report-list">
      {reports.length === 0 ? (
        <h2>No reports to show!!!!</h2>
      ) : (
        reports.map((report) => (
          <ReportCard key={report.id} report={report} />
        ))
      )}
    </div>
  );
};

export default ReportList;
