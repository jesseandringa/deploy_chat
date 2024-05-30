# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the content of the directory into the container at /app
COPY ./src /app/src
# COPY ./src /app/src #copy only the src folder
COPY credentials.json /app
COPY token.json /app
COPY logs.json /app
# COPY openaikey.json /app
# RUN mkdir /app/storage_resources

#commented out since trying to mount instead
# COPY ./storage_resources /app/storage_resources
# Install any needed dependencies specified in requirements.txt
COPY requirements.txt /app
# COPY ./file_resources/gunnison-resources /app/file_resources/gunnison-resources

RUN pip install --no-cache-dir -r requirements.txt
# ENV OPENAI_API_KEY=sk-proj-twhtcJKHIZThNS2eK9WTT3BlbkFJO4YH7KhpaJIVC40x6xZZ
ENV OPENAI_API_KEY=$OPENAI_API_KEY
# Expose the port the app runs on
# EXPOSE 5002
# Run chat_server.py when the container launches
CMD [ "python", "src/chat_server.py"]
