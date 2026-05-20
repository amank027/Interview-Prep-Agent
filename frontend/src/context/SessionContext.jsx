import { createContext, useContext, useState, useCallback } from "react";
import { v4 as uuidv4 } from "uuid";

const SessionContext = createContext(null);

export function SessionProvider({ children }) {
  const [sessionId] = useState(() => uuidv4());
  const [hasResume, setHasResume] = useState(false);
  const [hasJD, setHasJD] = useState(false);
  const [interviewId, setInterviewId] = useState(null);

  const markResumeUploaded = useCallback(() => setHasResume(true), []);
  const markJDUploaded = useCallback(() => setHasJD(true), []);

  return (
    <SessionContext.Provider
      value={{
        sessionId,
        hasResume,
        hasJD,
        interviewId,
        setInterviewId,
        markResumeUploaded,
        markJDUploaded,
      }}
    >
      {children}
    </SessionContext.Provider>
  );
}

export const useSession = () => {
  const ctx = useContext(SessionContext);
  if (!ctx) throw new Error("useSession must be used inside SessionProvider");
  return ctx;
};
