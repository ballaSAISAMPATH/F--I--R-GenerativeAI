import { Routes, Route, Navigate } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import Step1Page from "./pages/Step1Page";
import Step2Page from "./pages/Step2Page";

function App() {
  return (
    <Routes>
      {/* Landing / Home */}
      <Route path="/" element={<LandingPage />} />

      {/* Auth pages */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignUpPage />} />

      {/* FIR filing steps */}
      <Route path="/step-1" element={<Step1Page />} />
      <Route path="/step-2" element={<Step2Page />} />

      {/* Legacy /auth redirect → /login */}
      <Route path="/auth" element={<Navigate to="/login" replace />} />

      {/* 404 fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;