// ImageWithOverlay.js
import React from "react";
import "./style/ChatContainer.css";
import { useState, useEffect, useContext } from "react";
import background_image from "./assets/chat-image-background.png"; // Import the image file
import { getBotResponse } from "./BotClient";
import { FaArrowCircleUp, FaUserCircle } from "react-icons/fa";
import { FcBusinesswoman } from "react-icons/fc";
import DropdownMenu from "./DropdownMenu";
import { DBContext } from "./DBContext";

const ChatContainer = ({ handleAreMessagesChange }) => {
  const [input, setInput] = useState("");

  const [totalMessageCount, setTotalMessageCount] = useState(0);
  const [questionsAsked, setQuestionsAsked] = useState(0);
  const [wordList, setWordList] = useState([]);
  const {
    currentUser,
    areMessages,
    setAreMessages,
    botResponded,
    setBotResponded,
    userMessage,
    setUserMessage,
    botMessages,
    setBotMessages,
    botSources,
    setBotSources,
    selectedOption,
    setSelectedOption,
  } = useContext(DBContext);

  const handleOptionChange = (selectedValue) => {
    setSelectedOption(selectedValue);
  };

  useEffect(() => {
    if (!wordList || wordList.length === 0) return;

    let currentMessage = "";
    let index = 0;

    const interval = setInterval(() => {
      currentMessage += (index > 0 ? " " : "") + wordList[index];
      setBotMessages(currentMessage);
      index++;

      if (index === wordList.length) {
        clearInterval(interval);
      }
    }, 30); // Adjust the interval time as needed

    return () => clearInterval(interval);
  }, [wordList]);

  const sendMessage = (e) => {
    if (!currentUser) {
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
    handleAreMessagesChange(true);
    setBotMessages("");
    setWordList([]);
    setBotSources([]);
    setBotResponded(false);
    setTotalMessageCount(totalMessageCount + 1);

    // Simulate bot response
    setTimeout(async () => {
      if (questionsAsked > 3 && !currentUser.is_paying) {
        setAreMessages(false);
        handleAreMessagesChange(false);

        return alert(
          "You have reached the maximum number of questions. Please sign up and subscribe to ask more questions."
        );
      }
      try {
        const botResponse = await getBotResponse(
          input,
          selectedOption,
          currentUser
        );
        try {
          let sources = botResponse.sources.split(/,\s*|\s+/); 

          for (let i = 0; i < sources.length; i++) {
            // Filter out any empty strings from the split
            if (sources[i].trim() !== "") {
              setBotSources((botSources) =>
                botSources.concat({ text: sources[i].trim(), sender: "source" })
              );
            }
          }
        } catch (error) {
          setAreMessages(false);
          handleAreMessagesChange(false);
          return alert(
            "Looks like something went wrong. Please try again or contact support."
          );
        }
        setWordList(botResponse.response.split(" "));
        setBotResponded(true);
        setQuestionsAsked(parseInt(botResponse.questions_asked));
      } catch (error) {
        setAreMessages(false);
        handleAreMessagesChange(false);

        return alert(
          "Looks like something went wrong. Please try again or contact support."
        );
      }
    }, 500);

    setInput("");
  };

  const handleInput = (e) => {
    setInput(e.target.value);
    e.target.style.height = "auto"; // Reset height to auto

    e.target.style.height = "auto";
    // Set the height to scrollHeight minus the padding
    const padding = 20; // Total padding (top + bottom)
    e.target.style.height = `${e.target.scrollHeight - padding}px`;
    if (e.key === "Enter") {
      e.preventDefault(); // Prevent the default action (new line)
      sendMessage(e); // Call the send message function
    }
  };

  return (
    <div className="chat-container">
      <DropdownMenu
        className="dropdown-menu"
        selectedOption={selectedOption}
        onOptionChange={handleOptionChange}
      />
      <div className="chat-selector">
        {/* Render the DropdownMenu component and pass props */}

        {!areMessages && (
          <div className="example-questions">
            <h2>Example Questions</h2>
            <ul>
              <li>How do I get a permit to build an ADU? </li>
              <li>Am I allowed to collect rain water?</li>
              <li>What are the building requirements for a new garage?</li>
            </ul>
          </div>
        )}
      </div>
      {areMessages && (
        <div className="chat-box-container">
          <div className="chat-box">
            <h2> Question: </h2>
            <hr className="content-separator" />
            <div className="question-container">
              <FaUserCircle className="question-icon" />
              <p className="question-text"> {userMessage}</p>
            </div>
            {!botResponded && (
              <div className="bot-messages">
                <div className="bot-thinking">
                  {/* <FcBusinesswoman className="bot-icon" /> */}
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
                  {/* <FcBusinesswoman className="bot-icon-answered" /> */}
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

      <div className="overlay-no-messages">
        <form className="chat-input" onSubmit={sendMessage}>
          <textarea
            value={input}
            onChange={handleInput}
            onKeyDown={handleInput}
            placeholder="Ask a Question"
            rows={1} // Start with one row
            className="chat-textarea"
          />
          <button id="send-button" type="submit">
            <FaArrowCircleUp className="question-icon" />
          </button>
        </form>
      </div>
      <br></br>
    </div>
  );
};

export default ChatContainer;
