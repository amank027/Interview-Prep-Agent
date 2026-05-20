import { useState } from "react";
import { startInterview } from "../api/client";
import { useSession } from "../context/SessionContext";
import { useNavigate } from "react-router-dom";

const TYPES = [
  { value: "technical", label: "Technical", desc: "DSA, system design, coding concepts" },
  { value: "behavioral", label: "Behavioral", desc: "STAR-method, soft skills" },
  { value: "mixed", label: "Mixed", desc: "Blend of both" },
];

export default function InterviewSetup({ onStart }) {
  const { sessionId, hasResume, setInterviewId } = useSession();
  const [type, setType] = useState("technical");
  const [numQ, setNumQ] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleStart = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await startInterview(sessionId, type, numQ);
      setInterviewId(res.data.interview_id);
      onStart(res.data);
    } catch (e) {
      setError(e.response?.data?.detail || "Failed to start interview");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card max-w-lg mx-auto">
      <h2 className="text-lg font-semibold text-white mb-1">Start Mock Interview</h2>
      <p className="text-sm text-gray-400 mb-6">Questions are generated from your resume and JD.</p>

      {!hasResume && (
        <div className="bg-yellow-900/30 border border-yellow-800 text-yellow-300 text-sm rounded-lg px-4 py-3 mb-4">
          ⚠ Upload your resume first to generate personalized questions.
        </div>
      )}

      <div className="space-y-5">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">Interview Type</label>
          <div className="grid grid-cols-3 gap-2">
            {TYPES.map((t) => (
              <button
                key={t.value}
                onClick={() => setType(t.value)}
                className={`p-3 rounded-lg border text-left transition-all ${type === t.value ? "border-blue-500 bg-blue-950/40" : "border-gray-700 hover:border-gray-500"}`}
              >
                <p className="text-sm font-medium text-white">{t.label}</p>
                <p className="text-xs text-gray-500 mt-0.5">{t.desc}</p>
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-2">
            Number of Questions <span className="text-blue-400 font-bold">{numQ}</span>
          </label>
          <input
            type="range" min={3} max={10} value={numQ}
            onChange={(e) => setNumQ(+e.target.value)}
            className="w-full accent-blue-500"
          />
          <div className="flex justify-between text-xs text-gray-600 mt-1"><span>3</span><span>10</span></div>
        </div>

        {error && <p className="text-sm text-red-400">{error}</p>}

        <button onClick={handleStart} disabled={loading || !hasResume} className="btn-primary w-full py-2.5">
          {loading ? (
            <span className="flex items-center justify-center gap-2">
              <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Generating questions…
            </span>
          ) : "Start Interview"}
        </button>
      </div>
    </div>
  );
}
