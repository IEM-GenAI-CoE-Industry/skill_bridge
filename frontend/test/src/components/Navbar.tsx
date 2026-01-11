import { useState } from "react";
import "./Navbar.css";
import LoginModal from "./LoginModal";


function Navbar() {
  const [loginOpen, setLoginOpen] = useState(false);
  return (
    <header className="navbar">
      <div className="nav-container">
        <div className="logo">Skill Bridge</div>

        <div className="nav-actions">
         <button
  className="login-btn"
  onClick={() => setLoginOpen(true)}
>
  Login
</button>

        <button
  className="primary-btn"
  onClick={() =>
    document.getElementById("stats")?.scrollIntoView({ behavior: "smooth" })
  }
>
  Get Started
</button>
        </div>
      </div>
      <LoginModal
  open={loginOpen}
  onClose={() => setLoginOpen(false)}
/>

    </header>
  );
}

export default Navbar;

