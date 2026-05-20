import { useState, useRef, useEffect } from "react";
import { submitAnswer } from "../api/client";
import { useSession } from "../context/SessionContext";
import { useNavigate } from "react-router-dom";

export default function InterviewChat({ initData }) {
  const { sessionId, interviewId } = useSession();
  const navigate = useNavigate();
  const [messages, setMessages] = useState([
    { role: "assistant", content: initData.first_question },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState({ answered: 0, total: initData.total_questions });
  const [done, setDone] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const submit = async () => {
    const text = input.trim();
    if (!text || loading || done) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", content: text }]);
    setLoading(true);

    try {
      const res = await submitAnswer(sessionId, interviewId, text);
      const data = res.data;
      setProgress({ answered: data.questions_answered, total: data.total_questions });

      if (data.is_complete) {
        setDone(true);
        setMessages((m) => [...m, { role: "assistant", content: "Great job completing the interview! Your feedback is being prepared. 🎉" }]);
      } else {
        setMessages((m) => [...m, { role: "assistant", content: data.next_question }]);
      }
    } catch (e) {
      setMessages((m) => [...m, { role: "assistant", content: "Error submitting answer. Please try again." }]);
    } finally {
      setLoading(false);
    }
  };

  const pct = Math.round((progress.answered / progress.total) * 100);

  return (
    <div className="card flex flex-col h-[calc(100vh-12rem)]">
      <div className="flex items-center justify-between mb-3 shrink-0">
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Mock Interview</h2>
        <span className="text-xs text-gray-500">{progress.answered} / {progress.total} answered</span>
      </div>

      <div className="h-1.5 bg-gray-800 rounded-full mb-4 shrink-0">
        <div className="h-full bg-blue-600 rounded-full transition-all duration-500" style={{ width: `${pct}%` }} />
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 pr-1">
        {messages.map((msg, i) => {
          const isUser = msg.role === "user";
          return (
            <div key={i} className={`flex gap-3 animate-slide-up ${isUser ? "flex-row-reverse" : ""}`}>
              <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs shrink-0 font-medium ${isUser ? "bg-blue-600" : "bg-purple-700"}`}>
                {isUser ? "U" : "🤖"}
              </div>
              <div className={`max-w-[80%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${isUser ? "bg-blue-600 text-white rounded-tr-sm" : "bg-gray-800 text-gray-100 rounded-tl-sm"}`}>
                {msg.content}
              </div>
            </div>
          );
        })}
        {loading && (
          <div className="flex gap-3">
            <div className="w-7 h-7 rounded-full bg-purple-700 flex items-center justify-center text-xs shrink-0">🤖</div>
            <div className="bg-gray-800 rounded-2xl rounded-tl-sm px-4 py-3 flex gap-1">
              {[0,1,2].map(i => <span key={i} className="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: `${i*0.15}s` }} />)}
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="mt-4 shrink-0">
        {done ? (
          <button onClick={() => navigate("/feedback")} className="btn-primary w-full py-2.5">
            View Feedback & Roadmap →
          </button>
        ) : (
          <div className="flex gap-2">
            <textarea
              className="input text-sm resize-none"
              rows={2}
              placeholder="Type your answer…"
              value={input}
              disabled={loading}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && (e.preventDefault(), submit())}
            />
            <button onClick={submit} disabled={loading || !input.trim()} className="btn-primary px-4 shrink-0 self-end">
              Submit
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
