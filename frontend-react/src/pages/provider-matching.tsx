import React, { useState, useEffect } from "react";

interface ProviderMatchingProps {
  addLog: (type: "info" | "warning" | "error" | "success", message: string, details?: string) => void;
}

const ProviderMatching: React.FC<ProviderMatchingProps> = ({ addLog }) => {
  const [injuryDescription, setInjuryDescription] = useState("");
  const [zipCode, setZipCode] = useState("");
  const [insurance, setInsurance] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<any[]>([]);
  const [insuranceOptions, setInsuranceOptions] = useState<string[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/insurances")
      .then(res => res.json())
      .then(data => setInsuranceOptions(data))
      .catch(() => setInsuranceOptions([]));
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults([]);
    addLog("info", "Starting provider matching", `Injury: ${injuryDescription}, ZIP: ${zipCode}, Insurance: ${insurance}`);
    
    try {
      const response = await fetch("http://localhost:8000/api/match-providers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          injury_description: injuryDescription,
          zip_code: zipCode,
          insurance,
        }),
      });
      if (!response.ok) {
        throw new Error((await response.json()).detail || "Failed to fetch providers");
      }
      const data = await response.json();
      setResults(data);
      addLog("success", `Found ${data.length} matching providers`);
    } catch (err: any) {
      setError(err.message || "Unknown error");
      addLog("error", "Provider matching failed", err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Provider Matching</h1>
      <form className="space-y-4" onSubmit={handleSubmit}>
        <div>
          <label className="block font-medium">Injury Description</label>
          <textarea
            className="w-full border rounded p-2"
            value={injuryDescription}
            onChange={e => setInjuryDescription(e.target.value)}
            rows={3}
            required
          />
        </div>
        <div>
          <label className="block font-medium">Zip Code</label>
          <input
            className="w-full border rounded p-2"
            type="text"
            value={zipCode}
            onChange={e => setZipCode(e.target.value)}
            required
          />
        </div>
        <div>
          <label className="block font-medium">Insurance</label>
          <select
            className="w-full border rounded p-2"
            value={insurance}
            onChange={e => setInsurance(e.target.value)}
            required
          >
            <option value="">Select insurance</option>
            {insuranceOptions.map(option => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </div>
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded"
          disabled={loading}
        >
          {loading ? "Matching..." : "Find Providers"}
        </button>
      </form>
      {error && <div className="text-red-600 mt-4">{error}</div>}
      {loading && <div className="mt-4">Loading...</div>}
      {results.length > 0 && (
        <div className="mt-6 space-y-4">
          {results.map((provider, idx) => (
            <div key={idx} className="border rounded p-4 shadow">
              <div className="font-bold text-lg">{provider.name}</div>
              <div>Specialty: {provider.specialty}</div>
              <div>Distance: {provider.distance} miles</div>
              <div>Availability: {provider.availability}</div>
              <div className="text-sm text-gray-600">Reason: {provider.ranking_reason}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ProviderMatching;