// ImageWithOverlay.js
import React from "react";
import "./style/ChatContainer.css";
import { useState, useEffect } from "react";
import background_image from "./assets/chat-image-background.png"; // Import the image file
import { getBotResponse } from "./BotClient";
import { FcSportsMode } from "react-icons/fc";
import { FcBusinesswoman } from "react-icons/fc";
import DropdownMenu from "./DropdownMenu";
import axios from "axios";
import { useAuth0 } from "@auth0/auth0-react";

const ChatContainer = ({ userInfo }) => {
  // const [messages, setMessages] = useState([]);
  const [userMessage, setUserMessage] = useState("");
  const [botMessages, setBotMessages] = useState("");
  const [botSources, setBotSources] = useState([]);
  const [input, setInput] = useState("");
  // const [chatClicked, setChatClicked] = useState(false);
  const [areMessages, setAreMessages] = useState(false);
  const [botResponded, setBotResponded] = useState(false);
  const [selectedOption, setSelectedOption] = useState("");
  const [totalMessageCount, setTotalMessageCount] = useState(0);
  const [questionsAsked, setQuestionsAsked] = useState(0);
  const { isAuthenticated, isLoading, user } = useAuth0();
  const [isPayingUser, setIsPayingUser] = useState(false);

  useEffect(() => {
    //update isPayingUser when userInfo changes
    // console.log('chatcontainer userInfo:: ', userInfo);
    if (userInfo.is_paying) {
      setIsPayingUser(true);
      // console.log('isPayingUser: ', isPayingUser);
    } else {
      setIsPayingUser(false);
      // console.log('isPayingUser: ', isPayingUser);
    }
    if (userInfo.questions_asked) {
      // console.log('userInfo.questions_asked: ', userInfo.questions_asked);
      setQuestionsAsked(parseInt(userInfo.questions_asked));
      // console.log('questionsAsked: ', questionsAsked);
    }
  }, [userInfo, isPayingUser, questionsAsked]);

  const handleOptionChange = (selectedValue) => {
    setSelectedOption(selectedValue);
  };

  const sendMessage = (e) => {
    if (!isAuthenticated && !isLoading) {
      return alert(
        "Please Sign Up or Log In to ask questions. You'll be able to ask 4 questions for free."
      );
    }
    // if (questionsAsked > 3){
    //     return alert('You have reached the maximum number of questions. Please sign up to ask more questions.');
    // }
    e.preventDefault();
    if (!input.trim()) return;
    setUserMessage(input);
    setAreMessages(true);
    setBotMessages("");
    setBotSources([]);
    setBotResponded(false);
    setTotalMessageCount(totalMessageCount + 1);

    // Simulate bot response
    setTimeout(async () => {
      //  console.log('db user: ', userInfo);
      if (questionsAsked > 3 && !isPayingUser) {
        setAreMessages(false);
        return alert(
          "You have reached the maximum number of questions. Please sign up and subscribe to ask more questions."
        );
      }
      try {
        const botResponse = await getBotResponse(
          input,
          selectedOption,
          userInfo
        );
        try {
          let sources = botResponse.sources.split(",");
          for (let i = 0; i < sources.length; i++) {
            setBotSources((botSources) =>
              botSources.concat({ text: sources[i], sender: "source" })
            );
          }
        } catch (error) {
          setAreMessages(false);
          return alert(
            "Looks like something went wrong. Please try again or contact support."
          );
        }

        setBotMessages(botResponse.response);
        // console.log('bot response sources: ', botResponse.sources);
        // console.log('messages',botMessages)
        setBotResponded(true);
        // console.log('questions asked: ', botResponse.questions_asked)
        setQuestionsAsked(parseInt(botResponse.questions_asked));
        userInfo.questions_asked = botResponse.questions_asked;
        setIsPayingUser(botResponse.is_paying_user);
      } catch (error) {
        setAreMessages(false);
        return alert(
          "Looks like something went wrong. Please try again or contact support."
        );
      }
    }, 500);

    setInput("");
  };

  return (
    <div className="chat-container">
      <div className="chat-selector">
        {/* Render the DropdownMenu component and pass props */}
        <DropdownMenu
          selectedOption={selectedOption}
          onOptionChange={handleOptionChange}
        />
      </div>
      <div className="image-container">
        <div className="overlay-no-messages">
          <form className="chat-input" onSubmit={sendMessage}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a Question"
            />
            <button id="send-button" type="submit">
              {/* <FontAwesomeIcon icon={faPaperPlane} /> */}
              <FcSportsMode className="question-icon" />
            </button>
          </form>
        </div>
      </div>
      <br></br>
      {areMessages && (
        <div className="chat-box-container">
          <div className="chat-box">
            <h2> Question: </h2>
            <hr className="content-separator" />
            <div className="question-container">
              <FcSportsMode className="question-icon" />
              <p className="question-text"> {userMessage}</p>
            </div>
            {!botResponded && (
              <div className="bot-messages">
                <div className="bot-thinking">
                  <FcBusinesswoman className="bot-icon" />
                  <div className="dot-container">
                    <div className="dot"></div>
                    <div className="dot"></div>
                    <div className="dot"></div>
                  </div>
                </div>
              </div>
            )}

            {botResponded && (
              <div className="bot-response">
                <h2 className="bot-name">Answer:</h2>
                <hr className="content-separator" />
                <div className="bot-messages">
                  <FcBusinesswoman className="bot-icon-answered" />
                  <div className="bot-message">{botMessages}</div>
                </div>
                <h2 className="source-name">Sources:</h2>
                <hr className="content-separator" />
                <div className="bot-sources">
                  {botSources.map((msg, index) => (
                    <div className="source-item">
                      <a href={msg.text} target="_blank" rel="noreferrer">
                        {msg.text}
                      </a>
                      <br></br>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatContainer;
