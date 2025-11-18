export async function fetchFromAPI(endpoint: string, options: RequestInit = {}) {
  const baseURL = "http://localhost:8000";

  const res = await fetch(`${baseURL}${endpoint}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }

  return res.json();
}
