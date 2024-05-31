import React, { useState } from "react";
import "./style/SignUpSignIn.css";

const SignUpSignIn = ({ handleClose, isSignUp = false }) => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // Implement form submission logic here (e.g., send data to backend for signup/signin)
    console.log("Form Submitted:", formData);

    // After submission, you can close the modal (if applicable)
    handleClose?.();
  };

  return (
    <div className="signup-signin">
      <h2>{isSignUp ? "Sign Up" : "Sign In"}</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">{isSignUp ? "Sign Up" : "Sign In"}</button>
      </form>
    </div>
  );
};

export default SignUpSignIn;