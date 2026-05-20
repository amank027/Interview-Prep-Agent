import { useState, useRef, useEffect } from "react";
import { ragQuery } from "../api/client";
import { useSession } from "../context/SessionContext";
import ChunkVisualization from "./ChunkVisualization";

function Message({ msg }) {
  const isUser = msg.role === "user";
  return (
    <div className={`flex gap-3 animate-slide-up ${isUser ? "flex-row-reverse" : ""}`}>
      <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs shrink-0 ${isUser ? "bg-blue-600" : "bg-gray-700"}`}>
        {isUser ? "U" : "AI"}
      </div>
      <div className={`max-w-[80%] ${isUser ? "items-end" : "items-start"} flex flex-col gap-1`}>
        <div className={`px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${isUser ? "bg-blue-600 text-white rounded-tr-sm" : "bg-gray-800 text-gray-100 rounded-tl-sm"}`}>
          <span className="whitespace-pre-wrap">{msg.content}</span>
        </div>
        {msg.chunks && <ChunkVisualization chunks={msg.chunks} />}
      </div>
    </div>
  );
}

export default function ChatInterface() {
  const { sessionId, hasResume, hasJD } = useSession();
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Hi! Upload your resume and job description, then ask me anything — I'll answer using your documents." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const canChat = hasResume || hasJD;

  const send = async () => {
    const text = input.trim();
    if (!text || loading || !canChat) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", content: text }]);
    setLoading(true);
    try {
      const res = await ragQuery(sessionId, text);
      setMessages((m) => [
        ...m,
        { role: "assistant", content: res.data.answer, chunks: res.data.retrieved_chunks },
      ]);
    } catch (e) {
      setMessages((m) => [
        ...m,
        { role: "assistant", content: `Error: ${e.response?.data?.detail || "Something went wrong"}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card flex flex-col h-[calc(100vh-20rem)] min-h-[400px]">
      <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4 shrink-0">Chat</h2>

      <div className="flex-1 overflow-y-auto space-y-4 pr-1">
        {messages.map((msg, i) => <Message key={i} msg={msg} />)}
        {loading && (
          <div className="flex gap-3 animate-fade-in">
            <div className="w-7 h-7 rounded-full bg-gray-700 flex items-center justify-center text-xs shrink-0">AI</div>
            <div className="bg-gray-800 rounded-2xl rounded-tl-sm px-4 py-3">
              <div className="flex gap-1">
                {[0, 1, 2].map((i) => (
                  <span key={i} className="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: `${i * 0.15}s` }} />
                ))}
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="mt-4 flex gap-2 shrink-0">
        <input
          className="input text-sm"
          placeholder={canChat ? "Ask about your resume or job requirements…" : "Upload documents first to start chatting"}
          value={input}
          disabled={!canChat || loading}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && send()}
        />
        <button onClick={send} disabled={!canChat || loading || !input.trim()} className="btn-primary px-4 shrink-0">
          Send
        </button>
      </div>
    </div>
  );
}
