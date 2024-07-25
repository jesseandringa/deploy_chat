# Use Node.js as a base image
FROM node:14-alpine as build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the remaining app files to the working directory
COPY . .

# Run the app
# RUN npm run start
# Serve the build folder
# COPY --from=build /app/build /usr/share/nginx/html
CMD ["npm", "run", "start"]
# Build the app





