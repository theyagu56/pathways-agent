import React, { useState } from 'react';

interface ProviderMatch {
  name: string;
  specialty: string;
  distance: number;
  availability: string;
  ranking_reason: string;
}

interface MatchRequest {
  injury_description: string;
  zip_code: string;
  insurance: string;
}

interface ProviderMatchingProps {
  addLog: (type: 'info' | 'warning' | 'error' | 'success', message: string, details?: string) => void;
}

const ProviderMatching: React.FC<ProviderMatchingProps> = ({ addLog }) => {
  const [formData, setFormData] = useState<MatchRequest>({
    injury_description: '',
    zip_code: '',
    insurance: ''
  });
  const [providers, setProviders] = useState<ProviderMatch[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const insuranceOptions = [
    'Blue Cross',
    'Aetna',
    'Cigna',
    'UnitedHealth',
    'Medicare'
  ];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Form validation
    if (!formData.injury_description.trim()) {
      setError('Please describe your injury or condition.');
      addLog('error', 'Form validation failed', 'Injury description is required');
      setLoading(false);
      return;
    }
    
    if (!formData.zip_code.trim()) {
      setError('Please enter your ZIP code.');
      addLog('error', 'Form validation failed', 'ZIP code is required');
      setLoading(false);
      return;
    }
    
    if (!formData.insurance) {
      setError('Please select your insurance provider.');
      addLog('error', 'Form validation failed', 'Insurance provider is required');
      setLoading(false);
      return;
    }
    
    // Validate ZIP code format (basic)
    const zipRegex = /^\d{5}(-\d{4})?$/;
    if (!zipRegex.test(formData.zip_code.trim())) {
      setError('Please enter a valid 5-digit ZIP code.');
      addLog('error', 'Form validation failed', 'Invalid ZIP code format');
      setLoading(false);
      return;
    }

    addLog('info', 'Starting provider search', `Injury: ${formData.injury_description}, ZIP: ${formData.zip_code}, Insurance: ${formData.insurance}`);

    try {
      console.log('🚀 Sending provider matching request:', formData);
      addLog('info', 'Sending API request', 'Connecting to backend server...');
      
      const response = await fetch('http://localhost:8000/api/match-providers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      console.log('📡 Response status:', response.status);
      addLog('info', 'Received API response', `Status: ${response.status}`);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ API Error Response:', errorText);
        
        let errorMessage = `Server error (${response.status})`;
        try {
          const errorData = JSON.parse(errorText);
          errorMessage = errorData.detail || errorMessage;
        } catch {
          errorMessage = errorText || errorMessage;
        }
        
        addLog('error', 'API request failed', errorMessage);
        throw new Error(errorMessage);
      }

      const data = await response.json();
      console.log('✅ Received providers:', data);
      setProviders(data);
      
      if (data.length === 0) {
        setError('No providers found matching your criteria. Try adjusting your search parameters.');
        addLog('warning', 'No providers found', 'Try adjusting search criteria');
      } else {
        addLog('success', 'Providers found', `Found ${data.length} matching providers`);
      }
      
    } catch (err) {
      console.error('❌ Error in handleSubmit:', err);
      
      let errorMessage = 'An unexpected error occurred';
      
      if (err instanceof Error) {
        if (err.message.includes('Failed to fetch')) {
          errorMessage = 'Cannot connect to the server. Please make sure the backend is running on http://localhost:8000';
          addLog('error', 'Connection failed', 'Backend server not accessible');
        } else if (err.message.includes('NetworkError')) {
          errorMessage = 'Network error. Please check your internet connection.';
          addLog('error', 'Network error', 'Check internet connection');
        } else {
          errorMessage = err.message;
          addLog('error', 'Request failed', errorMessage);
        }
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Provider Matching
        </h1>
        <p className="text-lg text-gray-600">
          Find the right healthcare provider for your needs
        </p>
      </div>

        {/* Form */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">
            Provider Matching
          </h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="injury_description" className="block text-sm font-medium text-gray-700 mb-2">
                Describe your injury or condition
              </label>
              <textarea
                id="injury_description"
                name="injury_description"
                value={formData.injury_description}
                onChange={handleInputChange}
                required
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                placeholder="Describe your symptoms, injury, or condition in detail..."
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="zip_code" className="block text-sm font-medium text-gray-700 mb-2">
                  ZIP Code
                </label>
                <input
                  type="text"
                  id="zip_code"
                  name="zip_code"
                  value={formData.zip_code}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter your ZIP code"
                />
              </div>

              <div>
                <label htmlFor="insurance" className="block text-sm font-medium text-gray-700 mb-2">
                  Insurance Provider
                </label>
                <select
                  id="insurance"
                  name="insurance"
                  value={formData.insurance}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">Select insurance provider</option>
                  {insuranceOptions.map(option => (
                    <option key={option} value={option}>
                      {option}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="flex justify-center">
              <button
                type="submit"
                disabled={loading}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-8 rounded-lg transition duration-200 flex items-center space-x-2"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>Finding Providers...</span>
                  </>
                ) : (
                  <span>Find Providers</span>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3 flex-1">
                <h3 className="text-sm font-medium text-red-800">
                  Error
                </h3>
                <div className="mt-2 text-sm text-red-700">
                  {error}
                </div>
                {error.includes('Cannot connect to the server') && (
                  <div className="mt-3 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
                    <h4 className="text-sm font-medium text-yellow-800 mb-2">💡 Troubleshooting Tips:</h4>
                    <ul className="text-sm text-yellow-700 space-y-1">
                      <li>• Make sure the backend server is running on port 8000</li>
                      <li>• Check that you're running: <code className="bg-yellow-100 px-1 rounded">python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload</code></li>
                      <li>• Verify the backend is accessible at <a href="http://localhost:8000" target="_blank" rel="noreferrer" className="underline">http://localhost:8000</a></li>
                    </ul>
                  </div>
                )}
              </div>
              <div className="flex-shrink-0">
                <button
                  onClick={() => setError(null)}
                  className="text-red-400 hover:text-red-600"
                >
                  <svg className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {providers.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-2xl font-semibold text-gray-900 mb-6">
              Recommended Providers
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {providers.map((provider, index) => (
                <div key={index} className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                  <div className="flex items-start justify-between mb-4">
                    <h4 className="text-lg font-semibold text-gray-900">
                      {provider.name}
                    </h4>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      #{index + 1}
                    </span>
                  </div>
                  
                  <div className="space-y-3">
                    <div>
                      <span className="text-sm font-medium text-gray-500">Specialty:</span>
                      <p className="text-sm text-gray-900">{provider.specialty}</p>
                    </div>
                    
                    <div>
                      <span className="text-sm font-medium text-gray-500">Distance:</span>
                      <p className="text-sm text-gray-900">{provider.distance.toFixed(1)} miles</p>
                    </div>
                    
                    <div>
                      <span className="text-sm font-medium text-gray-500">Next Available:</span>
                      <p className="text-sm text-gray-900">{provider.availability}</p>
                    </div>
                    
                    <div>
                      <span className="text-sm font-medium text-gray-500">Why Recommended:</span>
                      <p className="text-sm text-gray-900">{provider.ranking_reason}</p>
                    </div>
                  </div>
                  
                  <div className="mt-4 pt-4 border-t border-gray-200">
                    <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition duration-200">
                      Schedule Appointment
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
    </div>
  );
};

export default ProviderMatching; 