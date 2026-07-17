# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

ENV TZ=Europe/Prague

# Copy requirements and install dependencies
RUN pip install --no-cache-dir anthropic python-dotenv

# Copy the current directory contents into the container
COPY . .

# Run the application
ENTRYPOINT ["python"]
CMD ["src/chat.py"]
