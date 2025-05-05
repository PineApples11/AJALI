import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Homepage from './pages/Homepage';
import AdminDashboard from './pages/AdminDashboard';
<<<<<<< HEAD
import IncidentForm from './components/IncidentForm';
import MediaUpload from './components/MediaUpload';
import ProtectedRoute from './components/ProtectedRoute';
=======
import ProtectedRoute from './components/ProtectedRoute';

>>>>>>> development
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
<<<<<<< HEAD
        <Route 
          path="/report-incident" 
          element={
            <ProtectedRoute>
                <IncidentForm />
            </ProtectedRoute>
          } 
        />
        <Route 
          path="/upload-media" 
          element={
            <ProtectedRoute>
                <MediaUpload onMediaChange={(mediaData) => console.log('Media data:', mediaData)} />
            </ProtectedRoute>
          } 
        />
=======
>>>>>>> development
      </Routes>
    </Router>
  );
}
<<<<<<< HEAD
export default App;
=======

export default App;
>>>>>>> development
