import { Link, useLocation } from "react-router-dom";

export default function Layout({ children }) {
  const location = useLocation();

  const navItems = [
    { path: "/", label: "Upload" },
    { path: "/match", label: "Match" },
  ];

  return (
    <div style={{ minHeight: "100vh", background: "var(--bg)" }}>
      <nav
        style={{
          background: "var(--surface)",
          borderBottom: "1px solid var(--border)",
          padding: "0 2rem",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          height: "64px",
          position: "sticky",
          top: 0,
          zIndex: 100,
          boxShadow: "0 1px 3px rgba(0,0,0,0.06)",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <div
            style={{
              width: 32,
              height: 32,
              background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
              borderRadius: 8,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "white",
              fontWeight: 700,
              fontSize: 16,
            }}
          >
            R
          </div>
          <span style={{ fontWeight: 700, fontSize: 18, color: "var(--text)" }}>
            ResumeIQ
          </span>
        </div>

        <div style={{ display: "flex", gap: "4px" }}>
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              style={{
                padding: "8px 16px",
                borderRadius: 8,
                textDecoration: "none",
                fontWeight: 500,
                fontSize: 14,
                color:
                  location.pathname === item.path
                    ? "var(--primary)"
                    : "var(--text-secondary)",
                background:
                  location.pathname === item.path
                    ? "var(--primary-light)"
                    : "transparent",
                transition: "all 0.15s",
              }}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </nav>

      <main
        style={{ maxWidth: 860, margin: "0 auto", padding: "2.5rem 1.5rem" }}
      >
        {children}
      </main>
    </div>
  );
}
