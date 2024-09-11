// import logo from './logo.svg';
import './style/HomePage.css';
import React, { useState, useEffect } from 'react';
import TopBar from './TopBar';
import BottomButtons from './BottomButtons';
import ChatContainer from './ChatContainer';
import PlansModal from './PlansModal';
import axios from 'axios';
import { useAuth0 } from '@auth0/auth0-react';
import {UpsertUser, UpdateUserSubscription, GetUser} from './BotClient';
import PayPal from './PayPal';

const HomePage = () => {
  const [showModal, setShowModal] = useState(false);
  const [IP, setIP] = useState('');
  const [gotIP, setGotIP] = useState(false);
  const { isAuthenticated, isLoading, user } = useAuth0();
  const [userInfo, setUserInfo] = useState({});
  const [dbUser, setDbUser] = useState({});
  const [dbUserGot, setDbUserGot] = useState(false);
  const [isUpserted, setIsUpserted] = useState(false);

  const onSubscriptionComplete = (data) => {
    console.log('Subscription complete!', data);
    setTimeout(async () => {
      try {
          const resposne = await UpdateUserSubscription(data,userInfo);
          if (resposne){
              setShowModal(false);
              var temp = userInfo;
              temp['is_paying'] = true;
              setUserInfo(temp);
          }
        }
      catch(error){
          console.log('error upserting user', error);
      }
  }, 500);

  }
  const handlePlansClicked = () => {
      setShowModal(true);
    };
  const getIpAddress = async () => {
       
      console.log('inside getIpAddress')
      const res = await axios.get("https://api.ipify.org/?format=json");

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
              const user = await UpsertUser(userInfo);
              if (user){
                  setIsUpserted(true);
              }
          }
          catch(error){
              console.log('error upserting user', error);
          }
      }, 500);
      
  }
  useEffect(() => {
      if (!isLoading && !gotIP){
        getIpAddress();
      }
  }, [isAuthenticated, isLoading, user, gotIP]);
    
  const getDBUser = async () => {
    setTimeout(async () => {
      try {
          setGotIP(true);
          const userResponse = await GetUser(userInfo.email);
          if (userResponse){
              console.log('userResponse: ', userResponse);
              setDbUser(userResponse);
              setDbUserGot(true);
              console.log('dbUser: ', dbUser);
          }
      }
      catch(error){
          console.log('error upserting user', error);
      }
    }, 500);
  }
    

  useEffect(() => {
    if (isAuthenticated && !isLoading && isUpserted && !dbUserGot){
      getDBUser();
    }
  }, [dbUser,isAuthenticated, isLoading, userInfo, isUpserted]);

  return (
    <>
    <div className = "container">
      
      {/* {!showModal && ( */}
      <div>
        <TopBar />
      <ChatContainer userInfo={dbUser}/>
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
    {showModal && 
    <>
    {/* <PlansModal className ="plans-modal" onClose={() => setShowModal(false)} /> */}
      <PayPal className="plans-modal" onClose={() => setShowModal(false) } onSubscriptionComplete={onSubscriptionComplete}></PayPal>
      </>
      }
    </>
  );
};

export default HomePage;
