// import logo from './logo.svg';
import "./style/HomePage.css";
import React, { useState, useEffect, useContext } from "react";
import TopBar from "./TopBar";
import ChatContainer from "./ChatContainer";
import { DBContext } from "./DBContext";
import { motion, Variants } from "framer-motion";

const details = [
  ["Welcome to Muni!", 210, 40,80],
  ["Streamline access to municipal codes, zoning details, and other resources with our intelligent chatbot.", 210, 50, 50],
  ["Get answers to your city-related queries without digging through endless documents.", 210, 60, 50],
  ["Use the source links to dig deeper or verify your answers. ", 210, 70, 50],
  // ["Use links to dig deeper and verify answers", 100, 140, 50],
];

const cardVariants = (fontSize) => ({
  offscreen: {
    y: 300
  },
  onscreen: {
    y: 50,
    transition: {
      type: "spring",
      bounce: 0.1,
      duration: 0.8
    }
  },
  fontSize: `${fontSize}px`
});

const hue = (h,p) => `hsl(${h}, ${p}%, 50%)`;

function Card({ text, hueA, hueB, fontsize }) {
  // const background = `linear-gradient(306deg, ${hue(hueA)}, ${hue(hueA)})`;
  const background = `linear-gradient(306deg, ${hue(hueA, hueB)}, ${hue(hueA,hueB)})`;

  return (
    <motion.div
      className="card-container"
      initial="offscreen"
      whileInView="onscreen"
      viewport={{ once: false, amount: 1.0 }}
    >
      <div className="splash" style={{ background }} />
      <motion.div className="card" variants={cardVariants(fontsize)} style={{ fontSize: `${fontsize}px` }}>
        {text}
      </motion.div>
    </motion.div>
  );
}

const HomePage = () => {
 
  return (
    <>
      <TopBar />
      {details.map(([text, hueA, hueB, fontsize]) => (
        <Card text={text} hueA={hueA} hueB={hueB} key={text} fontsize={fontsize} />
      ))}
    </>
  );
};

export default HomePage;