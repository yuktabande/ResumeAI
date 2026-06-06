import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import toast from "react-hot-toast";
import { Plus, Trash2, Zap } from "lucide-react";
import { createJobDescription, bulkMatch } from "../api/client";

const emptyJD = () => ({ title: "", company: "", description_text: "" });

export default function Match() {
  const navigate = useNavigate();
  const location = useLocation();
  const stored = localStorage.getItem("candidate");
  const candidateId =
    location.state?.candidateId || (stored ? JSON.parse(stored).id : null);
  const [jds, setJds] = useState([emptyJD()]);
  const [loading, setLoading] = useState(false);

  const inputStyle = {
    width: "100%",
    padding: "9px 12px",
    borderRadius: 8,
    border: "1px solid var(--border)",
    fontSize: 13,
    fontFamily: "inherit",
    outline: "none",
  };

  const updateJD = (index, field, value) => {
    setJds((prev) =>
      prev.map((jd, i) => (i === index ? { ...jd, [field]: value } : jd)),
    );
  };

  const addJD = () => {
    if (jds.length >= 10) {
      toast.error("Maximum 10 job descriptions at once.");
      return;
    }
    setJds((prev) => [...prev, emptyJD()]);
  };

  const removeJD = (index) => {
    if (jds.length === 1) return;
    setJds((prev) => prev.filter((_, i) => i !== index));
  };

  const handleMatch = async () => {
    if (!candidateId) {
      toast.error("No resume found. Please upload your resume first.");
      navigate("/");
      return;
    }
    const valid = jds.every(
      (jd) => jd.title && jd.company && jd.description_text,
    );
    if (!valid) {
      toast.error("Please fill in all fields for every job description.");
      return;
    }
    setLoading(true);
    try {
      const createdJDs = await Promise.all(
        jds.map((jd) =>
          createJobDescription(jd.title, jd.company, jd.description_text),
        ),
      );
      const jdIds = createdJDs.map((jd) => jd.id);
      const results = await bulkMatch(candidateId, jdIds);
      navigate("/results", { state: { results } });
    } catch (err) {
      const msg = err.response?.data?.detail || "Matching failed.";
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div style={{ marginBottom: "2rem" }}>
        <h1
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: "var(--text)",
            marginBottom: 8,
          }}
        >
          Add Job Descriptions
        </h1>
        <p style={{ color: "var(--text-secondary)", fontSize: 15 }}>
          Paste in the job descriptions you want to match against. Add up to 10
          at once.
        </p>
      </div>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
          marginBottom: "1.5rem",
        }}
      >
        {jds.map((jd, index) => (
          <div
            key={index}
            style={{
              background: "var(--surface)",
              border: "1px solid var(--border)",
              borderRadius: "var(--radius)",
              padding: "1.5rem",
              boxShadow: "var(--shadow)",
            }}
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                marginBottom: "1rem",
              }}
            >
              <div
                style={{
                  fontSize: 12,
                  fontWeight: 600,
                  color: "var(--primary)",
                  background: "var(--primary-light)",
                  padding: "3px 10px",
                  borderRadius: 20,
                }}
              >
                JD {index + 1}
              </div>
              {jds.length > 1 && (
                <button
                  onClick={() => removeJD(index)}
                  style={{
                    background: "none",
                    border: "none",
                    color: "var(--text-secondary)",
                    padding: 4,
                  }}
                >
                  <Trash2 size={16} />
                </button>
              )}
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: "0.75rem",
                marginBottom: "0.75rem",
              }}
            >
              <input
                style={inputStyle}
                placeholder="Job Title"
                value={jd.title}
                onChange={(e) => updateJD(index, "title", e.target.value)}
              />
              <input
                style={inputStyle}
                placeholder="Company"
                value={jd.company}
                onChange={(e) => updateJD(index, "company", e.target.value)}
              />
            </div>
            <textarea
              style={{ ...inputStyle, height: 120, resize: "vertical" }}
              placeholder="Paste the full job description here..."
              value={jd.description_text}
              onChange={(e) =>
                updateJD(index, "description_text", e.target.value)
              }
            />
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: "0.75rem" }}>
        <button
          onClick={addJD}
          style={{
            flex: 1,
            padding: "11px",
            borderRadius: 8,
            border: "1px solid var(--border)",
            background: "var(--surface)",
            color: "var(--text)",
            fontWeight: 500,
            fontSize: 14,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 6,
          }}
        >
          <Plus size={16} /> Add Another JD
        </button>
        <button
          onClick={handleMatch}
          disabled={loading}
          style={{
            flex: 2,
            padding: "11px",
            borderRadius: 8,
            border: "none",
            background: loading
              ? "#c7d2fe"
              : "linear-gradient(135deg, #6366f1, #8b5cf6)",
            color: "white",
            fontWeight: 600,
            fontSize: 14,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 6,
          }}
        >
          <Zap size={16} /> {loading ? "Matching..." : "Match My Resume"}
        </button>
      </div>
    </div>
  );
}
