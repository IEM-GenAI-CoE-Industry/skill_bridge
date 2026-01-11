import { useEffect } from "react";
import { useState } from "react";
import "./LoginModal.css";

type Props = {
  open: boolean;
  onClose: () => void;
};

function LoginModal({ open, onClose }: Props) {
  useEffect(() => {
  if (open) {
    document.body.style.overflow = "hidden";
  } else {
    document.body.style.overflow = "auto";
  }

  return () => {
    document.body.style.overflow = "auto";
  };
}, [open]);

useEffect(() => {
  const handleEsc = (e: KeyboardEvent) => {
    if (e.key === "Escape") {
      onClose();
    }
  };

  window.addEventListener("keydown", handleEsc);

  return () => {
    window.removeEventListener("keydown", handleEsc);
  };
}, [onClose]);

  const [mode, setMode] = useState<"login" | "signup">("login");

  if (!open) return null;

  return (
    <div className="login-overlay" onClick={onClose}>
      <div
        className="login-modal"
        onClick={(e) => e.stopPropagation()}
      >
        <button className="close-btn" onClick={onClose}>
          ×
        </button>

        <div className="auth-tabs">
          <button
            className={mode === "login" ? "active" : ""}
            onClick={() => setMode("login")}
          >
            Login
          </button>

          <button
            className={mode === "signup" ? "active" : ""}
            onClick={() => setMode("signup")}
          >
            Sign Up
          </button>
        </div>

        <h2>{mode === "login" ? "Welcome Back" : "Create Account"}</h2>
        <p>
          {mode === "login"
            ? "Login to continue"
            : "Start your journey with Skill Bridge"}
        </p>

        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />

        {mode === "signup" && (
          <input type="password" placeholder="Confirm Password" />
        )}

        <button className="login-submit">
          {mode === "login" ? "Login" : "Sign Up"}
        </button>
      </div>
    </div>
  );
}

export default LoginModal;
