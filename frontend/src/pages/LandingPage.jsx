import Navbar from "../components/Navbar";
import HeroSection from "../components/HeroSection";
import HowItWorks from "../components/HowItWorks";
import Footer from "../components/Footer";

/**
 * LandingPage
 * ────────────
 * Public marketing / home page.
 * Chat + Report have moved to /step-1 and /step-2.
 */
export default function LandingPage() {
  return (
    <div className="app-shell">
      <Navbar />
      <HeroSection />
      <HowItWorks />
      <Footer />
    </div>
  );
}