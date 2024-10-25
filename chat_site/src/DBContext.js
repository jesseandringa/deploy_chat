// src/DBContext.js
import React, { createContext, useState, useEffect } from "react";
import PropTypes from "prop-types";
import { useAuth0 } from "@auth0/auth0-react";
import { GetUser, UpsertUser } from "./BotClient";
import axios from "axios";

export const DBContext = createContext();

const DBProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [upsertedUser, setUpsertedUser] = useState(false);
  const [areMessages, setAreMessages] = useState(false);
  const [botResponded, setBotResponded] = useState(false);
  const [userMessage, setUserMessage] = useState("");
  const [botMessages, setBotMessages] = useState("");
  const [botSources, setBotSources] = useState([]);
  const [selectedOption, setSelectedOption] = useState("");

  const {
    isAuthenticated,
    user,
    getAccessTokenSilently,
    isLoading,
    loginWithRedirect,
    navigate,
  } = useAuth0();

  useEffect(() => {
    const checkUserSession = async () => {
      if (!isAuthenticated && !isLoading) {
        try {
          // Try silently getting the access token to check for a valid session
          await getAccessTokenSilently();
        } catch (error) {
          // If there's an error, redirect to the login page
          console.log("error", error);
          loginWithRedirect({
            appState: { targetUrl: window.location.pathname },
          });
        }
      }
    };

    checkUserSession();
  }, [
    isAuthenticated,
    isLoading,
    loginWithRedirect,
    user,
    navigate,
    getAccessTokenSilently,
  ]);

  useEffect(() => {
    console.log("currentUser", currentUser);
    const fetchUser = async () => {
      if (isAuthenticated && user && !currentUser) {
        try {
          const userResponse = await GetUser(user.email);
          if (userResponse) {
            setCurrentUser(userResponse);
          } else {
            const res = await axios.get("https://api.ipify.org/?format=json");

            const userInfo = {
              ip: res.data["ip"],
              email: user.email,
              name: user.name,
              given_name: user.given_name,
              family_name: user.family_name,
            };
            const response = await UpsertUser(userInfo);
            if (response) {
              setUpsertedUser(true);
            }
          }
        } catch (error) {
          console.error("Error fetching current user:", error);
        }
      } else if (!isAuthenticated) {
        setCurrentUser(null);
      }
    };

    fetchUser();
  }, [isAuthenticated, user, currentUser]);

  return (
    <DBContext.Provider
      value={{
        currentUser,
        setCurrentUser,
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
      }}
    >
      {children}
    </DBContext.Provider>
  );
};

DBProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export default DBProvider;
