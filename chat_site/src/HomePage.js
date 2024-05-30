// import logo from './logo.svg';
import './style/HomePage.css';
import React, { useState, useEffect } from 'react';
import TopBar from './TopBar';
import BottomButtons from './BottomButtons';
import ChatContainer from './ChatContainer';
import PlansModal from './PlansModal';
import {sendUserData} from './BotClient';
import axios from 'axios';

const HomePage = () => {
  const [showModal, setShowModal] = useState(false);
  const [IP, setIP] = useState('');
  const [gotIP, setGotIP] = useState(false);

  const handlePlansClicked = () => {
      setShowModal(true);
    };
    
    const getData = async () => {
      const res = await axios.get("https://api.ipify.org/?format=json");
      console.log('res: ');
      console.log(res.data);
      setIP(res.data['ip']);
      console.log('IP: ', IP);
      setGotIP(true);
    };

    useEffect(() => {
      console.log('inside useEffect')
      if (!gotIP) {
        getData();
      }
      if (gotIP) {
        
        setTimeout(async () => {
          try {
            setGotIP(true);
            const response = await sendUserData(IP);
            try{
                console.log( 'response: ', response);
                setGotIP(false);
            }
            catch(error){
                console.log('error response printing', error);
            }
  
          } catch (error) {
            console.error('There was an error getting the bot response:', error);
          }
              }, 500);
      }
      
      


      // Call the function to get user's geolocation when component mounts
      // getUserGeolocation();
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
