ECHO "Starting chat-site"
docker build -t chat-website .
docker run -p 3000:80 chat-website
ECHO "Chat-site started"
