import { Routes, Route, Navigate, Link } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from './context/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Profile from './pages/Profile';

function App() {
  const { user, logout } = useContext(AuthContext);

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      <nav className="bg-white shadow-sm border-b border-slate-200 px-6 py-4 flex justify-between items-center sticky top-0 z-10">
        <Link to="/dashboard">
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-violet-600 hover:opacity-80 transition-opacity">
            Smart Job Recommender
          </h1>
        </Link>
        {user && (
          <div className="flex space-x-6 items-center">
            <Link 
              to="/profile"
              className="text-sm font-medium text-slate-600 hover:text-indigo-600 transition-colors"
            >
              Profile
            </Link>
            <button 
              onClick={logout}
              className="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors"
            >
              Logout
            </button>
          </div>
        )}
      </nav>
      
      <main className="max-w-7xl mx-auto py-10 sm:px-6 lg:px-8">
        <Routes>
          <Route path="/login" element={!user ? <Login /> : <Navigate to="/dashboard" />} />
          <Route path="/register" element={!user ? <Register /> : <Navigate to="/dashboard" />} />
          <Route path="/dashboard" element={user ? <Dashboard /> : <Navigate to="/login" />} />
          <Route path="/profile" element={user ? <Profile /> : <Navigate to="/login" />} />
          <Route path="*" element={<Navigate to={user ? "/dashboard" : "/login"} />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
