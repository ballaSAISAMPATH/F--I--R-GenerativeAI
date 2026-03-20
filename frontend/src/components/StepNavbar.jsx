import { useNavigate } from "react-router-dom";

/**
 * StepNavbar
 * ───────────
 * Minimal top bar used on /step-1 and /step-2.
 * Shows the FIR logo + current step label + exit link.
 */
export default function StepNavbar({ currentStep }) {
  const navigate = useNavigate();

  return (
    <nav className="step-navbar no-print">
      <div className="step-navbar-inner">
        {/* Logo */}
        <button className="nav-logo" onClick={() => navigate("/")}>
          <div className="nav-logo-icon">F</div>
          <span className="nav-logo-text">FIR</span>
        </button>

        {/* Current step label */}
        <span className="step-navbar-label">
          {currentStep === 1 ? "Step 1 — Describe Incident" : "Step 2 — Review Report"}
        </span>

        {/* Exit */}
        <button className="step-navbar-exit" onClick={() => navigate("/")}>
          ✕ Exit
        </button>
      </div>
    </nav>
  );
}