# Chat Server with Redundancy using Docker
This project is a chat server that provides redundancy using Docker. The server allows multiple clients to connect and exchange messages. If the primary server goes down, the system automatically switches to a backup server to ensure uninterrupted communication.
## Prerequisites
Docker: Install Docker on your system if it's not already installed. You can download Docker from the official website: https://www.docker.com
## Getting Started
Follow the steps below to set up and run the chat server with redundancy using Docker:
1. Clone the repository:
```
git clone --branch https://github.com/Adrine27/Chat_application.git
```
2. If you want to build docker for the first time run
```
docker-compose up --build
```
   else run
```
docker-compose up
```
3. Create virtual environment
```
python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
4. Navigate to the clients directory
```
cd clients
```
5. Run clients in different terminals
```
python client.py
python client_2.py
```
You can now send and receive messages through the chat system.

## Project Structure
The project consists of the following files:
1. server.py: The script that implements the chat server and handles incoming client connections and messages.
2. client.py: The script that represents a chat client and allows sending and receiving messages to and from the server.
3. huffman.py: The script that provides functions for Huffman encoding and decoding used in message compression.
4. Dockerfile: The Dockerfile that defines the server and client containers.
5. docker-compose.yml: The Docker Compose configuration file that sets up the server and client containers.

## Server Configuration
The server is configured to listen on ports 8004, 8005, 8006, and 8007. These ports can be accessed from the host machine to connect to the server.

## Server Redundancy
The chat server is designed to provide redundancy using Docker and multiple server instances. If the primary server goes down, the system automatically switches to the next available server in the list of ports. The backup server takes over and continues to serve the clients.

## Enjoy chatting with redundancy using Docker!