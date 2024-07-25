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
CMD ["npm", "run", "start"]
# CMD ["npm", "run", "build"]

# Production stage
# FROM nginx:alpine

# Copy the build output to Nginx's html directory
# COPY --from=build /app/build /usr/share/nginx/html
# RUN rm /etc/nginx/conf.d/default.conf
# Expose the port Nginx runs on
# EXPOSE 80
# EXPOSE 443

# CMD ["tail", "-f", "/dev/null"]
# Start Nginx
# CMD ["nginx", "-g", "daemon off;"]



