
// A simple function to simulate a more dynamic response based on user input
const getBotResponse = (message, selectedCounty, IP) => {
    // Convert the user input to lowercase for easier keyword matching
// run locally
// const baseURL = 'http://localhost:3050/api/'; // Base URL
// run on server
const baseURL = 'http://3.143.1.57:3050/api'; // Base URL
// const baseURL = 'https://munihelp.com/api/';
const endpoint = 'get-response'; // Endpoint
const url = new URL(endpoint, baseURL);
url.searchParams.append('message', message);
url.searchParams.append('county', selectedCounty);// Construct the full URL manually
console.log("yoolo")
url.searchParams.append('ip', IP);
console.log('url: ', url);
console.log("hoohoh")

// Use the fetch API to send a GET request
return fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); // Parse the JSON response body
    })
    .then(data => {
      console.log('data: ', data);
      return data; // Make sure to return the data here so it can be used by the caller
    })
    .catch(error => {
      console.error('There has been a problem with your fetch operation:', error);
      
      throw error; // Rethrow the error so it can be caught by the caller
    });
  };
  
export {getBotResponse};

const sendUserData = (ip) => {
  // Convert the user input to lowercase for easier keyword matching
// run locally
// const baseURL = 'http://localhost:3050/api/'; // Base URL
// run on server
// const baseURL = 'https://munihelp.com/api/'; // Base URL
const baseURL = 'http://3.143.1.57:3050/api'; // Base URL
console.log('ip in sendUserData: ', ip);
const endpoint = 'user-data'; // Endpoint
const url = new URL(endpoint, baseURL);
url.searchParams.append('ip', ip);
console.log('url: ', url);
console.log("hoohoh")


// Use the fetch API to send a GET request
return fetch(url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Parse the JSON response body
  })
  .then(data => {
    console.log('data: ', data);
    return data; // Make sure to return the data here so it can be used by the caller
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
    
    throw error; // Rethrow the error so it can be caught by the caller
  });
};

export {sendUserData};


const changeCounty = (selectedCounty) => {
// const baseURL = 'http://localhost:3050/api'; // Base URL
const baseURL = 'http://18.191.103.216:3050/api'; // Base URL
const endpoint = '/change-county'; // Endpoint
const url = new URL(endpoint, baseURL);
url.searchParams.append('county', selectedCounty);// Construct the full URL manually
console.log('url: ', url);


// Use the fetch API to send a GET request
return fetch(url)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Parse the JSON response body
  })
  .then(data => {
    console.log('data: ', data);
    return data; // Make sure to return the data here so it can be used by the caller
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
    
    throw error; // Rethrow the error so it can be caught by the caller
  });
};

export {changeCounty};

const postEmail = (message, name,email) => {
    // Convert the user input to lowercase for easier keyword matching
const baseURL = 'http://api:5002';
// The message you want to send

// Construct the full URL with query parameters
const url = new URL('/send-email', baseURL);
url.searchParams.append('message', message);
url.searchParams.append('name', name);
url.searchParams.append('email', email);

// Use the fetch API to send a GET request
return fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); // Parse the JSON response body
    })
    .then(data => {
      console.log('data: ', data);
      return data; // Make sure to return the data here so it can be used by the caller
    })
    .catch(error => {
      console.error('There has been a problem with your fetch operation:', error);
      throw error; // Rethrow the error so it can be caught by the caller
    });
  };
  
export {postEmail};
