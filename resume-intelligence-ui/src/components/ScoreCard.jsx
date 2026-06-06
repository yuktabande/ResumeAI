export default function ScoreCard({ result }) {
  const getColor = (score) => {
    if (score >= 75) return "#10b981";
    if (score >= 55) return "#f59e0b";
    if (score >= 35) return "#f97316";
    return "#ef4444";
  };

  const color = getColor(result.match_percentage);
  const circumference = 2 * Math.PI * 36;
  const offset =
    circumference - (result.match_percentage / 100) * circumference;

  return (
    <div
      style={{
        background: "var(--surface)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius)",
        padding: "1.25rem 1.5rem",
        display: "flex",
        alignItems: "center",
        gap: "1.25rem",
        boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
        transition: "transform 0.15s, box-shadow 0.15s",
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = "translateY(-2px)";
        e.currentTarget.style.boxShadow = "0 4px 16px rgba(0,0,0,0.1)";
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.boxShadow = "0 1px 3px rgba(0,0,0,0.05)";
      }}
    >
      <svg width="88" height="88" style={{ flexShrink: 0 }}>
        <circle
          cx="44"
          cy="44"
          r="36"
          fill="none"
          stroke="#f1f5f9"
          strokeWidth="8"
        />
        <circle
          cx="44"
          cy="44"
          r="36"
          fill="none"
          stroke={color}
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform="rotate(-90 44 44)"
          style={{ transition: "stroke-dashoffset 1s ease" }}
        />
        <text
          x="44"
          y="44"
          textAnchor="middle"
          dominantBaseline="central"
          fontSize="16"
          fontWeight="700"
          fill={color}
        >
          {result.match_percentage}%
        </text>
      </svg>

      <div style={{ flex: 1, minWidth: 0 }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            marginBottom: 4,
          }}
        >
          <p
            style={{
              fontWeight: 600,
              fontSize: 15,
              color: "var(--text)",
              overflow: "hidden",
              textOverflow: "ellipsis",
              whiteSpace: "nowrap",
            }}
          >
            {result.job_title}
          </p>
          <span
            style={{
              fontSize: 11,
              fontWeight: 600,
              padding: "2px 8px",
              borderRadius: 20,
              background: `${color}18`,
              color,
              whiteSpace: "nowrap",
            }}
          >
            {result.assessment}
          </span>
        </div>
        <p style={{ fontSize: 13, color: "var(--text-secondary)" }}>
          {result.company}
        </p>
        <div
          style={{
            marginTop: 8,
            height: 4,
            borderRadius: 2,
            background: "#f1f5f9",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              height: "100%",
              width: `${result.match_percentage}%`,
              background: `linear-gradient(90deg, ${color}88, ${color})`,
              borderRadius: 2,
              transition: "width 1s ease",
            }}
          />
        </div>
      </div>
    </div>
  );
}
