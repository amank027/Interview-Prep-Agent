import { useState, useRef } from "react";
import { uploadResume, uploadJD } from "../api/client";
import { useSession } from "../context/SessionContext";

function UploadZone({ label, icon, accept, onUpload, uploaded, loading }) {
  const inputRef = useRef(null);
  const [dragging, setDragging] = useState(false);

  const handleFile = async (file) => {
    if (!file) return;
    await onUpload(file);
  };

  return (
    <div
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={(e) => { e.preventDefault(); setDragging(false); handleFile(e.dataTransfer.files[0]); }}
      className={`relative border-2 border-dashed rounded-xl p-6 cursor-pointer transition-all text-center
        ${dragging ? "border-blue-400 bg-blue-950/30" : uploaded ? "border-green-600 bg-green-950/20" : "border-gray-700 hover:border-gray-500 hover:bg-gray-800/40"}
        ${loading ? "opacity-60 pointer-events-none" : ""}
      `}
    >
      <input ref={inputRef} type="file" accept={accept} className="hidden" onChange={(e) => handleFile(e.target.files[0])} />
      <div className="text-3xl mb-2">{uploaded ? "✅" : icon}</div>
      <p className="font-medium text-sm text-gray-200">{label}</p>
      <p className="text-xs text-gray-500 mt-1">PDF or TXT · drag & drop or click</p>
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center rounded-xl bg-gray-950/60">
          <div className="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
        </div>
      )}
    </div>
  );
}

export default function UploadPanel({ onUploaded }) {
  const { sessionId, markResumeUploaded, markJDUploaded, hasResume, hasJD } = useSession();
  const [resumeLoading, setResumeLoading] = useState(false);
  const [jdLoading, setJdLoading] = useState(false);
  const [toast, setToast] = useState(null);

  const showToast = (msg, type = "success") => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3000);
  };

  const handleResume = async (file) => {
    setResumeLoading(true);
    try {
      const res = await uploadResume(sessionId, file);
      markResumeUploaded();
      showToast(`Resume indexed — ${res.data.chunks_stored} chunks stored`);
      onUploaded?.();
    } catch (e) {
      showToast(e.response?.data?.detail || "Upload failed", "error");
    } finally {
      setResumeLoading(false);
    }
  };

  const handleJD = async (file) => {
    setJdLoading(true);
    try {
      const res = await uploadJD(sessionId, file);
      markJDUploaded();
      showToast(`Job description indexed — ${res.data.chunks_stored} chunks stored`);
      onUploaded?.();
    } catch (e) {
      showToast(e.response?.data?.detail || "Upload failed", "error");
    } finally {
      setJdLoading(false);
    }
  };

  return (
    <div className="card">
      <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Documents</h2>
      <div className="grid grid-cols-2 gap-3">
        <UploadZone label="Resume" icon="📄" accept=".pdf,.txt" onUpload={handleResume} uploaded={hasResume} loading={resumeLoading} />
        <UploadZone label="Job Description" icon="💼" accept=".pdf,.txt" onUpload={handleJD} uploaded={hasJD} loading={jdLoading} />
      </div>
      {toast && (
        <div className={`mt-3 text-xs px-3 py-2 rounded-lg animate-fade-in ${toast.type === "error" ? "bg-red-900/50 text-red-300" : "bg-green-900/50 text-green-300"}`}>
          {toast.msg}
        </div>
      )}
    </div>
  );
}
