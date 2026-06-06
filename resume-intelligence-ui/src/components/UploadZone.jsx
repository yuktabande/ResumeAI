import { useDropzone } from "react-dropzone";
import { Upload } from "lucide-react";

export default function UploadZone({ onFileAccepted, file }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { "application/pdf": [".pdf"] },
    maxFiles: 1,
    onDropAccepted: (files) => onFileAccepted(files[0]),
  });

  return (
    <div
      {...getRootProps()}
      style={{
        border: `2px dashed ${isDragActive ? "var(--primary)" : "var(--border)"}`,
        borderRadius: "var(--radius)",
        padding: "2.5rem",
        textAlign: "center",
        cursor: "pointer",
        background: isDragActive ? "var(--primary-light)" : "var(--surface)",
        transition: "all 0.2s",
      }}
    >
      <input {...getInputProps()} />
      <Upload
        size={36}
        color={isDragActive ? "var(--primary)" : "var(--text-secondary)"}
        style={{ margin: "0 auto 12px" }}
      />
      {file ? (
        <div>
          <p style={{ fontWeight: 600, color: "var(--primary)" }}>
            {file.name}
          </p>
          <p
            style={{
              fontSize: 13,
              color: "var(--text-secondary)",
              marginTop: 4,
            }}
          >
            Click or drag to replace
          </p>
        </div>
      ) : (
        <div>
          <p style={{ fontWeight: 600, color: "var(--text)" }}>
            {isDragActive
              ? "Drop your resume here"
              : "Drag & drop your resume PDF"}
          </p>
          <p
            style={{
              fontSize: 13,
              color: "var(--text-secondary)",
              marginTop: 4,
            }}
          >
            or click to browse
          </p>
        </div>
      )}
    </div>
  );
}
