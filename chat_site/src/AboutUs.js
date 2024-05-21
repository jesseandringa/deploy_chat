// import logo from './logo.svg';
import './style/AboutUs.css';
import React, { useState } from 'react';
import TopBar from './TopBar';
import BottomButtons from './BottomButtons';
// import ChatContainer from './ChatContainer';
import PlansModal from './PlansModal';

const AboutUs = () => {
  const [showModal, setShowModal] = useState(false);

  const handlePlansClicked = () => {
      setShowModal(true);
    };
  

  return (
    <>
    <div className = "container">
      
      {/* {!showModal && ( */}
      <div>
        <TopBar />
        <div className="about-us">
        <h1>About Us</h1>
        <p> We created Muni because we were frustrated with the difficulty of navigating municipal websites. Each city, county, and state is different, with constantly changing information. We knew there had to be a better way to navigate this red tape, and so we set out to make the information as easy to access, and as transparent as possible. </p>

        <p>   Muni is a digital assistant, created to make your life easier. Whether you are a homeowner curious about codes in your local municipality, a Realtor looking to advise a client, a contractor pulling permits, or an investor in their due diligence period, we are here to help. </p>

        <p>As we are still in our early stages, we are limited in the cities and counties we have on our platform - with that said, if you are looking to use Muni for a county/city not currently available, please reach out and we can start the process to add it to our databases. </p>
        </div>
        
      {/* <BottomButtons onPlansClicked={handlePlansClicked}/> */}
      </div>
      {/* )} */}
     

    </div>
    {showModal && <PlansModal className ="plans-modal" onClose={() => setShowModal(false)} />}
    </>
  );
};

export default AboutUs;
