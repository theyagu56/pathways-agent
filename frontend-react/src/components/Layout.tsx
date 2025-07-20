import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

interface LogEntry {
  id: string;
  timestamp: string;
  type: 'info' | 'warning' | 'error' | 'success';
  message: string;
  details?: string;
}

interface LayoutProps {
  children: React.ReactNode;
  logs: LogEntry[];
  addLog: (type: LogEntry['type'], message: string, details?: string) => void;
  clearLogs: () => void;
}

const Layout: React.FC<LayoutProps> = ({ children, logs, addLog, clearLogs }) => {
  const [showEvents, setShowEvents] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const location = useLocation();

  // Navigation menu items
  const menuItems = [
    {
      id: 'dashboard',
      name: 'Dashboard',
      icon: '📊',
      path: '/',
      description: 'Main dashboard'
    },
    {
      id: 'patient-intake',
      name: 'Patient Intake',
      icon: '👤',
      path: '/patient-intake',
      description: 'Patient information and intake form'
    },
    {
      id: 'voice-intake',
      name: 'Voice Intake',
      icon: '🎤',
      path: '/voice-intake',
      description: 'Voice-enabled healthcare triage'
    },
    {
      id: 'referral-management',
      name: 'Referral Management',
      icon: '🏥',
      path: '/referral-management',
      description: 'Provider matching and referrals'
    },
    {
      id: 'appointments',
      name: 'Appointments',
      icon: '📅',
      path: '/appointments',
      description: 'Schedule and manage appointments'
    },
    {
      id: 'documents',
      name: 'Documents',
      icon: '📄',
      path: '/documents',
      description: 'Manage documents'
    },
    {
      id: 'settings',
      name: 'Settings',
      icon: '⚙️',
      path: '/settings',
      description: 'Application settings'
    }
  ];

  // Get log icon based on type
  const getLogIcon = (type: LogEntry['type']) => {
    switch (type) {
      case 'info':
        return 'ℹ️';
      case 'warning':
        return '⚠️';
      case 'error':
        return '❌';
      case 'success':
        return '✅';
      default:
        return '📝';
    }
  };

  // Get log color based on type
  const getLogColor = (type: LogEntry['type']) => {
    switch (type) {
      case 'info':
        return 'text-blue-600';
      case 'warning':
        return 'text-yellow-600';
      case 'error':
        return 'text-red-600';
      case 'success':
        return 'text-green-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Left Sidebar */}
      <div className="w-64 bg-white shadow-lg">
        {/* Logo/Brand */}
        <div className="p-6 border-b border-gray-200">
          <h1 className="text-2xl font-bold text-gray-900">Pathways Agent</h1>
          <p className="text-sm text-gray-600">Healthcare Management</p>
        </div>

        {/* Navigation Menu */}
        <nav className="mt-6">
          <div className="px-4 space-y-2">
            {menuItems.map((item) => (
              <Link
                key={item.id}
                to={item.path}
                className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                  location.pathname === item.path
                    ? 'bg-blue-100 text-blue-700 border-r-2 border-blue-700'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
                title={item.description}
              >
                <span className="text-xl">{item.icon}</span>
                <span className="font-medium">{item.name}</span>
              </Link>
            ))}
          </div>
        </nav>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Navigation Bar */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="flex justify-between items-center px-6 py-4">
            {/* Page Title */}
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                {menuItems.find(item => item.path === location.pathname)?.name || 'Dashboard'}
              </h2>
              <p className="text-sm text-gray-600">
                {menuItems.find(item => item.path === location.pathname)?.description || 'Welcome to Pathways Agent'}
              </p>
            </div>

            {/* Top Right Icons */}
            <div className="flex items-center space-x-4">
              {/* Events Icon */}
              <button
                onClick={() => setShowEvents(!showEvents)}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <span className="text-lg">📊</span>
                <span className="font-medium">Events</span>
                {logs.length > 0 && (
                  <span className="bg-red-500 text-white text-xs rounded-full px-2 py-1 min-w-[20px] text-center">
                    {logs.length}
                  </span>
                )}
              </button>

              {/* My Profile Icon */}
              <button
                onClick={() => setShowProfile(!showProfile)}
                className="flex items-center space-x-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                <span className="text-lg">👤</span>
                <span className="font-medium">My Profile</span>
              </button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>

      {/* Events Modal */}
      {showEvents && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full mx-4 max-h-[80vh] overflow-hidden">
            <div className="flex justify-between items-center p-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Events Log</h3>
              <div className="flex items-center space-x-2">
                <button
                  onClick={clearLogs}
                  className="px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
                >
                  Clear All
                </button>
                <button
                  onClick={() => setShowEvents(false)}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            
            <div className="p-4 overflow-y-auto max-h-[60vh]">
              {logs.length === 0 ? (
                <div className="text-center text-gray-500 py-8">
                  <span className="text-4xl mb-4 block">📝</span>
                  <p>No events logged yet.</p>
                  <p className="text-sm">Events will appear here when you interact with the application.</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {logs.map((log) => (
                    <div
                      key={log.id}
                      className="border border-gray-200 rounded-lg p-3 hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start space-x-3 flex-1">
                          <span className="text-lg">{getLogIcon(log.type)}</span>
                          <div className="flex-1">
                            <div className="flex items-center space-x-2">
                              <span className={`font-medium ${getLogColor(log.type)}`}>
                                {log.message}
                              </span>
                              <span className="text-xs text-gray-500">
                                {log.timestamp}
                              </span>
                            </div>
                            {log.details && (
                              <p className="text-sm text-gray-600 mt-1">
                                {log.details}
                              </p>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Profile Modal */}
      {showProfile && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
            <div className="flex justify-between items-center p-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">My Profile</h3>
              <button
                onClick={() => setShowProfile(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div className="p-6">
              <div className="text-center mb-6">
                <div className="w-20 h-20 bg-gray-300 rounded-full mx-auto mb-4 flex items-center justify-center">
                  <span className="text-3xl">👤</span>
                </div>
                <h4 className="text-xl font-semibold text-gray-900">User Profile</h4>
                <p className="text-gray-600">Pathways Agent User</p>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Name
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    placeholder="Enter your name"
                    defaultValue="John Doe"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md"
                    placeholder="Enter your email"
                    defaultValue="john.doe@example.com"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Preferred Insurance
                  </label>
                  <select className="w-full px-3 py-2 border border-gray-300 rounded-md">
                    <option>Blue Cross</option>
                    <option>Aetna</option>
                    <option>Cigna</option>
                    <option>UnitedHealth</option>
                    <option>Medicare</option>
                  </select>
                </div>
                
                <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors">
                  Save Profile
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Layout; 