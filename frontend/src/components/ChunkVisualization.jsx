import { useState } from "react";

export default function ChunkVisualization({ chunks }) {
  const [open, setOpen] = useState(false);

  if (!chunks || chunks.length === 0) return null;

  return (
    <div className="mt-2">
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-gray-300 transition-colors"
      >
        <span className={`transition-transform ${open ? "rotate-90" : ""}`}>▶</span>
        {chunks.length} source chunk{chunks.length > 1 ? "s" : ""} retrieved
      </button>

      {open && (
        <div className="mt-2 space-y-2 animate-slide-up">
          {chunks.map((chunk, i) => (
            <div key={i} className="bg-gray-800/60 border border-gray-700/50 rounded-lg p-3">
              <div className="flex items-center justify-between mb-1.5">
                <span className="badge-blue">{chunk.source}</span>
                <span className="text-xs text-gray-500">score: {chunk.score}</span>
              </div>
              <p className="text-xs text-gray-400 leading-relaxed line-clamp-3">
                {chunk.content}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
