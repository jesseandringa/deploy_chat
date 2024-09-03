// import logo from './logo.svg';
import './style/HomePage.css';
import React, { useState, useEffect } from 'react';
import TopBar from './TopBar';
import BottomButtons from './BottomButtons';
import ChatContainer from './ChatContainer';
import PlansModal from './PlansModal';
import axios from 'axios';

const HomePage = () => {
  const [showModal, setShowModal] = useState(false);
  const [IP, setIP] = useState('');
  const [gotIP, setGotIP] = useState(false);

  const handlePlansClicked = () => {
      setShowModal(true);
    };
    

  return (
    <>
    <div className = "container">
      
      {/* {!showModal && ( */}
      <div>
        <TopBar />
      <ChatContainer />
      <div className ="example-questions">
        <h2>Example Questions</h2>
        <ul>
          <li>How do I get a permit to build an ADU? </li>
          <li>Am I allowed to collect rain water?</li>
          <li>What are the building requirements for a new garage?</li>
        </ul>
      </div>
      <BottomButtons onPlansClicked={handlePlansClicked}/>
      </div>
      {/* )} */}
     

    </div>
    {showModal && <PlansModal className ="plans-modal" onClose={() => setShowModal(false)} />}
    </>
  );
};

export default HomePage;
