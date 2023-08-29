import json
import base64
import socket
import threading
from nacl.secret import SecretBox
from nacl.utils import random as randombytes
from huffman import huffman_encoding, huffman_decoding


class ChatClient:
    def __init__(self):
        """
            Initialize the ChatClient object.

            Args:
                None

            Returns:
                None
        """
        # Define server host and ports
        self.HOST = '192.168.1.6'
        self.PORTS = [8004, 8005, 8006, 8007]
        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Prompt the user for their name or username
        self.username = input("Enter your name or username: ")

        # Generate a random nonce
        self.nonce = randombytes(SecretBox.NONCE_SIZE)

        # Generate a random key
        key = b'*secret**secret**secret**secret*'
        self.box = SecretBox(key)

        # self.encoding_dict = ''

    def connect_to_server(self):
        """
            Connect to the server by iterating through available ports.

            Args:
                None

            Returns:
                bool: True if connection is successful, False otherwise.
        """
        for port in self.PORTS:
            try:
                self.client_socket.connect((self.HOST, port))
                return True
            except:
                continue
        return False


    def send_message(self):
        """
            Send messages to the server.

            Args:
                None

            Returns:
                None
        """
        while True:
            message = input('')
            # Include the username in the message
            message_with_username = f"{self.username}: {message}"
            # encode message using Huffman algorithm
            encoded_message, self.encoding_dict = huffman_encoding(message_with_username)

            # Encrypt the encoded_message using salsa20
            ciphertext = self.box.encrypt(encoded_message, self.nonce)
            # Convert the encrypted message and encoding dictionary to base64 strings
            data = {
                'ciphertext': base64.b64encode(ciphertext).decode(),
                'encoding_dict': self.encoding_dict
            }
            json_data = json.dumps(data)
            # Send the JSON-encoded data
            self.client_socket.sendall(json_data.encode())


    def receive_messages(self):
        """
            Receive and display messages from the server.

            Args:
                None

            Returns:
                None
        """
        while True:
            # Receive the JSON-encoded data
            json_data = self.client_socket.recv(1024)
            # Decode the JSON-encoded data
            data = json.loads(json_data)
            ciphertext = base64.b64decode(data['ciphertext'])
            encoding_dict = data['encoding_dict']
            # Decrypt the incoming message using salsa20
            plaintext = self.box.decrypt(ciphertext)
            # decode the Huffman encoded message
            message = huffman_decoding(plaintext, encoding_dict)
            # message = plaintext.decode()
            print("Received message:", message)


if __name__ == "__main__":
    chat_obj = ChatClient()
    # Start thread to connect to the server
    connect_thread = threading.Thread(target=chat_obj.connect_to_server)
    connect_thread.start()

    # Wait for the client to connect to the server
    connect_thread.join()

    # Check if the client successfully connected to the server
    if connect_thread.is_alive():
        print("Unable to connect to the server.")
    else:
        # Start thread to send messages to the server
        send_thread = threading.Thread(target=chat_obj.send_message)
        send_thread.start()
        chat_obj.receive_messages()
