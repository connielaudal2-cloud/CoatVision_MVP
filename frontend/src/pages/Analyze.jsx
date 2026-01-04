// frontend/src/pages/Analyze.jsx
import React, { useState, useRef } from "react";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function Analyze() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files?.[0];
    if (file && file.type.startsWith("image/")) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError("Velg et bilde først");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // Convert file to base64
      const reader = new FileReader();
      reader.readAsDataURL(selectedFile);
      
      await new Promise((resolve, reject) => {
        reader.onload = () => resolve();
        reader.onerror = reject;
      });

      const base64String = reader.result.split(',')[1];

      // Call analyze endpoint
      const response = await fetch(`${API_BASE_URL}/api/analyze/base64`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ image: base64String }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Analyse mislyktes");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error("Analyse feil:", err);
      setError(err.message || "Noe gikk galt under analysen");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div>
      <h1 style={{ marginBottom: "10px" }}>Analyser Coating</h1>
      <p style={{ color: "#666", marginBottom: "30px" }}>
        Last opp et bilde av et panel for å analysere coating-kvalitet
      </p>

      {/* Upload area */}
      <div
        style={{
          background: "white",
          borderRadius: "8px",
          padding: "30px",
          marginBottom: "20px",
          boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
        }}
      >
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          style={{
            border: "2px dashed #ccc",
            borderRadius: "8px",
            padding: "40px",
            textAlign: "center",
            cursor: "pointer",
            transition: "border-color 0.2s",
          }}
          onClick={() => fileInputRef.current?.click()}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            style={{ display: "none" }}
          />
          
          {!previewUrl ? (
            <>
              <div style={{ fontSize: "3rem", marginBottom: "10px" }}>📷</div>
              <p style={{ margin: "10px 0", fontWeight: "bold" }}>
                Klikk for å velge bilde eller dra og slipp
              </p>
              <p style={{ color: "#999", fontSize: "0.9rem" }}>
                Støtter JPG, PNG, og andre bildeformater
              </p>
            </>
          ) : (
            <div>
              <img
                src={previewUrl}
                alt="Preview"
                style={{
                  maxWidth: "100%",
                  maxHeight: "300px",
                  borderRadius: "4px",
                  marginBottom: "10px",
                }}
              />
              <p style={{ color: "#666" }}>
                {selectedFile?.name}
              </p>
            </div>
          )}
        </div>

        {selectedFile && (
          <div style={{ marginTop: "20px", display: "flex", gap: "10px", justifyContent: "center" }}>
            <button
              onClick={handleAnalyze}
              disabled={loading}
              style={{
                background: loading ? "#ccc" : "#1a1a2e",
                color: "white",
                border: "none",
                padding: "12px 24px",
                borderRadius: "4px",
                cursor: loading ? "not-allowed" : "pointer",
                fontSize: "1rem",
                fontWeight: "600",
              }}
            >
              {loading ? "Analyserer..." : "Analyser Coating"}
            </button>
            
            <button
              onClick={handleReset}
              disabled={loading}
              style={{
                background: "white",
                color: "#1a1a2e",
                border: "1px solid #1a1a2e",
                padding: "12px 24px",
                borderRadius: "4px",
                cursor: loading ? "not-allowed" : "pointer",
                fontSize: "1rem",
              }}
            >
              Nullstill
            </button>
          </div>
        )}

        {error && (
          <div style={{
            marginTop: "20px",
            padding: "15px",
            background: "#fee",
            color: "#c33",
            borderRadius: "4px",
            textAlign: "center",
          }}>
            {error}
          </div>
        )}
      </div>

      {/* Results */}
      {result && (
        <div
          style={{
            background: "white",
            borderRadius: "8px",
            padding: "30px",
            boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
          }}
        >
          <h2 style={{ marginTop: 0, marginBottom: "20px" }}>Analyseresultater</h2>

          {/* Main Metrics */}
          <div style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "20px",
            marginBottom: "30px",
          }}>
            {result.metrics?.cvi !== undefined && (
              <MetricCard
                title="CVI"
                subtitle="Coating Visual Index"
                value={result.metrics.cvi}
                unit="%"
              />
            )}
            {result.metrics?.cqi !== undefined && (
              <MetricCard
                title="CQI"
                subtitle="Coating Quality Index"
                value={result.metrics.cqi}
                unit="%"
              />
            )}
            {result.metrics?.coverage !== undefined && (
              <MetricCard
                title="Dekning"
                subtitle="Coverage"
                value={result.metrics.coverage}
                unit="%"
              />
            )}
          </div>

          {/* Additional Metrics */}
          <div style={{
            background: "#f9f9f9",
            padding: "20px",
            borderRadius: "8px",
          }}>
            <h3 style={{ marginTop: 0, marginBottom: "15px", fontSize: "1rem" }}>
              Detaljerte metrikker
            </h3>
            <div style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
              gap: "10px",
              fontSize: "0.9rem",
            }}>
              {result.metrics?.color_uniformity !== undefined && (
                <MetricRow label="Fargeuniformitet" value={result.metrics.color_uniformity} unit="%" />
              )}
              {result.metrics?.smoothness !== undefined && (
                <MetricRow label="Glatthet" value={result.metrics.smoothness} unit="%" />
              )}
              {result.metrics?.edge_density !== undefined && (
                <MetricRow label="Kanttetthet" value={result.metrics.edge_density} unit="%" />
              )}
              {result.metrics?.saturation_score !== undefined && (
                <MetricRow label="Metning" value={result.metrics.saturation_score} unit="%" />
              )}
              {result.metrics?.brightness_score !== undefined && (
                <MetricRow label="Lysstyrke" value={result.metrics.brightness_score} unit="%" />
              )}
              {result.metrics?.laplacian_variance !== undefined && (
                <MetricRow label="Laplacian Varians" value={result.metrics.laplacian_variance} />
              )}
            </div>
            
            {result.metrics?.note && (
              <p style={{ marginTop: "15px", color: "#666", fontStyle: "italic", fontSize: "0.85rem" }}>
                {result.metrics.note}
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// Helper component for main metric cards
function MetricCard({ title, subtitle, value, unit = "" }) {
  return (
    <div style={{
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      color: "white",
      padding: "20px",
      borderRadius: "8px",
      textAlign: "center",
    }}>
      <div style={{ fontSize: "0.85rem", opacity: 0.9, marginBottom: "5px" }}>
        {subtitle}
      </div>
      <div style={{ fontSize: "2rem", fontWeight: "bold", marginBottom: "5px" }}>
        {value}{unit}
      </div>
      <div style={{ fontSize: "1rem", fontWeight: "600" }}>
        {title}
      </div>
    </div>
  );
}

// Helper component for detailed metric rows
function MetricRow({ label, value, unit = "" }) {
  return (
    <div style={{
      display: "flex",
      justifyContent: "space-between",
      padding: "8px 0",
      borderBottom: "1px solid #eee",
    }}>
      <span style={{ fontWeight: "500" }}>{label}:</span>
      <span style={{ color: "#666" }}>{value}{unit}</span>
    </div>
  );
}
