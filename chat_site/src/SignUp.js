import React, { useState } from "react";
import "./style/SignUpLogin.css";
import { SignUpUser } from "./UserClient";
import axios from 'axios';
import TopBar from "./TopBar";
import { useContext } from "react";
import LoginContext from "./LoginContext";

function SignUp() {
  const [values, setValues] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: ""
  });
    const [IP, setIP] = useState('');
    const [gotIP, setGotIP] = useState(false);
    const { isLoggedIn, setIsLoggedIn } = useContext(LoginContext);

    const getIpAddress = async () => {
       
        const res = await axios.get("https://api.ipify.org/?format=json");
        console.log('res: ');
        console.log(res.data);
        setIP(res.data['ip']);
        setGotIP(true);
    }

  const handleInputChange = (event) => {
    /* event.persist(); NO LONGER USED IN v.17*/
    if (gotIP === false){
        getIpAddress();
    }
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
    if (values.firstName && values.lastName && values.email && values.password && values.confirmPassword && values.password === values.confirmPassword) {
      
      setTimeout(async () => {
        try {
          const resp = await SignUpUser(values.firstName, values.lastName, values.email, values.password, IP);
          try{
              console.log('resp: ', resp);
              if (resp['Success'] === 'true'){
                setValid(true);
                setIsLoggedIn(true);
              }
          }
          catch(error){
              console.log('error parsing response', error);
          }
        } catch (error) {
          console.error('There was an error getting the signup response:', error);
          setSubmitted(false);
          return alert('Sorry, we could not sign you up at with this informaiton.');
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
              Welcome {values.firstName} {values.lastName}{" "}
            </h3>
            <div> Your registration was successful! </div>
            <div className="home-button">
                <button onClick={() => window.location.href = '/'}>Home</button>
            </div>
          </div>
        )}
        {!valid && (
          <input
            class="form-field"
            type="text"
            placeholder="First Name"
            name="firstName"
            value={values.firstName}
            onChange={handleInputChange}
          />
        )}

        {submitted && !values.firstName && (
          <span id="first-name-error">Please enter a first name</span>
        )}

        {!valid && (
          <input
            class="form-field"
            type="text"
            placeholder="Last Name"
            name="lastName"
            value={values.lastName}
            onChange={handleInputChange}
          />
        )}

        {submitted && !values.lastName && (
          <span id="last-name-error">Please enter a last name</span>
        )}

        {!valid && (
          <input
            class="form-field"
            type="email"
            placeholder="Email"
            name="email"
            value={values.email}
            onChange={handleInputChange}
          />
        )}

        {submitted && !values.email && (
          <span id="email-error">Please enter an email address</span>
        )}

        {!valid && (
          <input
            class="form-field"
            type="password"
            placeholder="Password"
            name="password"
            value={values.password}
            onChange={handleInputChange}
          />
        )}

        {submitted && !values.password && (
          <span id="last-name-error">Please enter a password</span>
        )}

        {!valid && (
          <input
            class="form-field"
            type="password"
            placeholder="Confirm Password"
            name="confirmPassword"
            value={values.confirmPassword}
            onChange={handleInputChange}
          />
        )}

        {submitted && !values.confirmPassword && (
          <span id="last-name-error">Please confirm your password</span>
        )}
        {submitted && values.confirmPassword !== values.password && (
          <span id="last-name-error">Please make sure you passwords match</span>
        )}

        {!valid && (
          <button class="form-field" type="submit">
            Register
          </button>
        )}
        <div className="sign-in">
          <button onClick={() => window.location.href = '/login'}> Login </button>
        </div>
      </form>
    </div>
    </>
  );
}
export default SignUp;