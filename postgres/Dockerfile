FROM postgres:latest

# Set environment variable for password (replace with a strong password)
ENV POSTGRES_PASSWORD=my_strong_password

# Create the database upon container start
RUN mkdir -p /docker-entrypoint-initdb.d

# Replace with your schema script (optional)
# COPY schema.sql /docker-entrypoint-initdb.d/ 

# Expose the port for connection
EXPOSE 5432
