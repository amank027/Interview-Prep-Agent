import { useState } from "react";
import InterviewSetup from "../components/InterviewSetup";
import InterviewChat from "../components/InterviewChat";

export default function InterviewPage() {
  const [interviewData, setInterviewData] = useState(null);

  return (
    <div className="max-w-3xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Mock Interview</h1>
        <p className="text-gray-400 text-sm mt-1">AI-generated questions tailored to your resume and target role.</p>
      </div>

      {!interviewData ? (
        <InterviewSetup onStart={setInterviewData} />
      ) : (
        <InterviewChat initData={interviewData} />
      )}
    </div>
  );
}
