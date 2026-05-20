import { BrowserRouter, Routes, Route } from "react-router-dom";
import { SessionProvider } from "./context/SessionContext";
import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";
import InterviewPage from "./pages/InterviewPage";
import FeedbackPage from "./pages/FeedbackPage";

export default function App() {
  return (
    <BrowserRouter>
      <SessionProvider>
        <div className="min-h-screen bg-gray-950">
          <Navbar />
          <main>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/interview" element={<InterviewPage />} />
              <Route path="/feedback" element={<FeedbackPage />} />
            </Routes>
          </main>
        </div>
      </SessionProvider>
    </BrowserRouter>
  );
}
