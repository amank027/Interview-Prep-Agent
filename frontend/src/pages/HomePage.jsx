import UploadPanel from "../components/UploadPanel";
import ChatInterface from "../components/ChatInterface";

export default function HomePage() {
  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Prepare for Your Interview</h1>
        <p className="text-gray-400 text-sm mt-1">Upload your resume and job description, then chat with AI to explore gaps, skills, and practice.</p>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-[320px_1fr] gap-4">
        <div className="space-y-4">
          <UploadPanel />
          <div className="card text-xs text-gray-500 space-y-2">
            <p className="font-medium text-gray-400">Tips</p>
            <p>• Ask "What skills am I missing for this role?"</p>
            <p>• Ask "Summarize my resume strengths"</p>
            <p>• Ask "What should I study for this JD?"</p>
          </div>
        </div>
        <ChatInterface />
      </div>
    </div>
  );
}
