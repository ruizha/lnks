# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the entire project
COPY . /app

# Install Flask
RUN pip install Flask

# Copy and make the entrypoint script executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Set the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run the Flask application, passed to the entrypoint
CMD ["flask", "run", "--host=0.0.0.0"]
