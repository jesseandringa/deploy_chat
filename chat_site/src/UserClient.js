const SignUpUser = (firstName, lastName, email, password) => {
    const baseURL = 'http://3.143.1.57:3050/api';
    const endpoint = '/sign-up';
    const url = new URL(endpoint, baseURL);

    // Create a new object with user data
    const userData = {
        firstname: firstName,
        lastname: lastName,
        email: email,
        password: password
    };

    // Use the fetch API to send a POST request with JSON data
    return fetch(url, {
        method: 'POST', // Change to POST
        headers: {
            'Content-Type': 'application/json' // Set content type for JSON
        },
        body: JSON.stringify(userData) // Convert data to JSON string
    })
    .then(response => {
        // ... handle response
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON response body
    });
};
  
export {SignUpUser};

const LoginUser = (email, password) => {
    const baseURL = 'http://3.143.1.57:3050/api'; // Base URL
    const endpoint = '/login'; // Endpoint
    const url = new URL(endpoint, baseURL);
    url.searchParams.append('email', email);
    url.searchParams.append('password',password);
    
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
      
    export {LoginUser};