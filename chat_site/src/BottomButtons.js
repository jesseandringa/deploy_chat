
import React from "react";
import "./style/BottomButtons.css";
const BottomButtons = ( {onPlansClicked} ) => {
    // Define a function to handle button clicks
    const handleButtonClick = (buttonName) => {
      // Handle button click logic here
      console.log(`Clicked ${buttonName} button`);
    };
    const handlePlansClicked = () => {
        onPlansClicked();
    };
  
    return (
        <div className="bottom-container">
            <div className="bottom-bar">
                {/* Each button is a separate component */}
                <button onClick={() => window.location.href = '/contact-us'}>Leave us Feedback</button>
                <button id ="plans-button" onClick={handlePlansClicked}>Plans</button>
                <button onClick={() => window.location.href = '/contact-us'}>Contact us</button>
                {/* Add more buttons as needed */}
            </div>
        </div>
    );
  };
  
  export default BottomButtons;