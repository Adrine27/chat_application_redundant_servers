import socket
import threading
from clients.client import ChatClient
import base64
import json
from clients.huffman import huffman_decoding

# Define server host and ports
HOST = '0.0.0.0'
PORTS = [8004, 8005, 8006, 8007]

chat_client = ChatClient()
box = chat_client.box

# Create a list of server sockets
server_sockets = []
for port in PORTS:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, port))
    server_socket.listen()
    server_sockets.append(server_socket)

# List to store client connections
client_list = []

def handle_client(client_socket, client_address):
    """
        Handle incoming messages from a client.

        Args:
            client_socket (socket.socket): The client socket object.
            client_address (tuple): The address of the client.

        Returns:
            None
    """
    while True:
        try:
            # Receive message from client
            json_data = client_socket.recv(1024)
            if json_data:
                # Decode the JSON-encoded data
                data = json.loads(json_data)
                ciphertext = base64.b64decode(data['ciphertext'])
                encoding_dict = data['encoding_dict']

                # Decrypt the incoming message using salsa20
                plaintext = box.decrypt(ciphertext)

                # Decode the Huffman encoded message
                message = huffman_decoding(plaintext, encoding_dict)

                # Broadcast message to all connected clients
                for client in client_list:
                    if client != client_socket:
                        client.sendall(message.encode())
            else:
                # Remove client from client_list if connection is closed
                remove_client(client_socket)
                break
        except:
            # Remove client from client_list if connection is closed unexpectedly
            remove_client(client_socket)
            break

def remove_client(client_socket):
    """
        Remove a client from the client list.

        Args:
            client_socket (socket.socket): The client socket object to remove.

        Returns:
            None
    """
    if client_socket in client_list:
        client_list.remove(client_socket)

def accept_clients():
    """
        Accept incoming client connections and start a new thread to handle each client.

        Args:
            None

        Returns:
            None
    """
    while True:
        # Accept incoming client connection
        client_socket, client_address = server_sockets[0].accept()

        # Add client to client_list
        client_list.append(client_socket)

        # Start thread to handle incoming messages from client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

def switch_servers():
    """
        Monitor the server status and switch to a backup server if the current server is down.

        Args:
            None

        Returns:
            None
    """
    while True:
        # Check if the current server is down
        server_down = False
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((HOST, PORTS[0]))
        except:
            server_down = True

        # If the server is down, switch to the next available server
        if server_down:
            print(f"Server on port {PORTS[0]} is down. Switching to backup server...")
            server_sockets.pop(0)
            if len(server_sockets) == 0:
                print("All servers are down. Shutting down...")
                break
            else:
                accept_clients_thread = threading.Thread(target=accept_clients)
                accept_clients_thread.start()
                continue

        # Wait before checking the server again
        client_socket.close()
        threading.Event().wait(5)

# Start thread to accept incoming client connections
accept_clients_thread = threading.Thread(target=accept_clients)
accept_clients_thread.start()

# Start thread to switch to a backup server in case of a failure
switch_servers_thread = threading.Thread(target=switch_servers)
switch_servers_thread.start()