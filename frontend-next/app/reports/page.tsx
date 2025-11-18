"use client";

import { useEffect, useState } from "react";
import { fetchFromAPI } from "../../lib/api";

export default function Reports() {
  const [reports, setReports] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchFromAPI("/api/reports/")
      .then((res) => setReports(res))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div className="container">
      <h1>Reports</h1>
      {error && <p className="error">{error}</p>}
      {reports.length > 0 ? (
        <pre>{JSON.stringify(reports, null, 2)}</pre>
      ) : (
        !error && <p>Loading...</p>
      )}
    </div>
  );
}
