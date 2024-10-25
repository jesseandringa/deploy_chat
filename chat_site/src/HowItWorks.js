import "./style/HowItWorks.css";
import React, { useState, useContext } from "react";
import TopBar from "./TopBar";
import BottomButtons from "./BottomButtons";
import PayPal from "./PayPal";
import { UpdateUserSubscription, GetUser } from "./BotClient";
import { useAuth0 } from "@auth0/auth0-react";
import { DBContext } from "./DBContext";

const HowItWorks = () => {
  const [showModal, setShowModal] = useState(false);
  const { isAuthenticated, isLoading } = useAuth0();
  const { currentUser, setCurrentUser } = useContext(DBContext);

  const onSubscriptionComplete = (data) => {
    console.log("Subscription complete!", data);
    setTimeout(async () => {
      try {
        const resposne = await UpdateUserSubscription(data, currentUser);
        if (resposne) {
          setShowModal(false);
          setCurrentUser({ ...currentUser, is_paying: true });
        }
      } catch (error) {
        console.log("error upserting user", error);
      }
    }, 500);
  };
  const handlePlansClicked = () => {
    if (!isAuthenticated && !isLoading) {
      return alert("Please Sign Up or Log In before subscribing.");
    }
    setShowModal(true);
  };

  return (
    <>
      <div className="container">
        <div>
          <TopBar />
          <div className="how-it-works">
            <h1>How It Works</h1>
            <p>
              {" "}
              Muni let’s you access the information you need, faster. With
              access to all of the information on the (Salt Lake county)
              municipal website of your choosing, we have created a digital
              assistant, to help you answer those questions regarding zoning,
              codes, laws, and more. Not only do we provide the summarized
              information you’re looking for, but we also provide the location,
              and source of the documents. Here’s how it works!{" "}
            </p>
            <div className="how-it-works-steps">
              <p>Step 1: Select your municipality. </p>

              <p>Step 2: Ask your question.</p>

              <p>
                Step 3: Use the provided links to do further research, or ask
                another question!{" "}
              </p>
            </div>
            <BottomButtons
              className="bottom-buttons"
              onPlansClicked={handlePlansClicked}
            />
          </div>

          {showModal && (
            <>
              <PayPal
                className="plans-modal"
                onClose={() => setShowModal(false)}
                onSubscriptionComplete={onSubscriptionComplete}
              ></PayPal>
            </>
          )}
        </div>
        {/* )} */}
      </div>
      {/* {showModal && 
          <>
              <PayPal className="plans-modal" onClose={() => setShowModal(false) } onSubscriptionComplete={onSubscriptionComplete}></PayPal>
          </>
      } */}
    </>
  );
};

export default HowItWorks;
