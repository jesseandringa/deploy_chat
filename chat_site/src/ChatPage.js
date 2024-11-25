// import logo from './logo.svg';
import "./style/HomePage.css";
import React, { useState, useEffect, useContext } from "react";
import TopBar from "./TopBar";
import ChatContainer from "./ChatContainer";
import { DBContext } from "./DBContext";

const ChatPage = () => {
  const [areMessages, setAreMessages] = useState(false);

  const handleAreMessagesChange = (value) => {
    setAreMessages(value);
  };

  return (
    <>
      <div className="container">
        <div>
          <TopBar />
          <ChatContainer
            className="chat-container"
            handleAreMessagesChange={handleAreMessagesChange}
          />
        </div>
      </div>
    </>
  );
};

export default ChatPage;
