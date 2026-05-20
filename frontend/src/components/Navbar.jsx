import { Link, useLocation } from "react-router-dom";
import { useSession } from "../context/SessionContext";

const links = [
  { to: "/", label: "Prepare" },
  { to: "/interview", label: "Interview" },
  { to: "/feedback", label: "Feedback" },
];

export default function Navbar() {
  const location = useLocation();
  const { hasResume, hasJD } = useSession();

  return (
    <nav className="border-b border-gray-800 bg-gray-950/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-blue-400 text-xl">⚡</span>
          <span className="font-semibold text-white tracking-tight">PrepAI</span>
        </div>

        <div className="flex items-center gap-1">
          {links.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                location.pathname === to
                  ? "bg-blue-600 text-white"
                  : "text-gray-400 hover:text-white hover:bg-gray-800"
              }`}
            >
              {label}
            </Link>
          ))}
        </div>

        <div className="flex items-center gap-2 text-xs text-gray-500">
          <span className={`w-2 h-2 rounded-full ${hasResume ? "bg-green-400" : "bg-gray-700"}`} />
          <span>Resume</span>
          <span className={`w-2 h-2 rounded-full ${hasJD ? "bg-green-400" : "bg-gray-700"}`} />
          <span>JD</span>
        </div>
      </div>
    </nav>
  );
}
