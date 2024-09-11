
// A simple function to simulate a more dynamic response based on user input
const getBotResponse = (message, selectedCounty, userInfo) => {
    // Convert the user input to lowercase for easier keyword ma
  const baseURL = 'https://munihelp.com/api/';
  const endpoint = 'get-response'; // Endpoint
  const url = new URL(endpoint, baseURL);

  const email = userInfo.email;
  const ip = userInfo.ip;
  url.searchParams.append('message', message);
  url.searchParams.append('county', selectedCounty);// Construct the full URL manually
  url.searchParams.append('ip', ip);
  if (email){
    url.searchParams.append('email', email);
  }
  // console.log('url: ', url);

  // Use the fetch API to send a GET request
  return fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response body
      })
      .then(data => {
        // console.log('data: ', data);
        return data; // Make sure to return the data here so it can be used by the caller
      })
      .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        
        throw error; // Rethrow the error so it can be caught by the caller
      });
  };
  
export {getBotResponse};

const GetUser = (email) => {
  console.log('email: ', email);
  const baseURL = 'https://munihelp.com/api/'; // Base URL
  const endpoint = 'get_user'; // Endpoint
  const url = new URL(endpoint, baseURL);
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

export {GetUser};

const UpsertUser = (userInfo) => {

  // Convert the user input to lowercase for easier keyword matching
// run locally
    console.log('userInfo: ', userInfo);
    const baseURL = 'https://munihelp.com/api/'; // Base URL
    const endpoint = 'upsert_user'; // Endpoint
    const url = new URL(endpoint, baseURL);

    const username = userInfo.name;
    const email = userInfo.email;
    const ip = userInfo.ip;
    const given_name = userInfo.given_name;
    const family_name = userInfo.family_name;

    console.log('email: ', email);  
    url.searchParams.append('ip', ip);
    url.searchParams.append('email', email);
    url.searchParams.append('name', username);
    url.searchParams.append('given_name', given_name);
    url.searchParams.append('family_name', family_name);
  



    // Use the fetch API to send a GET request
    return fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response body
      })
      .then(data => {
        // console.log('data: ', data);
        return data; // Make sure to return the data here so it can be used by the caller
      })
      .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        
        throw error; // Rethrow the error so it can be caught by the caller
      });
};

export {UpsertUser};

const UpdateUserSubscription = (data, userInfo) => {

  // Convert the user input to lowercase for easier keyword matching
// run locally
    console.log('userInfo: ', userInfo);
    const baseURL = 'https://munihelp.com/api/'; // Base URL
    const endpoint = 'subscribe'; // Endpoint
    const url = new URL(endpoint, baseURL);

    const email = userInfo.email;
    const subscriptionId = data.subscriptionID;
    const paymentSource = data.paymentSource;
    const facilitatorAccessToken = data.facilitatorAccessToken;
    const orderId = data.orderID;

    console.log('email: ', email);  
    console.log('subscriptionId: ', subscriptionId);
    url.searchParams.append('email', email);
    url.searchParams.append('subscription_id', subscriptionId);
    url.searchParams.append('payment_source', paymentSource);
    url.searchParams.append('facilitator_access_token', facilitatorAccessToken);
    url.searchParams.append('order_id', orderId);
  
    // Use the fetch API to send a GET request
    return fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response body
      })
      .then(data => {
        // console.log('data: ', data);
        return data; // Make sure to return the data here so it can be used by the caller
      })
      .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        
        throw error; // Rethrow the error so it can be caught by the caller
      });
};

export {UpdateUserSubscription};

const postEmail = (message, name,email) => {
    // Convert the user input to lowercase for easier keyword matching
const baseURL = 'http://munichat/api/';
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
      // console.log('data: ', data);
      return data; // Make sure to return the data here so it can be used by the caller
    })
    .catch(error => {
      console.error('There has been a problem with your fetch operation:', error);
      throw error; // Rethrow the error so it can be caught by the caller
    });
  };
  
export {postEmail};
