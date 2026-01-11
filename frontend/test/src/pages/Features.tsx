import "./Features.css";

function Features() {
  return (
    <section className="features">
      <h2>Why Skill Bridge?</h2>

      <div className="feature-grid">
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
  );
}

export default Features;
