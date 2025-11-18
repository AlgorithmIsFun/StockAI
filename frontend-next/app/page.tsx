"use client";

import { useEffect, useState } from "react";
import { fetchFromAPI } from "../lib/api";

export default function Dashboard() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchFromAPI("/api/hello/")
      .then((res) => setData(res))
      .catch((err) => setError(err.message));
  }, []);

  // Make sure you have one single return statement and all JSX is wrapped
  return (
    <div className="container">
      <h1>Dashboard Home</h1>
      <h2>API Response:</h2>
      {error && <p className="error">Error: {error}</p>}
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
      {!data && !error && <p>Loading...</p>}
    </div>
  );
}
