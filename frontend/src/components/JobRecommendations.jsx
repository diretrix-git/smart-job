import { useState } from 'react';
import { Briefcase, BookOpen, CheckCircle } from 'lucide-react';
import { recommendationsAPI } from '../services/api';

export default function JobRecommendations() {
  const [jobs, setJobs] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFetchRecommendations = async () => {
    setLoading(true);
    setMessage('');
    try {
      const res = await recommendationsAPI.getJobs();
      setJobs(res.data);
      setMessage(res.data.length > 0 ? `Found ${res.data.length} matching jobs!` : 'No matching jobs found.');
    } catch (error) {
      setMessage('Failed to fetch recommendations.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="space-y-8">
        <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200 transition-shadow hover:shadow-md">
          <div className="flex items-center space-x-3 mb-4">
            <Briefcase className="w-6 h-6 text-emerald-500" />
            <h3 className="text-xl font-semibold text-slate-800">Job Recommendations</h3>
          </div>
          <p className="text-sm text-slate-500 mb-6">Based on your parsed resume skills.</p>
          <button 
            onClick={handleFetchRecommendations} 
            disabled={loading}
            className="w-full py-2 bg-slate-800 text-white rounded-md font-medium hover:bg-slate-900 disabled:opacity-50 transition-colors"
          >
            {loading ? 'Finding Jobs...' : 'Find Matching Jobs'}
          </button>
          {message && (
            <p className={`mt-4 text-center text-sm font-medium flex items-center justify-center ${message.includes('Found') ? 'text-emerald-600' : 'text-slate-600'}`}>
              {message.includes('Found') ? <CheckCircle className="w-4 h-4 mr-2" /> : null}
              {message}
            </p>
          )}
        </div>
      </div>

      {jobs.length > 0 && (
        <div className="mt-8 space-y-6 md:col-span-2">
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
                        {skill}
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
                         <span className="text-slate-500 text-xs mt-1 font-medium">{course.provider || course.platform}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </>
  );
}
