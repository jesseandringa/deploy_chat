import React, { useState } from "react";
import TopBar from "./TopBar";
import "./style/ContactUs.css";
import { postEmail } from "./BotClient";

function ContactUs() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevent default form submission behavior

    // Simulate form submission (replace with actual submission logic)
    // console.log('Name:', name);
    // console.log('Email:', email);
    // console.log('Message:', message);
    setTimeout(async () => {
      try {
        const emailResponse = await postEmail(message, name, email);
        console.log("email response: ", emailResponse);
      } catch (error) {
        console.log("There was an error sending the email: ", error);
      }
    }, 500);
    setName("");
    setEmail("");
    setMessage("");
    setSubmitted(true);
  };

  return (
    <>
      <TopBar />

      <div className="contact-us">
        <p>
          Do you have any suggestions, questions, comments, or want access to a
          different municipality somewhere?{" "}
        </p>
        <p>
          Send us a message and we will get back to you as soon as possible!
        </p>
        <h1>Contact Us</h1>
        {submitted ? (
          <p>Thank you for your message! We will get back to you soon.</p>
        ) : (
          <form onSubmit={handleSubmit}>
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              name="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              name="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <label htmlFor="message">Message:</label>
            <textarea
              id="message"
              name="message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              required
            />
            <button type="submit">Submit</button>
          </form>
        )}
      </div>
    </>
  );
}

export default ContactUs;
