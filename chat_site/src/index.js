import React from 'react';
import ReactDOM from 'react-dom/client';
import './style/index.css';
import HomePage from './HomePage';
import AboutUs from './AboutUs';
import HowItWorks from './HowItWorks';
import ContactUs from './ContactUs';
import Features from './Features';
import SignUp from './SignUp';
import Login from './Login';
import reportWebVitals from './reportWebVitals';
import { createContext } from 'react';
import LoginContext from './LoginContext';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';



const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Router>
    <LoginContext.Provider>
      <Routes>
        <Route path="/" exact element={ <HomePage/> } />
        <Route path="/about-us" element={ <AboutUs/> } />
        <Route path="/how-it-works" element={ <HowItWorks/> } />
        <Route path="/contact-us" element={ <ContactUs/> } />
        <Route path="/features" element={ <Features/> } />
        <Route path="/login" element={ <Login/> } />
        <Route path="/register" element={ <SignUp/> } />

      </Routes>
    </LoginContext.Provider>
  </Router>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
