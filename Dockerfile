# Use a base image with Python pre-installed
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the required files into the container
COPY server.py client.py huffman.py requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the ports used by the server
EXPOSE 8004-8007

# Set the entry point to run the server
CMD [ "python", "server.py" ]
