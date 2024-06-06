import React, { useState, useContext } from "react";
import "./style/SignUpLogin.css";
import { LoginUser } from "./UserClient";
import LoginContext from "./LoginContext";
import TopBar from "./TopBar";
function Login() {
  const [values, setValues] = useState({
    email: "",
    password: ""
  });
  const { isLoggedIn, setIsLoggedIn } = useContext(LoginContext);

  const handleInputChange = (event) => {
    /* event.persist(); NO LONGER USED IN v.17*/
    event.preventDefault();

    const { name, value } = event.target;
    setValues((values) => ({
      ...values,
      [name]: value
    }));
  };

  const [submitted, setSubmitted] = useState(false);
  const [valid, setValid] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (values.email && values.password) {

      setTimeout(async () => {
        try {
          const resp = await LoginUser(values.email, values.password);
          try{
              console.log('resp: ', resp);
              if (resp['Success'] === 'true'){
                setValid(true);
                console.log("use context : setIsLoggedIn");
                setIsLoggedIn(true);
              }
          }
          catch(error){
              console.log('error parsing response', error);
              setSubmitted(false);
          }
        } catch (error) {
          console.error('There was an error getting the login response:', error);
          setSubmitted(false);
          return alert('Could not sign in. Please check email and password.');
        }
      }, 500);
    }
    setSubmitted(true);
  };

  return (
    <>
    <TopBar />
    
    <div className="form-container">
      <form className="register-form" onSubmit={handleSubmit}>
        {submitted && valid && (
            <div className="success-message">
                <h3>
                {" "}
                Welcome {values.email}{" "}
                </h3>
                <div> Your login was successful! </div>
            <div className="home-button">
                <button onClick={() => window.location.href = '/'}>Home</button>
            </div>
          </div>
        )}
        {isLoggedIn && (
            <p> You are logged in</p>
        )}
        {!valid && (
          <input
            className="form-field"
            type="text"
            placeholder="Email"
            name="email"
            value={values.email}
            onChange={handleInputChange}
          />
        )}

        {submitted && !values.firstName && (
          <span id="first-name-error">Please enter your email</span>
        )}

        {!valid && (
          <input
            className="form-field"
            type="password"
            placeholder="Password"
            name="password"
            value={values.password}
            onChange={handleInputChange}
          />
        )}

        {submitted && !values.lastName && (
          <span id="last-name-error">Please enter your password</span>
        )}

        {submitted && !values.email && (
          <span id="email-error">Please enter an email address</span>
        )}
        {!valid && (
          <button className="form-field" type="submit">
            Login
          </button>
        )}
        <div className="sign-in">
          <button onClick={() => window.location.href = '/register'}> Create An Account </button>
        </div>
      </form>
    </div>
    </>
  );
}
export default Login;