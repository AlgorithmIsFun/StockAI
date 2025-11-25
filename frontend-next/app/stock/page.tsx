"use client";

import { useEffect, useState } from "react";
import { fetchFromAPI } from "../../lib/api";

const fetchStockReport = async (ticker) => {
  if (!ticker) {
    throw new Error("Please enter a valid stock ticker.");
  }

  const upperTicker = ticker.toUpperCase().trim();

  // 1. Define the hypothetical Django API endpoint
  const backendUrl = 'http://localhost:8000/api/stock/' + upperTicker + '/';

  console.log(`[SIMULATING FETCH] Attempting to contact Django backend at: ${backendUrl}`);

  // --- START of Simulated Network Call (Replace with actual 'fetch' in production) ---
  try {
    // 1. Initiate the real HTTP request using fetch
    const response = await fetch(backendUrl);

    // 2. Check for HTTP errors (e.g., 404, 503)
    if (!response.ok) {
      // Attempt to parse the JSON error body returned by Django Rest Framework
      const errorBody = await response.json().catch(() => ({ detail: 'No detailed error message from server.' }));

      // Throw an error with the status code and the detail message from the backend
      throw new Error(`[Status ${response.status}] ${errorBody.detail || 'Server error occurred.'}`);
    }

    // 3. Return the parsed JSON report data
    const data = await response.json();
    return data;

  } catch (error) {
    // Handle network errors (e.g., server offline, connection refused)
    if (error.message.includes('Failed to fetch')) {
        throw new Error('Network error: Could not connect to the backend server.');
    }
    throw error; // Re-throw the structured HTTP error
  }
};
// -------------------------------------------------------------------

export default function Reports() {
  const [ticker, setTicker] = useState("");
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFetchReport = async (e) => {
    e.preventDefault();
    setError(null);
    setReport(null);
    setLoading(true);

    try {
      const data = await fetchStockReport(ticker);
      setReport(data);
    } catch (err) {
      // The error object now contains the status and message from the backend
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6 sm:p-10">
      <div className="max-w-3xl mx-auto bg-white shadow-2xl rounded-xl p-6 sm:p-8">
        <h1 className="text-3xl font-extrabold text-gray-900 border-b pb-3 mb-6">
          Stock Report Lookup (Connected to Backend)
        </h1>

        {/* Input Form */}
        <form onSubmit={handleFetchReport} className="flex flex-col sm:flex-row gap-4 mb-8">
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value.toUpperCase())}
            placeholder="Enter Ticker (e.g., GOOG, MSFT)"
            className="flex-grow p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500 text-lg shadow-sm"
            disabled={loading}
          />
          <button
            type="submit"
            className={`px-6 py-3 font-semibold text-white rounded-lg transition duration-300 shadow-md ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 active:bg-blue-800'
            }`}
            disabled={loading}
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin h-5 w-5 mr-3 text-white" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Fetching...
              </span>
            ) : (
              'Get Report'
            )}
          </button>
        </form>

        {/* Results Display */}
        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md mb-4" role="alert">
            <p className="font-bold">Error</p>
            <p>{error}</p>
          </div>
        )}

        {report && (
          <div className="border border-gray-200 rounded-xl p-5 bg-white shadow-lg">
            <h2 className="text-2xl font-bold mb-4 text-blue-700">{report.company} ({report.symbol})</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-gray-700">
              <p><span className="font-semibold">Current Price:</span> <span className="text-xl text-green-600">${report.price}</span></p>
              <p><span className="font-semibold">Sector:</span> {report.sector}</p>
              <p className="sm:col-span-2"><span className="font-semibold">Market Cap:</span> {report.market_cap}</p>
            </div>
            <p className="mt-4 border-t pt-4"><span className="font-semibold">Summary:</span> {report.summary}</p>

            <h3 className="text-lg font-semibold mt-6 mb-2 text-gray-800">Raw Data (from backend)</h3>
            <pre className="bg-gray-800 text-yellow-300 p-4 rounded-lg overflow-auto text-sm">
              {JSON.stringify(report, null, 2)}
            </pre>
          </div>
        )}

        {!report && !error && !loading && (
          <div className="text-center p-8 bg-gray-100 rounded-lg border border-dashed border-gray-300">
            <p className="text-gray-500 italic">Enter a stock ticker (e.g., GOOG, MSFT, AAPL) to fetch the report from the Django API.</p>
            <p className="text-xs mt-2 text-gray-400">Try 'ERR' to simulate a 503 server error from the backend.</p>
          </div>
        )}
      </div>
    </div>
  );
}