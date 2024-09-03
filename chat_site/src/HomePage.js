// import logo from './logo.svg';
import './style/HomePage.css';
import React, { useState, useEffect } from 'react';
import TopBar from './TopBar';
import BottomButtons from './BottomButtons';
import ChatContainer from './ChatContainer';
import PlansModal from './PlansModal';
import axios from 'axios';
import { useAuth0 } from '@auth0/auth0-react';
import {UpsertUser} from './BotClient';


const HomePage = () => {
  const [showModal, setShowModal] = useState(false);
  const [IP, setIP] = useState('');
  const [gotIP, setGotIP] = useState(false);
  const { isAuthenticated, isLoading, user } = useAuth0();
  const [userInfo, setUserInfo] = useState({});

  const handlePlansClicked = () => {
      setShowModal(true);
    };
    const getIpAddress = async () => {
       
      console.log('inside getIpAddress')
      const res = await axios.get("https://api.ipify.org/?format=json");
      // console.log('res: ');
      // console.log(res.data);
      setIP(res.data['ip']);
      setGotIP(true);
      if (isAuthenticated && !isLoading) {
          console.log("user: ", user);
          setUserInfo({"ip": res.data['ip'], 
                      "email": user.email,
                      "name": user.name,
                      "given_name": user.given_name,
                      "family_name": user.family_name});
      }
      else{
          setUserInfo({"ip": res.data['ip']});
      }
      setTimeout(async () => {
          try {
              setGotIP(true);
              const response = await UpsertUser(userInfo);
          }
          catch(error){
              console.log('error upserting user', error);
          }
      }, 500);
      
  }
  useEffect(() => {
      if (!isLoading){
        getIpAddress();
      }
  }, [isAuthenticated, isLoading, user, gotIP]);
    

  return (
    <>
    <div className = "container">
      
      {/* {!showModal && ( */}
      <div>
        <TopBar />
      <ChatContainer userInfo={userInfo}/>
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
