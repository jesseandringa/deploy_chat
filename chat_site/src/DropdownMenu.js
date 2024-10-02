// DropdownMenu.js
import React from "react";
import "./style/DropdownMenu.css";
// import {changeCounty} from './BotClient';
import { useState } from "react";

const DropdownMenu = ({ selectedOption, onOptionChange }) => {
  // const [countyChanged, setCountyChanged] = useState(false);
  // Function to handle option selection
  const handleOptionChange = (event) => {
    const selectedValue = event.target.value;
    onOptionChange(selectedValue); // Call the parent component's handler function
  };
  const isDefaultOptionSelected = () => {
    return selectedOption === "";
  };

  return (
    <div className="dropdown-container">
      {/* <h3>Select an Option:</h3> */}
      {/* Dropdown menu */}
      <select
        value={selectedOption}
        onChange={handleOptionChange}
        className={`dropdown-menu ${
          isDefaultOptionSelected() ? "default-option" : "selected-option"
        }`}
      >
        <option value="">Select a County...</option>
        <option value="sandy-ut">Sandy, UT</option>
        <option value="millcreek-ut">Millcreek, UT</option>
        <option value="murray-ut">Murray, UT</option>
        <option value="summit-ut">Summit, UT</option>
        <option value="gunnison-co">Gunnison, CO</option>
        <option value="elko-nv">Elko, NV</option>
        <option value="king-wa">King, WA</option>
        <option value="cumberland-nc">Cumberland, NC</option>
        <option value="cullman-al">Cullmaan, AL</option>
      </select>

      {/* Add more options as needed */}
    </div>
  );
};

export default DropdownMenu;
