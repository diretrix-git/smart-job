import { useContext, useState } from 'react';
import { AuthContext } from '../context/AuthContext';
import { User, Settings, Shield, History, CheckCircle } from 'lucide-react';
import api from '../services/api';

export default function Profile() {
  const { user } = useContext(AuthContext);
  const [username, setUsername] = useState(user?.username || '');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    
    try {
      const payload = {};
      if (username && username !== user?.username) payload.username = username;
      if (password) payload.password = password;

      if (Object.keys(payload).length === 0) {
        setMessage('No changes to save.');
        setLoading(false);
        return;
      }

      await api.put('/auth/me', payload);
      setMessage('Profile updated successfully!');
      setPassword(''); // clear password field after successful update
      
      // Need a hard refresh to get new context, or we can just rely on the message.
      // Ideally we would update the AuthContext state here.
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Failed to update profile.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200 flex items-center space-x-6">
        <div className="w-20 h-20 bg-indigo-100 rounded-full flex items-center justify-center">
          <User className="w-10 h-10 text-indigo-600" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-slate-800">{user?.username || 'User Profile'}</h2>
          <p className="text-slate-500">{user?.email}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="col-span-1 md:col-span-2 space-y-8">
          <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200">
            <div className="flex items-center space-x-3 mb-6">
              <Settings className="w-6 h-6 text-indigo-500" />
              <h3 className="text-xl font-semibold text-slate-800">Account Settings</h3>
            </div>
            
            <form onSubmit={handleUpdate} className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Username</label>
                <input
                  type="text"
                  className="w-full px-4 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1 flex items-center">
                  <Shield className="w-4 h-4 mr-1 text-slate-400" />
                  New Password
                </label>
                <input
                  type="password"
                  className="w-full px-4 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  placeholder="Leave blank to keep current password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2 px-4 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Saving...' : 'Save Changes'}
              </button>

              {message && (
                <p className="mt-4 text-center text-sm font-medium text-indigo-600 flex items-center justify-center">
                  <CheckCircle className="w-4 h-4 mr-2" /> {message}
                </p>
              )}
            </form>
          </div>
        </div>

        <div className="col-span-1 space-y-8">
          <div className="bg-white p-8 rounded-xl shadow-sm border border-slate-200 opacity-60">
            <div className="flex items-center space-x-3 mb-6">
              <History className="w-6 h-6 text-amber-500" />
              <h3 className="text-xl font-semibold text-slate-800">Activity History</h3>
            </div>
            <p className="text-sm text-slate-500">
              Feature coming soon: View your past resume uploads and recommended job matches.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
