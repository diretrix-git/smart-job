import { useState } from 'react';
import { Upload, CheckCircle, Loader2 } from 'lucide-react';
import { resumesAPI } from '../services/api';
import { validateResumeFile } from '../utils/file';

export default function ResumeUploader() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);

  const uploadFile = async (selectedFile) => {
    setFile(selectedFile);
    setUploading(true);
    setMessage('');
    try {
      await resumesAPI.upload(selectedFile);
      setMessage('Resume uploaded successfully!');
    } catch (error) {
      setMessage('Failed to upload resume.');
      setFile(null);
    } finally {
      setUploading(false);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      const validation = validateResumeFile(selectedFile);
      if (!validation.valid) {
        setMessage(validation.message);
        return;
      }
      uploadFile(selectedFile);
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
      uploadFile(selectedFile);
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
        {uploading ? (
          <div className="text-center py-4">
             <Loader2 className="w-10 h-10 text-indigo-500 animate-spin mx-auto mb-3" />
             <p className="text-sm font-medium text-slate-700">Uploading {file?.name}...</p>
          </div>
        ) : file && message.includes('successfully') ? (
          <div className="text-center py-4">
             <CheckCircle className="w-10 h-10 text-emerald-500 mx-auto mb-3" />
             <p className="text-sm font-medium text-slate-800">{file.name} Uploaded!</p>
             <button 
              onClick={() => { setFile(null); setMessage(''); }} 
              className="mt-3 text-xs text-indigo-600 hover:text-indigo-800 font-medium underline"
            >
              Upload a different resume
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
      </div>
      {message && !message.includes('successfully') && (
        <p className="mt-4 text-center text-sm font-medium flex items-center justify-center text-red-600">
          {message}
        </p>
      )}
    </div>
  );
}
