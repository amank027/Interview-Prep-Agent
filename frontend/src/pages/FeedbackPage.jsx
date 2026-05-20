import FeedbackDashboard from "../components/FeedbackDashboard";

export default function FeedbackPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Feedback & Roadmap</h1>
        <p className="text-gray-400 text-sm mt-1">Detailed analysis of your interview performance with a personalized learning roadmap.</p>
      </div>
      <FeedbackDashboard />
    </div>
  );
}
