import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const IncidentForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    type: '',
    status: '',
    longitude: '',
    latitude: '',
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [errors, setErrors] = useState({});
  const [useCurrentLocation, setUseCurrentLocation] = useState(false);

  const incidentTypes = [
    { value: 'red_flag', label: 'Red Flag' },
    { value: 'intervention', label: 'Intervention' },
  ];
  
  const incidentStatuses = [
    { value: 'draft', label: 'Draft' },
    { value: 'under_investigation', label: 'Under Investigation' },
    { value: 'resolved', label: 'Resolved' },
    { value: 'rejected', label: 'Rejected' }
  ];

  // Get current location if user requests it
  useEffect(() => {
    if (useCurrentLocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setFormData(prev => ({
            ...prev,
            latitude: position.coords.latitude.toString(),
            longitude: position.coords.longitude.toString()
          }));
          setUseCurrentLocation(false);
        },
        (error) => {
          console.error("Error getting location:", error);
          setMessage("Error: Couldn't get your location. Please enter coordinates manually.");
          setUseCurrentLocation(false);
        }
      );
    }
  }, [useCurrentLocation]);

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.title.trim()) newErrors.title = "Title is required";
    else if (formData.title.length < 5) newErrors.title = "Title must be at least 5 characters";
    
    if (!formData.description.trim()) newErrors.description = "Description is required";
    else if (formData.description.length < 20) newErrors.description = "Description should be more detailed (min 20 chars)";
    
    if (!formData.type) newErrors.type = "Please select an incident type";
    if (!formData.status) newErrors.status = "Please select a status";
    
    if (!formData.longitude) newErrors.longitude = "Longitude is required";
    else if (isNaN(parseFloat(formData.longitude)) || 
             parseFloat(formData.longitude) < -180 || 
             parseFloat(formData.longitude) > 180) {
      newErrors.longitude = "Longitude must be between -180 and 180";
    }
    
    if (!formData.latitude) newErrors.latitude = "Latitude is required";
    else if (isNaN(parseFloat(formData.latitude)) || 
             parseFloat(formData.latitude) < -90 || 
             parseFloat(formData.latitude) > 90) {
      newErrors.latitude = "Latitude must be between -90 and 90";
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('/api/incidents', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          longitude: parseFloat(formData.longitude),
          latitude: parseFloat(formData.latitude),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to submit incident');
      }

      setMessage('Incident submitted successfully!');
      
      // Reset form
      setFormData({
        title: '',
        description: '',
        type: '',
        status: '',
        longitude: '',
        latitude: '',
      });
      
      // Navigate to media upload page after successful submission
      setTimeout(() => {
        navigate('/upload-media');
      }, 2000);
      
    } catch (error) {
      console.error('Submission error:', error);
      setMessage(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <form
        onSubmit={handleSubmit}
        className="p-6 bg-gray-800 rounded-2xl shadow-xl space-y-6 text-white"
        aria-labelledby="form-heading"
      >
        <h2 id="form-heading" className="text-2xl font-semibold mb-4 border-b border-gray-700 pb-2">
          Report an Incident
        </h2>

        {message && (
          <div 
            className={`p-3 rounded text-sm font-medium mb-2 flex items-center ${
              message.startsWith('Error') ? 'bg-red-900 text-red-200' : 'bg-green-900 text-green-200'
            }`}
            role="alert"
          >
            <span className="mr-2">
              {message.startsWith('Error') ? '⚠️' : '✅'}
            </span>
            {message}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Left column */}
          <div className="space-y-6">
            <div>
              <label htmlFor="title" className="block mb-1 font-medium">
                Title <span className="text-red-400">*</span>
              </label>
              <input
                id="title"
                type="text"
                name="title"
                required
                value={formData.title}
                onChange={handleChange}
                aria-describedby={errors.title ? "title-error" : undefined}
                className={`w-full p-3 rounded bg-gray-700 border ${
                  errors.title ? 'border-red-500 focus:border-red-500' : 'border-gray-600 focus:border-blue-500'
                } transition-colors focus:outline-none`}
                placeholder="Brief title of the incident"
              />
              {errors.title && (
                <p id="title-error" className="mt-1 text-sm text-red-400">
                  {errors.title}
                </p>
              )}
            </div>

            <div>
              <label htmlFor="description" className="block mb-1 font-medium">
                Description <span className="text-red-400">*</span>
              </label>
              <textarea
                id="description"
                name="description"
                required
                value={formData.description}
                onChange={handleChange}
                aria-describedby={errors.description ? "description-error" : undefined}
                className={`w-full p-3 rounded bg-gray-700 border ${
                  errors.description ? 'border-red-500 focus:border-red-500' : 'border-gray-600 focus:border-blue-500'
                } transition-colors focus:outline-none min-h-[120px]`}
                placeholder="Detailed description of what happened"
              />
              {errors.description && (
                <p id="description-error" className="mt-1 text-sm text-red-400">
                  {errors.description}
                </p>
              )}
            </div>

            <div>
              <label htmlFor="type" className="block mb-1 font-medium">
                Incident Type <span className="text-red-400">*</span>
              </label>
              <select
                id="type"
                name="type"
                required
                value={formData.type}
                onChange={handleChange}
                aria-describedby={errors.type ? "type-error" : undefined}
                className={`w-full p-3 rounded bg-gray-700 border ${
                  errors.type ? 'border-red-500 focus:border-red-500' : 'border-gray-600 focus:border-blue-500'
                } transition-colors focus:outline-none`}
              >
                <option value="">Select Type</option>
                {incidentTypes.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
              {errors.type && (
                <p id="type-error" className="mt-1 text-sm text-red-400">
                  {errors.type}
                </p>
              )}
            </div>
          </div>

          {/* Right column */}
          <div className="space-y-6">
            <div>
              <label htmlFor="status" className="block mb-1 font-medium">
                Status <span className="text-red-400">*</span>
              </label>
              <select
                id="status"
                name="status"
                required
                value={formData.status}
                onChange={handleChange}
                aria-describedby={errors.status ? "status-error" : undefined}
                className={`w-full p-3 rounded bg-gray-700 border ${
                  errors.status ? 'border-red-500 focus:border-red-500' : 'border-gray-600 focus:border-blue-500'
                } transition-colors focus:outline-none`}
              >
                <option value="">Select Status</option>
                {incidentStatuses.map((status) => (
                  <option key={status.value} value={status.value}>
                    {status.label}
                  </option>
                ))}
              </select>
              {errors.status && (
                <p id="status-error" className="mt-1 text-sm text-red-400">
                  {errors.status}
                </p>
              )}
            </div>

            <div className="space-y-6">
              <div>
                <div className="flex justify-between items-center mb-1">
                  <label htmlFor="longitude" className="block font-medium">
                    Longitude <span className="text-red-400">*</span>
                  </label>
                  <button 
                    type="button" 
                    onClick={() => setUseCurrentLocation(true)}
                    disabled={loading || useCurrentLocation}
                    className="text-xs bg-blue-700 hover:bg-blue-800 px-2 py-1 rounded text-white transition-colors"
                  >
                    {useCurrentLocation ? 'Getting location...' : 'Use Current Location'}
                  </button>
                </div>
                <input
                  id="longitude"
                  type="number"
                  name="longitude"
                  step="any"
                  required
                  value={formData.longitude}
                  onChange={handleChange}
                  aria-describedby={errors.longitude ? "longitude-error" : undefined}
                  className={`w-full p-3 rounded bg-gray-700 border ${
                    errors.longitude ? 'border-red-500 focus:border-red-500' : 'border-gray-600 focus:border-blue-500'
                  } transition-colors focus:outline-none`}
                  placeholder="e.g. -73.935242"
                />
                {errors.longitude && (
                  <p id="longitude-error" className="mt-1 text-sm text-red-400">
                    {errors.longitude}
                  </p>
                )}
              </div>

              <div>
                <label htmlFor="latitude" className="block mb-1 font-medium">
                  Latitude <span className="text-red-400">*</span>
                </label>
                <input
                  id="latitude"
                  type="number"
                  name="latitude"
                  step="any"
                  required
                  value={formData.latitude}
                  onChange={handleChange}
                  aria-describedby={errors.latitude ? "latitude-error" : undefined}
                  className={`w-full p-3 rounded bg-gray-700 border ${
                    errors.latitude ? 'border-red-500 focus:border-red-500' : 'border-gray-600 focus:border-blue-500'
                  } transition-colors focus:outline-none`}
                  placeholder="e.g. 40.730610"
                />
                {errors.latitude && (
                  <p id="latitude-error" className="mt-1 text-sm text-red-400">
                    {errors.latitude}
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="pt-4 border-t border-gray-700">
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:opacity-70 rounded font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-800"
            aria-disabled={loading}
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Submitting...
              </span>
            ) : 'Submit Incident Report'}
          </button>
        </div>

        <div className="flex justify-between text-sm">
          <Link to="/dashboard" className="text-blue-400 hover:text-blue-300">
            ← Back to Dashboard
          </Link>
          <Link to="/upload-media" className="text-blue-400 hover:text-blue-300">
            Skip to Media Upload →
          </Link>
        </div>
      </form>
    </div>
  );
};

export default IncidentForm;