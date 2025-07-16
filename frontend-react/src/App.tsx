import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import ProviderMatching from './pages/provider-matching';
import Appointments from './pages/Appointments';
import Documents from './pages/Documents';
import Settings from './pages/Settings';
import PatientIntakeForm from './components/PatientIntakeForm';

interface LogEntry {
  id: string;
  timestamp: string;
  type: 'info' | 'warning' | 'error' | 'success';
  message: string;
  details?: string;
}

function App() {
  const [logs, setLogs] = useState<LogEntry[]>([]);

  const addLog = (type: LogEntry['type'], message: string, details?: string) => {
    const newLog: LogEntry = {
      id: Date.now().toString(),
      timestamp: new Date().toLocaleString(),
      type,
      message,
      details
    };
    setLogs(prev => [newLog, ...prev]);
  };

  const clearLogs = () => {
    setLogs([]);
  };

  return (
    <Router>
      <Layout logs={logs} addLog={addLog} clearLogs={clearLogs}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/patient-intake" element={
            <PatientIntakeForm
              familyMembers={[]}
              insuranceProviders={[]}
              mode="dashboard"
              onSubmit={(data) => {
                console.log('Form submitted:', data);
              }}
            />
          } />
          <Route path="/referral-management" element={<ProviderMatching addLog={addLog} />} />
          <Route path="/appointments" element={<Appointments />} />
          <Route path="/documents" element={<Documents />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App; 