import { useEffect } from "react";
import "./Landing.css";

function Landing() {

  useEffect(() => {
  const reveals = document.querySelectorAll(".reveal");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("active");
        }
      });
    },
    { threshold: 0.15 }
  );

  reveals.forEach((el) => observer.observe(el));

  return () => observer.disconnect();
}, []);

  return (
    <>
      {/* HERO */}
      <section className="hero">
        <div className="container">
          <h1>
            Forge  Your <span> Future Skills </span>
          </h1>

          <p>
            Upload your CV, Discover skill gaps, and Get a personalized roadmap
            to your dream career.
          </p>

          <div className="actions">
          <button
  className="primary"
  onClick={() =>
    document
      .getElementById("stats")
      ?.scrollIntoView({ behavior: "smooth" })
  }
>
  Get Started
</button>
            <button
  className="secondary"
  onClick={() => {
    document.getElementById("features")?.scrollIntoView({
      behavior: "smooth"
    });
  }}
>
  Explore Features
</button>
          </div>
        </div>
      </section>

      {/* FEATURES */}
    <section className="features reveal" id="features">
        <div className="container features-grid">
          <div className="feature-card">
            <h3>Skill Gap Analysis</h3>
            <p>Identify missing skills based on your career goals.</p>
          </div>

          <div className="feature-card">
            <h3>Personalized Roadmap</h3>
            <p>Get a step-by-step learning path tailored to you.</p>
          </div>

          <div className="feature-card">
            <h3>Career Matching</h3>
            <p>Match your skills with real job opportunities.</p>
          </div>
        </div>
      </section>
{/* WHY SKILL BRIDGE */}
<section className="why reveal">
  <div className="container">
    <h2>Why Skill Bridge?</h2>
    <p className="why-subtitle">
      We don’t just show you courses — We guide you with clarity, structure,
      and real career outcomes.
    </p>

    <div className="why-grid">
      <div className="why-card">
        <h3>AI-Driven Insights</h3>
        <p>
          Your CV and goals are analyzed to identify real, job-ready skill gaps.
        </p>
      </div>

      <div className="why-card">
        <h3>Clear Learning Path</h3>
        <p>
          No confusion, no overload — just a step-by-step roadmap that works.
        </p>
      </div>

      <div className="why-card">
        <h3>Career-Focused</h3>
        <p>
          Every recommendation is aligned with real hiring requirements.
        </p>
      </div>
    </div>
  </div>
</section>
      {/* STATS */}
     <section className="stats reveal" id="stats">
        <div className="container stats-grid">
          <div className="stat-box">
            <h3>50K+</h3>
            <p>Career Paths Built</p>
          </div>

          <div className="stat-box">
            <h3>98%</h3>
            <p>Skill Match Rate</p>
          </div>

          <div className="stat-box">
            <h3>10K+</h3>
            <p>Jobs Matched</p>
          </div>
        </div>
      </section>
    </>
  );
}

export default Landing;

