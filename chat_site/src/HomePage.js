// import logo from './logo.svg';
import "./style/HomePage.css";
import React, { useState, useEffect } from "react";
import TopBar from "./TopBar";
import BottomButtons from "./BottomButtons";
import ChatContainer from "./ChatContainer";
import PlansModal from "./PlansModal";
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";
import { UpsertUser, UpdateUserSubscription, GetUser } from "./BotClient";
import PayPal from "./PayPal";

const HomePage = () => {
  const [showModal, setShowModal] = useState(false);
  const [IP, setIP] = useState("");
  const [gotIP, setGotIP] = useState(false);
  const { isAuthenticated, isLoading, user } = useAuth0();
  const [userInfo, setUserInfo] = useState({});
  const [dbUser, setDbUser] = useState({});
  const [dbUserGot, setDbUserGot] = useState(false);
  const [isUpserted, setIsUpserted] = useState(false);

  const onSubscriptionComplete = (data) => {
    console.log("Subscription complete!", data);
    setTimeout(async () => {
      try {
        const resposne = await UpdateUserSubscription(data, userInfo);
        if (resposne) {
          setShowModal(false);
          var temp = userInfo;
          temp["is_paying"] = true;
          setUserInfo(temp);
        }
      } catch (error) {
        console.log("error upserting user", error);
      }
    }, 500);
  };
  const handlePlansClicked = () => {
    if (!isAuthenticated && !isLoading) {
      return alert("Please Sign Up or Log In before subscribing.");
    }
    setShowModal(true);
  };
  const getIpAddressAndUpserUser = async () => {
    const res = await axios.get("https://api.ipify.org/?format=json");

    setIP(res.data["ip"]);
    if (isAuthenticated && !isLoading && user.email) {
      // console.log("user: ", user);
      // console.log("user.email: ", user.email);
      setUserInfo({
        ip: res.data["ip"],
        email: user.email,
        name: user.name,
        given_name: user.given_name,
        family_name: user.family_name,
      });
      if (userInfo.email) {
        setTimeout(async () => {
          try {
            setGotIP(true);
            // console.log("userInfo: ", userInfo);
            const user = await UpsertUser(userInfo);
            if (user) {
              setIsUpserted(true);
            }
          } catch (error) {
            console.log("error upserting user", error);
          }
        }, 500);
      }
    }
  };

  const getDBUser = async () => {
    setTimeout(async () => {
      try {
        const userResponse = await GetUser(userInfo.email);
        if (userResponse) {
          // console.log("userResponse: ", userResponse);
          setDbUser(userResponse);
          setDbUserGot(true);
          // console.log("dbUser: ", dbUser);
        }
      } catch (error) {
        console.log("error upserting user", error);
      }
    }, 500);
  };

  useEffect(() => {
    if (isAuthenticated && !isLoading && !dbUserGot && !gotIP) {
      getIpAddressAndUpserUser();
    }
    if (isAuthenticated && !isLoading && !dbUserGot && gotIP) {
      getDBUser();
    }
  }, [dbUser, isAuthenticated, isLoading, userInfo, isUpserted, user]);

  return (
    <>
      <div className="container">
        {/* {!showModal && ( */}
        <div>
          <TopBar myUser={dbUser} />
          <ChatContainer className="chat-container" userInfo={dbUser} />
          <BottomButtons
            className="bottom-buttons"
            onPlansClicked={handlePlansClicked}
          />
        </div>
      </div>
      {showModal && (
        <>
          <PayPal
            className="plans-modal"
            onClose={() => setShowModal(false)}
            onSubscriptionComplete={onSubscriptionComplete}
          ></PayPal>
        </>
      )}
    </>
  );
};

export default HomePage;
