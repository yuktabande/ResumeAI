import { useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import UploadZone from "../components/UploadZone";
import { createCandidate, uploadResume } from "../api/client";

export default function Home() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const inputStyle = {
    width: "100%",
    padding: "10px 14px",
    borderRadius: 8,
    border: "1px solid var(--border)",
    fontSize: 14,
    fontFamily: "inherit",
    outline: "none",
    transition: "border-color 0.15s",
  };

  const handleSubmit = async () => {
    if (!name || !email || !file) {
      toast.error("Please fill in all fields and upload your resume.");
      return;
    }
    setLoading(true);
    try {
      const candidate = await createCandidate(name, email);
      await uploadResume(candidate.id, file);
      toast.success("Resume uploaded successfully!");
      localStorage.setItem("candidate", JSON.stringify(candidate));
      navigate("/match", { state: { candidateId: candidate.id } });
    } catch (err) {
      const msg = err.response?.data?.detail || "Something went wrong.";
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
          Upload Your Resume
        </h1>
        <p style={{ color: "var(--text-secondary)", fontSize: 15 }}>
          Upload your resume and match it against job descriptions to see how
          well you fit.
        </p>
      </div>

      <div
        style={{
          background: "var(--surface)",
          borderRadius: "var(--radius)",
          border: "1px solid var(--border)",
          padding: "2rem",
          boxShadow: "var(--shadow)",
          display: "flex",
          flexDirection: "column",
          gap: "1.25rem",
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "1rem",
          }}
        >
          <div>
            <label
              style={{
                fontSize: 13,
                fontWeight: 500,
                color: "var(--text)",
                display: "block",
                marginBottom: 6,
              }}
            >
              Full Name
            </label>
            <input
              style={inputStyle}
              placeholder="Yukta Bande"
              value={name}
              onChange={(e) => setName(e.target.value)}
              onFocus={(e) => (e.target.style.borderColor = "var(--primary)")}
              onBlur={(e) => (e.target.style.borderColor = "var(--border)")}
            />
          </div>
          <div>
            <label
              style={{
                fontSize: 13,
                fontWeight: 500,
                color: "var(--text)",
                display: "block",
                marginBottom: 6,
              }}
            >
              Email
            </label>
            <input
              style={inputStyle}
              placeholder="yukta@example.com"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onFocus={(e) => (e.target.style.borderColor = "var(--primary)")}
              onBlur={(e) => (e.target.style.borderColor = "var(--border)")}
            />
          </div>
        </div>

        <div>
          <label
            style={{
              fontSize: 13,
              fontWeight: 500,
              color: "var(--text)",
              display: "block",
              marginBottom: 6,
            }}
          >
            Resume PDF
          </label>
          <UploadZone onFileAccepted={setFile} file={file} />
        </div>

        <button
          onClick={handleSubmit}
          disabled={loading}
          style={{
            padding: "12px",
            borderRadius: 8,
            border: "none",
            background: loading
              ? "#c7d2fe"
              : "linear-gradient(135deg, #6366f1, #8b5cf6)",
            color: "white",
            fontWeight: 600,
            fontSize: 15,
            transition: "opacity 0.15s",
          }}
        >
          {loading ? "Uploading..." : "Upload Resume →"}
        </button>
      </div>
    </div>
  );
}
