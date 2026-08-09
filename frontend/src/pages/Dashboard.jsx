import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import ResumeUploader from '../components/ResumeUploader';
import JobRecommendations from '../components/JobRecommendations';

export default function Dashboard() {
  const { user } = useContext(AuthContext);

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
        <h2 className="text-2xl font-bold text-slate-800">Welcome, {user?.username || user?.email}</h2>
        <p className="text-slate-500 mt-2">Manage your resume and find matched jobs below.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <ResumeUploader />
        <JobRecommendations />
      </div>
    </div>
  );
}
