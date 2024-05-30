// DropdownMenu.js
import React from 'react';
import './style/DropdownMenu.css';
// import {changeCounty} from './BotClient';
import { useState } from 'react';

const DropdownMenu = ({ selectedOption, onOptionChange }) => {
  // const [countyChanged, setCountyChanged] = useState(false);
  // Function to handle option selection
  const handleOptionChange = (event) => {
    const selectedValue = event.target.value;
    onOptionChange(selectedValue); // Call the parent component's handler function
    // setTimeout(async () => {
    //   try {
    //     setCountyChanged(true);
    //     const resp = await changeCounty(selectedValue);
    //     try{
    //        console.log('resp: ', resp);
    //     }
    //     catch(error){
    //         console.log('timed out error: ', error)
    //         setCountyChanged(false);
    //     }
    //   } catch (error) {
    //     console.error('There was an error getting the county response:', error);
    //     setCountyChanged(false);
    //   }
    // }, 500);
  };
  const isDefaultOptionSelected = () => {
    return selectedOption === '';
  };

  return (
    <div className='dropdown-container'>
      {/* <h3>Select an Option:</h3> */}
      {/* Dropdown menu */}
      <select value={selectedOption} onChange={handleOptionChange}  className={`dropdown-menu ${isDefaultOptionSelected() ? 'default-option' : 'selected-option'}`}>
        <option value="">Select a County...</option>
        <option value="sandy-ut">Sandy, UT</option>
        <option value="millcreek-ut">Millcreek, UT</option>
        <option value="murray-ut">Murray, UT</option>
        <option value="gunnison-co">Gunnison, CO</option>
        {/* Add more options as needed */}
      </select>
      {/* {countyChanged && <p>County changed, this might take a couple of minutes</p>} */}
    </div>
  );
};

export default DropdownMenu;
