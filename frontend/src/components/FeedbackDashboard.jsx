import { useState, useEffect } from "react";
import { getFeedback } from "../api/client";
import { useSession } from "../context/SessionContext";

function ScoreRing({ score }) {
  const color = score >= 75 ? "text-green-400" : score >= 50 ? "text-yellow-400" : "text-red-400";
  return (
    <div className={`text-5xl font-bold ${color}`}>
      {score}<span className="text-2xl text-gray-500">/100</span>
    </div>
  );
}

function QuestionCard({ qf, index }) {
  const [open, setOpen] = useState(false);
  const scoreColor = qf.score >= 8 ? "badge-green" : qf.score >= 5 ? "badge-yellow" : "badge-red";

  return (
    <div className="border border-gray-800 rounded-xl overflow-hidden">
      <button
        onClick={() => setOpen(v => !v)}
        className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-gray-800/50 transition-colors"
      >
        <div className="flex items-center gap-3">
          <span className="text-xs text-gray-500 font-mono">Q{index + 1}</span>
          <span className="text-sm text-gray-200 line-clamp-1">{qf.question}</span>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <span className={scoreColor}>{qf.score}/10</span>
          <span className={`transition-transform text-gray-500 ${open ? "rotate-180" : ""}`}>▼</span>
        </div>
      </button>

      {open && (
        <div className="px-4 pb-4 space-y-3 border-t border-gray-800 pt-3 animate-slide-up">
          <div>
            <p className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Your Answer</p>
            <p className="text-sm text-gray-300 bg-gray-800/50 rounded-lg px-3 py-2">{qf.user_answer}</p>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <p className="text-xs text-green-500 mb-1.5 uppercase tracking-wider">✓ Strengths</p>
              <ul className="space-y-1">
                {qf.strengths.map((s, i) => <li key={i} className="text-xs text-gray-300">• {s}</li>)}
              </ul>
            </div>
            <div>
              <p className="text-xs text-yellow-500 mb-1.5 uppercase tracking-wider">↑ Improve</p>
              <ul className="space-y-1">
                {qf.improvements.map((s, i) => <li key={i} className="text-xs text-gray-300">• {s}</li>)}
              </ul>
            </div>
          </div>
          {qf.ideal_answer_hints && (
            <div>
              <p className="text-xs text-blue-400 mb-1 uppercase tracking-wider">💡 Ideal Answer Hints</p>
              <p className="text-xs text-gray-400">{qf.ideal_answer_hints}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function RoadmapCard({ item }) {
  const priorityBadge = item.priority === "High" ? "badge-red" : item.priority === "Medium" ? "badge-yellow" : "badge-green";
  return (
    <div className="card">
      <div className="flex items-start justify-between gap-2 mb-2">
        <h3 className="text-sm font-semibold text-white">{item.topic}</h3>
        <span className={priorityBadge}>{item.priority}</span>
      </div>
      <p className="text-xs text-gray-500 mb-2">⏱ {item.estimated_time}</p>
      <div className="space-y-1">
        {item.resources.map((r, i) => (
          <p key={i} className="text-xs text-gray-400">• {r}</p>
        ))}
      </div>
    </div>
  );
}

export default function FeedbackDashboard() {
  const { sessionId, interviewId } = useSession();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [tab, setTab] = useState("overview");

  useEffect(() => {
    if (!sessionId || !interviewId) return;
    setLoading(true);
    getFeedback(sessionId, interviewId)
      .then((res) => setData(res.data))
      .catch((e) => setError(e.response?.data?.detail || "Failed to load feedback"))
      .finally(() => setLoading(false));
  }, [sessionId, interviewId]);

  if (!interviewId) {
    return (
      <div className="card text-center py-16 text-gray-500">
        <p className="text-4xl mb-3">📊</p>
        <p>Complete a mock interview first to see your feedback.</p>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="card text-center py-16">
        <div className="w-10 h-10 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p className="text-gray-400">Analyzing your performance…</p>
        <p className="text-xs text-gray-600 mt-1">This may take a moment</p>
      </div>
    );
  }

  if (error) {
    return <div className="card text-center py-12 text-red-400">{error}</div>;
  }

  if (!data) return null;

  const TABS = [
    { id: "overview", label: "Overview" },
    { id: "questions", label: `Questions (${data.question_feedbacks.length})` },
    { id: "roadmap", label: `Roadmap (${data.roadmap.length})` },
  ];

  return (
    <div className="space-y-4 animate-fade-in">
      <div className="card">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <h2 className="text-lg font-semibold text-white mb-1">Interview Results</h2>
            <p className="text-sm text-gray-400">{data.overall_summary}</p>
          </div>
          <ScoreRing score={data.overall_score} />
        </div>

        <div className="grid grid-cols-2 gap-4 mt-5">
          <div>
            <p className="text-xs text-green-500 uppercase tracking-wider mb-2">✓ Strengths</p>
            <ul className="space-y-1">
              {data.strengths.map((s, i) => <li key={i} className="text-sm text-gray-300">• {s}</li>)}
            </ul>
          </div>
          <div>
            <p className="text-xs text-yellow-500 uppercase tracking-wider mb-2">↑ Areas to Improve</p>
            <ul className="space-y-1">
              {data.areas_for_improvement.map((s, i) => <li key={i} className="text-sm text-gray-300">• {s}</li>)}
            </ul>
          </div>
        </div>
      </div>

      <div className="flex gap-1 bg-gray-900 rounded-xl p-1 border border-gray-800">
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`flex-1 py-1.5 text-sm rounded-lg transition-colors font-medium ${tab === t.id ? "bg-blue-600 text-white" : "text-gray-400 hover:text-white"}`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === "overview" && (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {data.question_feedbacks.map((qf, i) => (
            <div key={i} className="card text-center">
              <p className="text-xs text-gray-500 mb-1">Q{i+1}</p>
              <p className={`text-2xl font-bold ${qf.score >= 8 ? "text-green-400" : qf.score >= 5 ? "text-yellow-400" : "text-red-400"}`}>{qf.score}<span className="text-sm text-gray-500">/10</span></p>
            </div>
          ))}
        </div>
      )}

      {tab === "questions" && (
        <div className="space-y-2">
          {data.question_feedbacks.map((qf, i) => <QuestionCard key={i} qf={qf} index={i} />)}
        </div>
      )}

      {tab === "roadmap" && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {data.roadmap.map((item, i) => <RoadmapCard key={i} item={item} />)}
        </div>
      )}
    </div>
  );
}
