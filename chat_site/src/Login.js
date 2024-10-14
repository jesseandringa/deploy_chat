import React, { useState } from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { FaUserCircle } from "react-icons/fa";
import "./style/SignUpLogin.css";
import { UnsubscribeUser } from "./BotClient";

const ProfileModal = ({ show, setShow, myUser }) => {
  const { user, isAuthenticated, logout } = useAuth0();
  const [unsubscribed, setUnsubscribed] = useState(false);

  const unsubscribeUser = async () => {
    const response = await UnsubscribeUser(user.email);
    if (response) {
      setUnsubscribed(true);
      myUser.is_paying = false;
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
        {myUser.is_paying && (
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
  const { loginWithRedirect, user, isAuthenticated, isLoading } = useAuth0();

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

// import React, { useState } from "react";
// import { useAuth0 } from "@auth0/auth0-react";
// // import Avatar from "@mui/material/Avatar"; // MUI Avatar component for profile icon
// import { FaUserCircle } from "react-icons/fa";
// import "./style/SignUpLogin.css";
// import { UnsubscribeUser } from "./BotClient";

// const ProfileModal = ({ show, setShow, myUser }) => {
//   const { user, isAuthenticated, logout } = useAuth0();
//   const [unsubscribed, setUnsubscribed] = useState(false);

//   const unsubscribeUser = async () => {
//     const response = await UnsubscribeUser(user.email);
//     if (response) {
//       setUnsubscribed(true);
//       myUser.is_paying = false;
//     }
//   };

//   const logoutUser = () => {
//     setShow(false);
//     return logout({ returnTo: window.location.origin });
//   };

//   if (!show || !isAuthenticated) {
//     return null;
//   }
//   return (
//     <div className="modal-overlay">
//       <div className="modal-content">
//         {/* <h1>Profile</h1> */}
//         <img src={user.picture} alt={user.name} width="100" height="100" />
//         <h2>{user.name}</h2>
//         <p>{user.email}</p>
//         {myUser.is_paying && (
//           <div>
//             {unsubscribed && <p>Unsubscribed!</p>}
//             {!unsubscribed && (
//               <button
//                 className="unsubscribe-text"
//                 onClick={() => unsubscribeUser()}
//               >
//                 Unsubscribe
//               </button>
//             )}
//           </div>
//         )}

//         <br></br>
//         <div className="ok-buttons">
//           <button className="logout-button" onClick={() => logoutUser()}>
//             Logout
//           </button>
//           <button className="close-button" onClick={() => setShow(false)}>
//             Close
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// };

// const LoginButtonOrProfileIcon = ({ show, setShow }) => {
//   const { loginWithRedirect, logout, user, isAuthenticated, isLoading } =
//     useAuth0();

//   // If still loading auth status, don't show anything
//   if (isLoading) return null;

//   // If user is not authenticated, show the login button
//   if (!isAuthenticated) {
//     return <button onClick={loginWithRedirect}>Sign Up/Log In</button>;
//   }

//   // If user is authenticated, show the profile icon (Avatar)
//   return (
//     <div>
//       <FaUserCircle
//         src={user.picture}
//         alt={user.name}
//         onClick={() => setShow(true)}
//         style={{ cursor: "pointer" }} // cursor to show it's clickable
//       />
//     </div>
//   );
// };

// const LoginProfileComponent = ({ myUser }) => {
//   const [show, setShow] = useState(false);

//   return (
//     <div>
//       <LoginButtonOrProfileIcon show={show} setShow={setShow} />
//       <ProfileModal show={show} setShow={setShow} myUser={myUser} />
//     </div>
//   );
// };

// export default LoginProfileComponent;
