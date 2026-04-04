import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ReportSection from "../components/ReportSection";
import StepNavbar from "../components/StepNavbar";

/**
 * Step2Page  (/step-2)
 * ──────────────────────
 * Step 2: Review and download the generated FIR report.
 * Reads the report from sessionStorage (set by Step1Page).
 * If no report is found, redirects the user back to Step 1.
 */
export default function Step2Page() {
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = sessionStorage.getItem("firReport");
    if (stored) {
      try {
        setReport(JSON.parse(stored));
      } catch {
        navigate("/step-1", { replace: true });
      }
    } else {
      // No report available — send back to step 1
      navigate("/step-1", { replace: true });
    }
    setLoading(false);
  }, [navigate]);

  const handleFileAnother = () => {
    sessionStorage.removeItem("firReport");
    navigate("/step-1");
  };

  if (loading) {
    return (
      <div className="app-shell step-page step-loading">
        <div className="step-loading-spinner" />
        <p>Loading your report…</p>
      </div>
    );
  }

  return (
    <div className="app-shell step-page">
      <StepNavbar currentStep={2} />

      {/* Step progress bar */}
      <div className="step-progress-wrap no-print">
        <div className="step-progress-bar">
          <div className="step-progress-segment done">
            <div className="step-progress-circle done">✓</div>
            <span className="step-progress-label">Describe Incident</span>
          </div>
          <div className="step-progress-connector done" />
          <div className="step-progress-segment active">
            <div className="step-progress-circle active">2</div>
            <span className="step-progress-label">Review Report</span>
          </div>
        </div>
      </div>

      {/* Report Section renders the full IF1 form */}
      <ReportSection report={report} />

      {/* File Another FIR button */}
      <div className="step2-actions no-print">
        <button className="step2-restart-btn" onClick={handleFileAnother}>
          ↻ File Another FIR
        </button>
      </div>
    </div>
  );
}