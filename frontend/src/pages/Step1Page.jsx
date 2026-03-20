import { useNavigate } from "react-router-dom";
import ChatSection from "../components/ChatSection";
import StepNavbar from "../components/StepNavbar";

/**
 * Step1Page  (/step-1)
 * ──────────────────────
 * Step 1: User describes the incident via chat / voice.
 * When the FIR report is ready, we persist it to sessionStorage
 * and navigate automatically to Step 2.
 */
export default function Step1Page() {
  const navigate = useNavigate();

  const handleFIRReady = (report) => {
    if (!report) return;
    // Pass the report to Step 2 via sessionStorage so it survives the navigation
    sessionStorage.setItem("firReport", JSON.stringify(report));
    navigate("/step-2");
  };

  return (
    <div className="app-shell step-page">
      <StepNavbar currentStep={1} />

      {/* Step progress bar */}
      <div className="step-progress-wrap no-print">
        <div className="step-progress-bar">
          <div className="step-progress-segment active">
            <div className="step-progress-circle active">1</div>
            <span className="step-progress-label">Describe Incident</span>
          </div>
          <div className="step-progress-connector" />
          <div className="step-progress-segment">
            <div className="step-progress-circle">2</div>
            <span className="step-progress-label">Review Report</span>
          </div>
        </div>
      </div>

      {/* Chat section handles all voice/text interaction */}
      <ChatSection onFIRReady={handleFIRReady} />
    </div>
  );
}