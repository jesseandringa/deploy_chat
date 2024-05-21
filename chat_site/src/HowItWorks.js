// import logo from './logo.svg';
import './style/HowItWorks.css';
import React, { useState } from 'react';
import TopBar from './TopBar';
import BottomButtons from './BottomButtons';
// import ChatContainer from './ChatContainer';
import PlansModal from './PlansModal';
// import ChatContainer from './ChatContainer';

const HowItWorks = () => {
  const [showModal, setShowModal] = useState(false);

  const handlePlansClicked = () => {
      setShowModal(true);
    };
  

  return (
    <>
    <div className = "container">
      
      {/* {!showModal && ( */}
      <div>
        <TopBar />
        <div className="how-it-works">
            <h1>How It Works</h1>
            <p> Muni let’s you access the information you need, faster. With access to all of the information on the (Salt Lake county) municipal website of your choosing, we have created a digital assistant, to help you answer those questions regarding zoning, codes, laws, and more. Not only do we provide the summarized information you’re looking for, but we also provide the location, and source of the documents. Here’s how it works! </p>
            <div className="how-it-works-steps">
                <p>Step 1: Select your municipality. </p>

                <p>Step 2: Ask your question.</p>

                <p>Step 3: Use the provided links to do further research, or ask another question! </p>
            </div>
            <button id ="chat-button" onClick={() => window.location.href = '/'}>Chat</button>
        </div>
      <BottomButtons onPlansClicked={handlePlansClicked}/>
      </div>
      {/* )} */}
     

    </div>
    {showModal && <PlansModal className ="plans-modal" onClose={() => setShowModal(false)} />}
    </>
  );
};

export default HowItWorks;
