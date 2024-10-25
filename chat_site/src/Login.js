import React, { useState, useContext } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { FaUserCircle } from "react-icons/fa";
import "./style/SignUpLogin.css";
import { UnsubscribeUser } from "./BotClient";
import { DBContext } from "./DBContext";
const ProfileModal = ({ show, setShow }) => {
  const { user, isAuthenticated, logout } = useAuth0();
  const { currentUser, setCurrentUser } = useContext(DBContext);
  const [unsubscribed, setUnsubscribed] = useState(false);

  const unsubscribeUser = async () => {
    const response = await UnsubscribeUser(user.email);
    if (response) {
      setUnsubscribed(true);
      setCurrentUser({ ...currentUser, is_paying: false });
    }
  };

  const logoutUser = () => {
    setShow(false);
    return logout({ returnTo: window.location.origin });
  };

  if (!show || !isAuthenticated) {
    return null;
  }
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <img src={user.picture} alt={user.name} width="100" height="100" />
        <h2>{user.name}</h2>
        <p>{user.email}</p>
        {currentUser.is_paying && (
          <div>
            {unsubscribed && <p>Unsubscribed!</p>}
            {!unsubscribed && (
              <button className="unsubscribe-text" onClick={unsubscribeUser}>
                Unsubscribe
              </button>
            )}
          </div>
        )}
        <div className="ok-buttons">
          <button className="logout-button" onClick={logoutUser}>
            Logout
          </button>
          <button className="close-button" onClick={() => setShow(false)}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

const LoginButtonOrProfileIcon = ({ show, setShow }) => {
  const { loginWithRedirect, isAuthenticated, isLoading } = useAuth0();

  if (isLoading) return null;

  if (!isAuthenticated) {
    return (
      <button className="login-button" onClick={loginWithRedirect}>
        Sign Up/Log In
      </button>
    );
  }

  return (
    <div>
      <FaUserCircle
        onClick={() => setShow(true)}
        style={{ cursor: "pointer", color: "#ffffff", fontSize: "24px" }} // Adjust color and size
      />
    </div>
  );
};

const LoginProfileComponent = ({ myUser }) => {
  const [show, setShow] = useState(false);

  return (
    <div>
      <LoginButtonOrProfileIcon show={show} setShow={setShow} />
      <ProfileModal show={show} setShow={setShow} myUser={myUser} />
    </div>
  );
};

export default LoginProfileComponent;
