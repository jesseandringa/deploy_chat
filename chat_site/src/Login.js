import React from "react";
import { useAuth0 } from "@auth0/auth0-react";

const LoginButton = () => {
  const { loginWithRedirect, logout, isAuthenticated, isLoading } = useAuth0();
  const [loggedIn, setLoggedIn] = React.useState(false);

  React.useEffect(() => {
    console.log(isAuthenticated, isLoading);
    if (isAuthenticated && !isLoading) {
      setLoggedIn(true);
    }
  }, [isAuthenticated, isLoading, loggedIn]);

  const handleLogin = () => {
    loginWithRedirect();
    setLoggedIn(true);
  }

  const handleLogout = () => {
    logout({ returnTo: window.location.origin });
    setLoggedIn(false);
  }

  return (
    <button onClick={() => loggedIn ? handleLogout() : handleLogin()}>
      {loggedIn ? 'Logout' : 'Sign Up/Log In'}
    </button>
  );
};

export default LoginButton;
