// import logo from './logo.svg';
import './style/HomePage.css';
import React, { useState, useEffect } from 'react';
import TopBar from './TopBar';
import BottomButtons from './BottomButtons';
import ChatContainer from './ChatContainer';
import PlansModal from './PlansModal';
import {sendUserData} from './BotClient';
const HomePage = () => {
  const [showModal, setShowModal] = useState(false);
  
  const handlePlansClicked = () => {
      setShowModal(true);
    };
  
    useEffect(() => {
      // Function to get user's geolocation
      const getUserGeolocation = () => {
          navigator.geolocation.getCurrentPosition(position => {
              const { latitude, longitude } = position.coords;
              const userAgent = navigator.userAgent;

              setTimeout(async () => {
                try {
                  console.log('latitude: ', latitude)
                  console.log('longitude: ', longitude)
                  console.log('userAgent: ', userAgent)
                  const response = await sendUserData(longitude, latitude, userAgent);
                  try{
                      console.log( 'response: ', response);
                  }
                  catch(error){
                      console.log('error response printing', error);
                  }
      
                } catch (error) {
                  console.error('There was an error getting the bot response:', error);
                }
              }, 500);
      });
    }

      // Call the function to get user's geolocation when component mounts
      getUserGeolocation();
  }, []);
  

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
