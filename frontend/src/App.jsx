// frontend/src/App.jsx
// v2
import React from "react";
import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import Jobs from "./pages/Jobs";
import Agents from "./pages/Agents";
import Reports from "./pages/Reports";
import Analyze from "./pages/Analyze";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/analyze" element={<Analyze />} />
        <Route path="/jobs" element={<Jobs />} />
        <Route path="/agents" element={<Agents />} />
        <Route path="/reports" element={<Reports />} />
      </Routes>
    </Layout>
  );
}
