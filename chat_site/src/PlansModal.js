import React from 'react';
import './style/PlansModal.css';
function PlansModal({ onClose }) {
    return (
        <div className="modal">
          <div className="modal-content">
            <h2>Choose a plan</h2>
            <button className="closeButton" onClick={onClose}>Close</button>
            <div className="plan-types">
              <div className="plan">
                <h3>Basic Plan</h3>
                <p>Description of basic plan</p>
                <button>Choose</button>
              </div>
              <div className="plan">
                <h3>Premium Plan</h3>
                <p>Description of premium plan</p>
                <button>Choose</button>
              </div>
            </div>
          </div>
        </div>
      );
    }
  
export default PlansModal  