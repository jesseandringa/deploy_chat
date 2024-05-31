import React from "react";
import "./style/TopBar.css";
const TopBar = () => {
    // Define a function to handle button clicks
    const handleButtonClick = (buttonName) => {
      // Handle button click logic here
      console.log(`Clicked ${buttonName} button`);
    };
  
    return (
        <div className="top-container">
            <div className = "sign-in-up">
                <button onClick={() => window.location.href = '/sign-up-sign-in'}>Sign Up/In</button>
            </div>
            <div className="name-and-description">
                <h1 id="website-name" onClick={() => window.location.href = '/'}>Muni</h1>
                <h2 id="website-description">Your own personal municipal assistant</h2>
            </div>
            
            <div className="top-bar">
                {/* Each button is a separate component */}
                <button onClick={() => window.location.href = '/how-it-works'}>How It Works</button>
                <button id ="center-button" onClick={() => window.location.href = '/features'}>Features</button>
                <button onClick={() => window.location.href = '/about-us'}>About Us</button>
                {/* Add more buttons as needed */}
            </div>
            
        </div>
    );
  };
  
  export default TopBar;