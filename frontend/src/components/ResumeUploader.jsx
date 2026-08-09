import { useState } from 'react';
import { Upload, CheckCircle } from 'lucide-react';
import { resumesAPI } from '../services/api';
import { validateResumeFile } from '../utils/file';

export default function ResumeUploader() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      const validation = validateResumeFile(selectedFile);
      if (!validation.valid) {
        setMessage(validation.message);
        return;
      }
      setFile(selectedFile);
      setMessage('');
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const selectedFile = e.dataTransfer.files[0];
      const validation = validateResumeFile(selectedFile);
      if (!validation.valid) {
        setMessage(validation.message);
        return;
      }
      setFile(selectedFile);
      setMessage('');
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setMessage('');
    try {
      await resumesAPI.upload(file);
      setMessage('Resume uploaded successfully!');
      setFile(null);
    } catch (error) {
      setMessage('Failed to upload resume.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
      <div className="flex items-center space-x-3 mb-6">
        <Upload className="w-6 h-6 text-indigo-500" />
        <h3 className="text-xl font-semibold text-slate-800">Upload Resume</h3>
      </div>
      <div 
        className={`flex flex-col items-center justify-center border-2 border-dashed rounded-lg p-8 transition-colors ${
          isDragOver ? 'border-indigo-500 bg-indigo-50' : 'border-slate-300 hover:border-indigo-400 bg-slate-50'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {file ? (
          <div className="text-center">
            <p className="text-sm font-medium text-slate-800">{file.name}</p>
            <p className="text-xs text-slate-500 mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            <button 
              onClick={() => setFile(null)} 
              className="mt-3 text-xs text-red-500 hover:text-red-700 font-medium"
            >
              Remove file
            </button>
          </div>
        ) : (
          <div className="text-center">
            <Upload className="w-10 h-10 text-slate-400 mx-auto mb-3" />
            <p className="text-sm font-medium text-slate-700">Drag & drop your resume here, or</p>
            <label className="mt-2 cursor-pointer inline-flex items-center justify-center px-4 py-2 text-sm font-semibold text-indigo-700 bg-indigo-100 rounded-full hover:bg-indigo-200 transition-colors">
              <span>Browse files</span>
              <input 
                type="file" 
                accept=".pdf,.docx,.doc,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/msword" 
                onChange={handleFileChange}
                className="hidden"
              />
            </label>
          </div>
        )}
        
        {file && (
          <button 
            onClick={handleUpload}
            disabled={uploading}
            className="mt-6 w-full py-2 bg-indigo-600 text-white rounded-md font-medium hover:bg-indigo-700 disabled:opacity-50 transition-colors"
          >
            {uploading ? 'Uploading...' : 'Upload File'}
          </button>
        )}
      </div>
      {message && (
        <p className={`mt-4 text-center text-sm font-medium flex items-center justify-center ${message.includes('successfully') ? 'text-emerald-600' : 'text-red-600'}`}>
          {message.includes('successfully') ? <CheckCircle className="w-4 h-4 mr-2" /> : null}
          {message}
        </p>
      )}
    </div>
  );
}
