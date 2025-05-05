import React, { useState, useRef } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const MediaUpload = ({ onMediaChange }) => {
  const navigate = useNavigate();
  const [mediaType, setMediaType] = useState('image'); // 'image', 'video'
  const [uploadType, setUploadType] = useState('url'); // 'url', 'file'
  const [mediaUrl, setMediaUrl] = useState('');
  const [fileUploaded, setFileUploaded] = useState(null);
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const fileInputRef = useRef(null);

  // Reset fields when changing media types
  const handleMediaTypeChange = (type) => {
    setMediaType(type);
    setMediaUrl('');
    setFileUploaded(null);
    setPreview(null);
    setError('');
    
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };
  
  // Reset fields when changing upload types
  const handleUploadTypeChange = (type) => {
    setUploadType(type);
    setMediaUrl('');
    setFileUploaded(null);
    setPreview(null);
    setError('');
    
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Validate URL input
  const validateUrl = (url, type) => {
    if (!url) return false;
    
    // Basic URL validation
    if (!url.match(/^https?:\/\/.+/i)) {
      setError(`Please enter a valid ${type} URL starting with http:// or https://`);
      return false;
    }
    
    // Image URL validation - check for common extensions
    if (type === 'image' && !url.match(/\.(jpeg|jpg|gif|png|webp|bmp|svg)(\?.*)?$/i)) {
      setError('URL does not point to a supported image file');
      return false;
    }
    
    // Video URL validation - check for common extensions or video hosting services
    if (type === 'video' && 
        !url.match(/\.(mp4|webm|ogg|mov)(\?.*)?$/i) && 
        !url.match(/^https?:\/\/(www\.)?(youtube\.com|youtu\.be|vimeo\.com)/i)) {
      setError('URL does not point to a supported video file or service');
      return false;
    }
    
    setError('');
    return true;
  };

  // Handle URL input change
  const handleUrlChange = (e) => {
    const url = e.target.value;
    setMediaUrl(url);
    
    if (url) {
      if (validateUrl(url, mediaType)) {
        setPreview(url);
        
        // Notify parent component
        if (onMediaChange) {
          onMediaChange({
            type: mediaType,
            source: 'url',
            url: url,
            file: null
          });
        }
      } else {
        setPreview(null);
      }
    } else {
      setError('');
      setPreview(null);
    }
  };

  // Handle file upload
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setError('');
    
    if (!file) {
      setFileUploaded(null);
      setPreview(null);
      return;
    }
    
    // Validate file type
    const acceptedImageTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/svg+xml'];
    const acceptedVideoTypes = ['video/mp4', 'video/webm', 'video/ogg', 'video/quicktime'];
    
    if (mediaType === 'image' && !acceptedImageTypes.includes(file.type)) {
      setError('File is not a supported image type. Please upload JPEG, PNG, GIF, WEBP, or SVG.');
      fileInputRef.current.value = '';
      return;
    }
    
    if (mediaType === 'video' && !acceptedVideoTypes.includes(file.type)) {
      setError('File is not a supported video type. Please upload MP4, WebM, OGG, or MOV.');
      fileInputRef.current.value = '';
      return;
    }
    
    // Check file size (limit to 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size exceeds 10MB limit.');
      fileInputRef.current.value = '';
      return;
    }
    
    setFileUploaded(file);
    
    // Create preview URL
    const objectUrl = URL.createObjectURL(file);
    setPreview(objectUrl);
    
    // Notify parent component
    if (onMediaChange) {
      onMediaChange({
        type: mediaType,
        source: 'file',
        url: null,
        file: file
      });
    }
    
    // Clean up object URL on component unmount
    return () => URL.revokeObjectURL(objectUrl);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (uploadType === 'url' && !mediaUrl) {
      setError(`Please enter a ${mediaType} URL`);
      return;
    }
    
    if (uploadType === 'file' && !fileUploaded) {
      setError(`Please select a ${mediaType} file to upload`);
      return;
    }
    
    // This would typically upload the file to your server
    setLoading(true);
    
    try {
      // Here you would typically send the media to your server
      // For demonstration purposes, we're just simulating a successful upload
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      console.log('Media submitted:', {
        type: mediaType,
        source: uploadType,
        url: mediaUrl,
        file: fileUploaded
      });
      
      // Set success state
      setSuccess(true);
      
      // Navigate to dashboard after successful upload
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
      
    } catch (error) {
      setError('Upload failed. Please try again.');
      console.error('Upload error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-4">
      <div className="p-8 bg-gray-800 rounded-2xl shadow-xl space-y-8 text-white">
        <h2 className="text-2xl font-bold mb-6 border-b border-gray-700 pb-4">
          Media Upload
        </h2>
        
        {error && (
          <div className="p-3 rounded-lg bg-red-900 text-red-200 text-base">
            <span className="mr-2">⚠️</span> {error}
          </div>
        )}

        {success && (
          <div className="p-3 rounded-lg bg-green-900 text-green-200 text-base">
            <span className="mr-2">✅</span> Media uploaded successfully! Redirecting to dashboard...
          </div>
        )}
        
        <form onSubmit={handleSubmit}>
          {/* Media Type Selection */}
          <div className="mb-6">
            <label className="block mb-2 font-semibold text-lg">Media Type</label>
            <div className="flex space-x-4">
              <button
                type="button"
                onClick={() => handleMediaTypeChange('image')}
                className={`px-5 py-3 rounded-lg font-medium ${
                  mediaType === 'image' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                Image
              </button>
              <button
                type="button"
                onClick={() => handleMediaTypeChange('video')}
                className={`px-5 py-3 rounded-lg font-medium ${
                  mediaType === 'video' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                Video
              </button>
            </div>
          </div>
          
          {/* Upload Type Selection */}
          <div className="mb-6">
            <label className="block mb-2 font-semibold text-lg">Upload Method</label>
            <div className="flex space-x-4">
              <button
                type="button"
                onClick={() => handleUploadTypeChange('url')}
                className={`px-5 py-3 rounded-lg font-medium ${
                  uploadType === 'url' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                URL
              </button>
              <button
                type="button"
                onClick={() => handleUploadTypeChange('file')}
                className={`px-5 py-3 rounded-lg font-medium ${
                  uploadType === 'file' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                }`}
              >
                File Upload
              </button>
            </div>
          </div>
          
          {/* URL Input */}
          {uploadType === 'url' && (
            <div className="mb-6">
              <label htmlFor="mediaUrl" className="block mb-2 font-semibold text-lg">
                {mediaType === 'image' ? 'Image URL' : 'Video URL'}
              </label>
              <input
                type="text"
                id="mediaUrl"
                value={mediaUrl}
                onChange={handleUrlChange}
                placeholder={mediaType === 'image' 
                  ? 'https://example.com/image.jpg' 
                  : 'https://example.com/video.mp4'}
                className="w-full p-4 rounded-lg text-base bg-gray-700 border border-gray-600 focus:border-blue-500 transition-colors focus:outline-none"
              />
              <p className="mt-1 text-sm text-gray-400">
                {mediaType === 'image' 
                  ? 'Enter the URL of your image (JPG, PNG, GIF, WEBP, etc.)' 
                  : 'Enter the URL of your video (MP4, WebM, YouTube, Vimeo, etc.)'}
              </p>
            </div>
          )}
          
          {/* File Upload */}
          {uploadType === 'file' && (
            <div className="mb-6">
              <label htmlFor="mediaFile" className="block mb-2 font-semibold text-lg">
                {mediaType === 'image' ? 'Upload Image' : 'Upload Video'}
              </label>
              <input
                type="file"
                id="mediaFile"
                onChange={handleFileChange}
                accept={mediaType === 'image' 
                  ? 'image/jpeg, image/png, image/gif, image/webp, image/svg+xml' 
                  : 'video/mp4, video/webm, video/ogg, video/quicktime'}
                ref={fileInputRef}
                className="w-full p-4 rounded-lg text-base bg-gray-700 border border-gray-600 focus:border-blue-500 transition-colors focus:outline-none"
              />
              <p className="mt-1 text-sm text-gray-400">
                {mediaType === 'image' 
                  ? 'Maximum file size: 10MB. Supported formats: JPG, PNG, GIF, WEBP, SVG' 
                  : 'Maximum file size: 10MB. Supported formats: MP4, WebM, OGG, MOV'}
              </p>
            </div>
          )}
          
          {/* Preview */}
          {preview && (
            <div className="mb-6">
              <label className="block mb-2 font-semibold text-lg">Preview</label>
              <div className="border border-gray-600 rounded-lg p-2 bg-gray-900">
                {mediaType === 'image' ? (
                  <img 
                    src={preview} 
                    alt="Preview" 
                    className="max-h-64 mx-auto rounded-lg object-contain"
                    onError={() => {
                      setError('Failed to load image. Please check the URL and try again.');
                      setPreview(null);
                    }}
                  />
                ) : (
                  <video 
                    src={preview} 
                    controls 
                    className="max-h-64 w-full rounded-lg"
                    onError={() => {
                      setError('Failed to load video. Please check the URL and try again.');
                      setPreview(null);
                    }}
                  >
                    Your browser does not support the video tag.
                  </video>
                )}
              </div>
            </div>
          )}
          
          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading || (!mediaUrl && !fileUploaded) || success}
            className="w-full py-4 px-6 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 disabled:opacity-70 rounded-lg font-bold text-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:ring-offset-gray-800 mt-4"
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Uploading...
              </span>
            ) : (
              `Upload ${mediaType === 'image' ? 'Image' : 'Video'}`
            )}
          </button>
          
          <div className="flex justify-between text-sm mt-4">
            <Link to="/report-incident" className="text-blue-400 hover:text-blue-300">
              ← Back to Incident Form
            </Link>
            <Link to="/dashboard" className="text-blue-400 hover:text-blue-300">
              Skip to Dashboard →
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default MediaUpload;