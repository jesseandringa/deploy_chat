import React, { useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
// import Avatar from "@mui/material/Avatar"; // MUI Avatar component for profile icon
import { FaUserCircle } from "react-icons/fa";
import "./style/SignUpLogin.css";
import { UnsubscribeUser } from "./BotClient";

const ProfileModal = ({ show, setShow }) => {
  const { user, isAuthenticated, logout } = useAuth0();
  const [unsubscribed, setUnsubscribed] = useState(false);

  const unsubscribeUser = async () => {
    const response = await UnsubscribeUser(user.email);
    if (response) {
      setUnsubscribed(true);
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
        {/* <h1>Profile</h1> */}
        <img src={user.picture} alt={user.name} width="100" height="100" />
        <h2>{user.name}</h2>
        <p>{user.email}</p>
        {unsubscribed ? <p>Unsubscribed!</p> : null}
        <button className="unsubscribe-text" onClick={() => unsubscribeUser()}>
          Unsubscribe
        </button>
        <br></br>
        <div className="ok-buttons">
          <button className="logout-button" onClick={() => logoutUser()}>
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
  const { loginWithRedirect, logout, user, isAuthenticated, isLoading } =
    useAuth0();

  // If still loading auth status, don't show anything
  if (isLoading) return null;

  // If user is not authenticated, show the login button
  if (!isAuthenticated) {
    return <button onClick={loginWithRedirect}>Sign Up/Log In</button>;
  }

  // If user is authenticated, show the profile icon (Avatar)
  return (
    <div>
      <FaUserCircle
        src={user.picture}
        alt={user.name}
        onClick={() => setShow(true)}
        style={{ cursor: "pointer" }} // cursor to show it's clickable
      />
    </div>
  );
};

const LoginProfileComponent = () => {
  const [show, setShow] = useState(false);

  return (
    <div>
      <LoginButtonOrProfileIcon show={show} setShow={setShow} />
      <ProfileModal show={show} setShow={setShow} />
    </div>
  );
};

export default LoginProfileComponent;

// import React from "react";
// import { useAuth0 } from "@auth0/auth0-react";

// const ProfileModal = ({ show, setShow }) => {
//   const { user, isAuthenticated, isLoading } = useAuth0();

//   if (!show) {
//     return null;
//   }

//   return (
//     <div>
//       <h1>Profile</h1>
//       <img src={user.picture} alt={user.name} />
//       <h2>{user.name}</h2>
//       <p>{user.email}</p>
//       <button onClick={() => setShow(false)}>Close</button>
//     </div>
//   );
// };
// const LoginButton = () => {
//   const { loginWithRedirect, logout, isAuthenticated, isLoading } = useAuth0();
//   const [loggedIn, setLoggedIn] = React.useState(false);

//   React.useEffect(() => {
//     console.log(isAuthenticated, isLoading);
//     if (isAuthenticated && !isLoading) {
//       setLoggedIn(true);
//     }
//   }, [isAuthenticated, isLoading, loggedIn]);

//   const handleLogin = () => {
//     loginWithRedirect();
//     setLoggedIn(true);
//   };

//   const handleLogout = () => {
//     logout({ returnTo: window.location.origin });
//     setLoggedIn(false);
//   };

//   return (
//     <button onClick={() => (loggedIn ? handleLogout() : handleLogin())}>
//       {loggedIn ? "Logout" : "Sign Up/Log In"}
//     </button>
//   );
// };

// // export default LoginButton;

// const LoginProfileComponent = () => {
//   const [show, setShow] = React.useState(false);

//   return (
//     <div>
//       <LoginButton show={show} setShow={setShow} />
//       <ProfileModal show={show} setShow={setShow} />
//     </div>
//   );
// };

// export default LoginProfileComponent;
