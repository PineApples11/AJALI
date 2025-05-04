import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext'; // Assumes Member 1 created this
import ReportCard from '../components/ReportCard'; // Assumes Member 3 created this

const AdminDashboard = () => {
  const { user } = useAuth();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const res = await fetch('http://localhost:5000/api/reports', {
          method: 'GET',
          credentials: 'include', // important for sessions
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${user?.accessToken}`, // if token-based auth
          },
        });

        if (!res.ok) {
          throw new Error('Failed to fetch reports');
        }

        const data = await res.json();
        setReports(data);
      } catch (err) {
        console.error(err);
        setError('Something went wrong while loading reports.');
      } finally {
        setLoading(false);
      }
    };

    if (user?.role === 'admin') {
      fetchReports();
    }
  }, [user]);

  if (loading) return <p className="p-4">Loading reports...</p>;
  if (error) return <p className="p-4 text-red-500">{error}</p>;

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-3xl font-semibold mb-6">Admin Dashboard</h1>

      {reports.length === 0 ? (
        <p className="text-gray-600">No incident reports available.</p>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {reports.map((report) => (
            <ReportCard key={report.id} report={report} isAdmin={true} />
          ))}
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
