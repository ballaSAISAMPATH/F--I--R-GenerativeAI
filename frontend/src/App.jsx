import { useState } from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HeroSection from "./components/HeroSection";
import HowItWorks from "./components/HowItWorks";
import ChatSection from "./components/ChatSection";
import ReportSection from "./components/ReportSection";
import Footer from "./components/Footer";
import AuthPage from "./components/AuthPage";

function HomePage() {
  const [firReport, setFirReport] = useState(null);

  return (
    <div className="app-shell">
      <Navbar />
      <HeroSection />
      <HowItWorks />
      <ChatSection onFIRReady={setFirReport} />
      <ReportSection report={firReport} />
      <Footer />
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/auth" element={<AuthPage />} />
    </Routes>
  );
}

export default App;