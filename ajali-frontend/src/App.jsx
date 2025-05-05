import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Homepage from './pages/Homepage';
import AdminDashboard from './pages/AdminDashboard';
import ProtectedRoute from './components/ProtectedRoute';
import IncidentForm from './components/IncidentForm';
import MediaUpload from './components/MediaUpload';
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route 
          path="/report-incident" 
          element={
            <ProtectedRoute>
              <div className="container mx-auto py-8">
                <h1 className="text-3xl font-bold mb-6 text-center">Report an Incident</h1>
                <IncidentForm />
              </div>
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/upload-media" 
          element={
            <ProtectedRoute>
              <div className="container mx-auto py-8">
                <h1 className="text-3xl font-bold mb-6 text-center">Upload Media</h1>
                <MediaUpload onMediaChange={(mediaData) => console.log('Media data:', mediaData)} />
              </div>
            </ProtectedRoute>
          } 
        />
      </Routes>
    </Router>
  );
}
export default App;