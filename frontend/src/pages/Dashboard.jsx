import { useContext, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import { resumesAPI, recommendationsAPI } from '../services/api';
import { Upload, Briefcase, BookOpen, CheckCircle } from 'lucide-react';

export default function Dashboard() {
  const { user } = useContext(AuthContext);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [jobs, setJobs] = useState([]);
  
  const [isDragOver, setIsDragOver] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0];
      if (selectedFile.size > 10 * 1024 * 1024) {
        setMessage('File size exceeds 10MB limit.');
        return;
      }
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
      const fileExt = selectedFile.name.toLowerCase().slice(selectedFile.name.lastIndexOf('.'));
      if (!allowedTypes.includes(selectedFile.type) && !['.pdf', '.docx', '.doc'].includes(fileExt)) {
        setMessage('Please upload a PDF or DOCX file.');
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
      if (selectedFile.size > 10 * 1024 * 1024) {
        setMessage('File size exceeds 10MB limit.');
        return;
      }
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'];
      const fileExt = selectedFile.name.toLowerCase().slice(selectedFile.name.lastIndexOf('.'));
      if (!allowedTypes.includes(selectedFile.type) && !['.pdf', '.docx', '.doc'].includes(fileExt)) {
        setMessage('Please upload a PDF or DOCX file.');
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

  const handleFetchRecommendations = async () => {
    try {
      const res = await recommendationsAPI.getJobs();
      setJobs(res.data);
      setMessage(res.data.length > 0 ? `Found ${res.data.length} matching jobs!` : 'No matching jobs found.');
    } catch (error) {
      setMessage('Failed to fetch recommendations.');
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
        <h2 className="text-2xl font-bold text-slate-800">Welcome, {user?.username || user?.email}</h2>
        <p className="text-slate-500 mt-2">Manage your resume and find matched jobs below.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
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
            <p className={`mt-4 text-center text-sm font-medium flex items-center justify-center ${message.includes('successfully') || message.includes('Found') ? 'text-emerald-600' : 'text-red-600'}`}>
              {message.includes('successfully') || message.includes('Found') ? <CheckCircle className="w-4 h-4 mr-2" /> : null}
              {message}
            </p>
          )}
        </div>

        <div className="space-y-8">
          <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200 transition-shadow hover:shadow-md">
            <div className="flex items-center space-x-3 mb-4">
              <Briefcase className="w-6 h-6 text-emerald-500" />
              <h3 className="text-xl font-semibold text-slate-800">Job Recommendations</h3>
            </div>
            <p className="text-sm text-slate-500 mb-6">Based on your parsed resume skills.</p>
            <button onClick={handleFetchRecommendations} className="w-full py-2 bg-slate-800 text-white rounded-md font-medium hover:bg-slate-900 transition-colors">
              Find Matching Jobs
            </button>
          </div>
        </div>
      </div>

      {jobs.length > 0 && (
        <div className="mt-8 space-y-6">
          <h3 className="text-2xl font-semibold text-slate-800 flex items-center">
            <Briefcase className="w-6 h-6 mr-3 text-indigo-500" />
            Your Recommended Jobs
          </h3>
          {jobs.map((match, idx) => (
            <div key={idx} className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start">
                 <div>
                   <h4 className="text-lg font-bold text-slate-800">{match.job.title}</h4>
                   <h5 className="text-md font-medium text-indigo-600">
                     {match.job.company_url ? (
                       <a href={match.job.company_url} target="_blank" rel="noreferrer" className="hover:underline">
                         {match.job.company}
                       </a>
                     ) : (
                       match.job.company
                     )}
                   </h5>
                   <p className="text-sm text-slate-600 mt-3">{match.job.description}</p>
                 </div>
                 <div className="bg-emerald-100 text-emerald-800 px-4 py-2 rounded-full text-sm font-bold shadow-sm whitespace-nowrap">
                   {(match.match_score * 100).toFixed(0)}% Match
                 </div>
              </div>
              
              {match.missing_skills && match.missing_skills.length > 0 && (
                <div className="mt-6 pt-4 border-t border-slate-100">
                  <h5 className="text-sm font-semibold text-amber-600 mb-3 flex items-center">
                    Skills to Improve
                  </h5>
                  <div className="flex flex-wrap gap-2">
                    {match.missing_skills.map((skill, i) => (
                      <span key={i} className="bg-amber-50 text-amber-700 px-3 py-1.5 rounded-md text-xs font-medium border border-amber-200">
                        {skill.name}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              
              {match.recommended_courses && match.recommended_courses.length > 0 && (
                <div className="mt-6 pt-4 border-t border-slate-100">
                  <h5 className="text-sm font-semibold text-emerald-600 mb-3 flex items-center">
                    <BookOpen className="w-4 h-4 mr-2" />
                    Recommended Courses
                  </h5>
                  <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {match.recommended_courses.map((course, i) => (
                      <li key={i} className="text-sm bg-slate-50 p-3 rounded-lg border border-slate-100 flex flex-col justify-center">
                         <a href={course.url} target="_blank" rel="noreferrer" className="text-indigo-600 hover:text-indigo-800 hover:underline font-medium block truncate" title={course.title}>
                           {course.title}
                         </a>
                         <span className="text-slate-500 text-xs mt-1 font-medium">{course.platform}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
