// frontend/src/pages/Jobs.jsx
import React, { useEffect, useState } from "react";
import { supabase, isSupabaseConfigured } from "../lib/supabaseClient";

export default function Jobs() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchJobs() {
      if (!isSupabaseConfigured()) {
        setError("Supabase not configured. Set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.");
        setLoading(false);
        return;
      }

      try {
        // Use security-definer RPC to read jobs with anon key (bypasses RLS).
        const { data, error } = await supabase.rpc("get_latest_jobs", { p_limit: 50 });
        if (error) throw error;
        setJobs(data || []);
      } catch (err) {
        console.error("Error fetching jobs:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchJobs();
  }, []);

  const statusColor = (status) => {
    if (status === "completed") return "#2e7d32";
    if (status === "pending") return "#e65100";
    if (status === "failed") return "#c62828";
    return "#555";
  };

  return (
    <div>
      <h1>Jobber</h1>

      {loading && <p>Laster...</p>}
      {error && <p style={{ color: "red" }}>Feil: {error}</p>}

      {!loading && !error && (
        <div style={{
          background: "white",
          borderRadius: "8px",
          padding: "20px",
          marginTop: "20px",
          boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
        }}>
          <h2 style={{ marginTop: 0 }}>Siste jobber</h2>

          {jobs.length === 0 ? (
            <p>Ingen jobber funnet.</p>
          ) : (
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <thead>
                <tr style={{ borderBottom: "2px solid #ddd" }}>
                  <th style={thStyle}>ID</th>
                  <th style={thStyle}>Status</th>
                  <th style={thStyle}>Dato</th>
                </tr>
              </thead>
              <tbody>
                {jobs.map((j) => (
                  <tr key={j.id} style={{ borderBottom: "1px solid #eee" }}>
                    <td style={tdStyle}>{j.id}</td>
                    <td style={{ ...tdStyle, color: statusColor(j.status), fontWeight: "600" }}>
                      {j.status}
                    </td>
                    <td style={tdStyle}>
                      {j.created_at ? new Date(j.created_at).toLocaleDateString("no-NO") : "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}
    </div>
  );
}

const thStyle = {
  textAlign: "left",
  padding: "10px",
  color: "#666"
};

const tdStyle = {
  padding: "10px"
};
