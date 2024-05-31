import { createContext } from "react";

const LoginContext = createContext({
    isLoggedIn: false,
    setIsLoggedIn: () => {},
  });
  export default LoginContext;