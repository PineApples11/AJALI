// src/components/ReportCard.js
import React from 'react';
import { formatTimestamp } from '../utils/utils'; // Importing the utility

const ReportCard = ({ report }) => {
  return (
    <div className="report-card">
      <h2>{report.title}</h2>
      <p>{report.description}</p>
      <p><strong>Type:</strong> {report.type}</p>
      <p><strong>Status:</strong> {report.status}</p>
      <p><strong>Reported on:</strong> {formatTimestamp(report.timestamp)}</p>
      <p><strong>Location:</strong> Latitude {report.latitude}, Longitude {report.longitude}</p>
    </div>
  );
};

export default ReportCard;
