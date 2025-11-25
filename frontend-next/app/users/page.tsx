"use client";

import { useEffect, useState } from "react";
import { fetchFromAPI } from "../../lib/api";
//Create Users with python manage.py createsuperuser
export default function Users() {
  const [users, setUsers] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
      setMounted(true);
      fetchFromAPI("/api/users/")
            .then((res) => setUsers(res))
            .catch((err) => setError(err.message));
      }, []);
  if (!mounted) return null; // don’t render anything until client
  return (
    <div className="container">
      <h1>Users</h1>
      {error && <p className="error">{error}</p>}
      {users.length > 0 ? (
        <pre>{JSON.stringify(users, null, 2)}</pre>
      ) : (
        !error && <p>Loading...</p>
      )}
    </div>
  );
}
