import { useLocation, useNavigate } from "react-router-dom";
import { ArrowLeft, Trophy } from "lucide-react";
import ScoreCard from "../components/ScoreCard";

export default function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const results = location.state?.results;

  if (!results) {
    navigate("/");
    return null;
  }

  const best = results.results[0];
  const avg = Math.round(
    results.results.reduce((sum, r) => sum + r.match_percentage, 0) /
      results.results.length,
  );

  return (
    <div>
      <button
        onClick={() => navigate("/match")}
        style={{
          display: "flex",
          alignItems: "center",
          gap: 6,
          background: "none",
          border: "none",
          color: "var(--text-secondary)",
          fontSize: 14,
          marginBottom: "1.5rem",
          padding: 0,
        }}
      >
        <ArrowLeft size={16} /> Back to matching
      </button>

      <div style={{ marginBottom: "2rem" }}>
        <h1
          style={{
            fontSize: 28,
            fontWeight: 700,
            color: "var(--text)",
            marginBottom: 8,
          }}
        >
          Your Results
        </h1>
        <p style={{ color: "var(--text-secondary)", fontSize: 15 }}>
          Matched against {results.total_jds_matched} job description
          {results.total_jds_matched > 1 ? "s" : ""}, ranked by relevance.
        </p>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: "1rem",
          marginBottom: "2rem",
        }}
      >
        <div
          style={{
            background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
            borderRadius: "var(--radius)",
            padding: "1.25rem 1.5rem",
            color: "white",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 8,
              marginBottom: 4,
            }}
          >
            <Trophy size={18} />
            <span style={{ fontSize: 13, fontWeight: 500, opacity: 0.9 }}>
              Best Match
            </span>
          </div>
          <p style={{ fontSize: 22, fontWeight: 700 }}>
            {best.match_percentage}%
          </p>
          <p style={{ fontSize: 13, opacity: 0.85, marginTop: 2 }}>
            {best.job_title} @ {best.company}
          </p>
        </div>

        <div
          style={{
            background: "var(--surface)",
            border: "1px solid var(--border)",
            borderRadius: "var(--radius)",
            padding: "1.25rem 1.5rem",
            boxShadow: "var(--shadow)",
          }}
        >
          <p
            style={{
              fontSize: 13,
              fontWeight: 500,
              color: "var(--text-secondary)",
              marginBottom: 4,
            }}
          >
            Average Score
          </p>
          <p style={{ fontSize: 22, fontWeight: 700, color: "var(--text)" }}>
            {avg}%
          </p>
          <p
            style={{
              fontSize: 13,
              color: "var(--text-secondary)",
              marginTop: 2,
            }}
          >
            across {results.total_jds_matched} roles
          </p>
        </div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        {results.results.map((result, index) => (
          <div
            key={index}
            style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}
          >
            <div
              style={{
                width: 24,
                height: 24,
                borderRadius: "50%",
                background:
                  index === 0
                    ? "linear-gradient(135deg, #6366f1, #8b5cf6)"
                    : "var(--border)",
                color: index === 0 ? "white" : "var(--text-secondary)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 11,
                fontWeight: 700,
                flexShrink: 0,
              }}
            >
              {index + 1}
            </div>
            <div style={{ flex: 1 }}>
              <ScoreCard result={result} />
            </div>
          </div>
        ))}
      </div>

      <button
        onClick={() => navigate("/")}
        style={{
          marginTop: "2rem",
          width: "100%",
          padding: "12px",
          borderRadius: 8,
          border: "1px solid var(--border)",
          background: "var(--surface)",
          color: "var(--text)",
          fontWeight: 600,
          fontSize: 14,
        }}
      >
        Start Over with a New Resume
      </button>
    </div>
  );
}
