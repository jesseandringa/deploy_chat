// ImageWithOverlay.js
import React from 'react';
import './style/ChatContainer.css'; 
import { useState, useEffect } from 'react';
import background_image from './assets/chat-image-background.png'; // Import the image file
import {getBotResponse} from './BotClient';
// import iconUrl from './assets/paper-plane.png';
// import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
// import { faPaperPlane, faUser} from '@fortawesome/free-solid-svg-icons';
import { FcSportsMode } from "react-icons/fc";
import { FcBusinesswoman } from "react-icons/fc";
import DropdownMenu from './DropdownMenu';
import axios from 'axios';
import { useContext } from 'react';
import LoginContext from './LoginContext';

const ChatContainer = () => {
    // const [messages, setMessages] = useState([]);
    const [userMessage, setUserMessage] = useState('');
    const [botMessages, setBotMessages] = useState('');
    const [botSources, setBotSources] = useState([]);
    const [input, setInput] = useState('');
    const [chatClicked, setChatClicked] = useState(false);
    const [areMessages, setAreMessages] = useState(false);
    const [botResponded, setBotResponded] = useState(false);
    const [selectedOption, setSelectedOption] = useState('');
    const [totalMessageCount, setTotalMessageCount] = useState(0);
    const [IP, setIP] = useState('');
    const [gotIP, setGotIP] = useState(false);
    const [questionsAsked, setQuestionsAsked] = useState(0);
    const { isLoggedIn, setIsLoggedIn } = useContext(LoginContext);
    const [isHomePageUpdated, setIsHomePageUpdated] = useState(false);

    useEffect(() => {
        // Update flag when login state changes
        console.log("isLoggedIn: ", isLoggedIn);
        setIsHomePageUpdated(isLoggedIn);
      }, [isLoggedIn]);
    const getIpAddress = async () => {
       
        const res = await axios.get("https://api.ipify.org/?format=json");
        console.log('res: ');
        console.log(res.data);
        setIP(res.data['ip']);
        setGotIP(true);
    }

    const handleOptionChange = (selectedValue) => {
        setSelectedOption(selectedValue);
    };

    useEffect(() => {
        console.log('inside useEffect')
        if (!gotIP) {
          getIpAddress();
        }
    }, []);

    const sendMessage = (e) => {
        // if (questionsAsked > 3){
        //     return alert('You have reached the maximum number of questions. Please sign up to ask more questions.');
        // }
        e.preventDefault();
        if (!input.trim()) return;
        console.log("user message: ", input);
        setUserMessage(input);
        setAreMessages(true);
        setBotMessages('');
        setBotSources([]);
        setBotResponded(false);
        setTotalMessageCount(totalMessageCount + 1);
        
        // Simulate bot response
        setTimeout(async () => {
          try {
            const botResponse = await getBotResponse(input, selectedOption, IP);
            try{
                let sources = botResponse.sources.split(',');
                for (let i = 0; i < sources.length; i++) {
                    setBotSources(botSources => botSources.concat({text: sources[i], sender: 'source'}));
                }
            }
            catch(error){
                console.log('error in splitting sources')
            }

            setBotMessages(botResponse.response);
            console.log('bot response sources: ', botResponse.sources);
            console.log('messages',botMessages)
            setBotResponded(true);
            console.log('questions asked: ', botResponse.questions_asked)
            setQuestionsAsked(parseInt(botResponse.questions_asked))
          } catch (error) {
            console.error('There was an error getting the bot response:', error);
          }
        }, 500);
    
        setInput('');
      };

  return (
    <div className ="chat-container">  
    <div className="chat-selector">
    {/* Render the DropdownMenu component and pass props */}
    <DropdownMenu selectedOption={selectedOption} onOptionChange={handleOptionChange} />
    {isLoggedIn && isHomePageUpdated &&(
        
    <p> HELLLO LOGGED in user</p>)
    }
    </div>
    <div className="image-container">
      {/* <img src={background_image} alt="Placeholder" /> */}

       
       <div className="overlay-no-messages">
            <form className="chat-input" onSubmit={sendMessage}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask a Question"
                />
                <button id="send-button"  type="submit">
                {/* <FontAwesomeIcon icon={faPaperPlane} /> */}
                <FcSportsMode className="question-icon" />
                </button>
          
            </form>
        </div> 
    </div>
    <br></br>
    {areMessages && (
        
        <div className="chat-box-container">
        
            <div className='chat-box'>
                <h2> Question: </h2>
                <hr className="content-separator" />
                <div className='question-container'>
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
                            <div className="bot-message">
                                {botMessages}
                            </div>
                        </div>
                        <h2 className="source-name">Sources:</h2>
                        <hr className="content-separator" />
                        <div className="bot-sources">
                            
                            
                            {botSources.map((msg, index) => (
                                 <div className="source-item">
                                <a href={msg.text} target="_blank" rel="noreferrer">{msg.text}</a>
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
