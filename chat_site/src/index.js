import React from "react";
import ReactDOM from "react-dom/client";
import "./style/index.css";
import HomePage from "./HomePage";
import AboutUs from "./AboutUs";
import HowItWorks from "./HowItWorks";
import ContactUs from "./ContactUs";
import Features from "./Features";
import reportWebVitals from "./reportWebVitals";
import { createContext } from "react";
import LoginButton from "./Login";
import Auth0ProviderWithNavigate from "./AuthProviderWithNavigate";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { PayPalScriptProvider, PayPalButtons } from "@paypal/react-paypal-js";
import DBProvider from "./DBContext";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <Router>
    <PayPalScriptProvider options={{ clientId: "test" }}>
      <Auth0ProviderWithNavigate>
        <DBProvider>
          <Routes>
            <Route path="/" exact element={<HomePage />} />
            <Route path="/about-us" element={<AboutUs />} />
            <Route path="/how-it-works" element={<HowItWorks />} />
            <Route path="/contact-us" element={<ContactUs />} />
            <Route path="/features" element={<Features />} />
          </Routes>
        </DBProvider>
      </Auth0ProviderWithNavigate>
    </PayPalScriptProvider>
  </Router>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
