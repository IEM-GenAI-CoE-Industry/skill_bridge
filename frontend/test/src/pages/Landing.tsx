import { useState, useEffect } from "react";
import "./Landing.css";

function Landing() {
const [cvFile, setCvFile] = useState<File | null>(null);
const [isAnalyzing, setIsAnalyzing] = useState(false);
const [showSkillModal, setShowSkillModal] = useState(false);

const [missingSkills, setMissingSkills] = useState<string[]>([
  "Python",
  "SQL",
  "React"
]);

const [selectedSkills, setSelectedSkills] = useState<string[]>([]);


  // Scroll reveal animation
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
      {/* LOADING OVERLAY */}
      {isAnalyzing && (
        <div className="loading-overlay">
          <div className="loader-card">
            <div className="spinner"></div>
            <p>Analyzing skill gaps...</p>
          </div>
        </div>
      )}

      {/* HERO */}
      <section className="hero">
        <div className="container">
          <h1>
            Forge Your <span>Future Skills</span>
          </h1>

          <p>
            Upload your CV, discover skill gaps, and get a personalized roadmap
            to your dream career.
          </p>

          <div className="actions">
            <button
              className="primary"
              onClick={() =>
                document
                  .getElementById("cv-upload")
                  ?.scrollIntoView({ behavior: "smooth" })
              }
            >
              Get Started
            </button>

            <button
              className="secondary"
              onClick={() =>
                document
                  .getElementById("features")
                  ?.scrollIntoView({ behavior: "smooth" })
              }
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

      {/* CV UPLOAD */}
      <section className="cv-upload reveal" id="cv-upload">
        <div className="container">
          <h2>Upload Your CV</h2>
          <p>Upload your resume to analyze your skill gaps</p>

          <label className="upload-box">
            <input
              type="file"
              accept=".pdf,.doc,.docx"
              hidden
              onChange={(e) => {
                if (e.target.files && e.target.files[0]) {
                  setCvFile(e.target.files[0]);
                }
              }}
            />

            {!cvFile ? (
              <span>Drag & drop your CV here or click to upload</span>
            ) : (
              <span className="uploaded">✅ {cvFile.name}</span>
            )}
          </label>

          <button
            className="analyze-btn"
            disabled={!cvFile || isAnalyzing}
            onClick={() => {
  setIsAnalyzing(true);

  setTimeout(() => {
    setIsAnalyzing(false);
    setShowSkillModal(true); // open modal
  }, 2500);
}}

          >
            {isAnalyzing ? "Analyzing..." : "Analyze My Profile"}
          </button>
        </div>
      </section>

      {/* WHY SKILL BRIDGE */}
      <section className="why reveal">
        <div className="container">
          <h2>Why Skill Bridge?</h2>
          <p className="why-subtitle">
            We don’t just show you courses — we guide you with clarity, structure,
            and real career outcomes.
          </p>

          <div className="why-grid">
            <div className="why-card">
              <h3>AI-Driven Insights</h3>
              <p>Your CV is analyzed to identify job-ready skill gaps.</p>
            </div>

            <div className="why-card">
              <h3>Clear Learning Path</h3>
              <p>No confusion, no overload — just a focused roadmap.</p>
            </div>

            <div className="why-card">
              <h3>Career-Focused</h3>
              <p>Every recommendation aligns with real hiring needs.</p>
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

      {showSkillModal && (
  <div className="skill-modal-overlay">
    <div className="skill-modal">
      <h2>Let’s verify your skills</h2>
      <p>
        The AI identified these skills as missing from your CV.
        Do you already know any of them?
      </p>

      <div className="skill-list">
        {missingSkills.map((skill) => (
          <label key={skill} className="skill-item">
            <input
              type="checkbox"
              checked={selectedSkills.includes(skill)}
              onChange={() => {
                setSelectedSkills((prev) =>
                  prev.includes(skill)
                    ? prev.filter((s) => s !== skill)
                    : [...prev, skill]
                );
              }}
            />
            <span>{skill}</span>
          </label>
        ))}
      </div>

      <button
        className="confirm-btn"
        onClick={() => {
          console.log("Known skills:", selectedSkills);
          console.log(
            "Learning roadmap:",
            missingSkills.filter((s) => !selectedSkills.includes(s))
          );

          setShowSkillModal(false);
          alert("Next: Redirect to dashboard 🚀");
        }}
      >
        Confirm & Generate Roadmap
      </button>
    </div>
  </div>
)}

    </>
  );
}

export default Landing;
