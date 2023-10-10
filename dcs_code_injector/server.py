from PySide6.QtCore import *
import socket

class Server(QObject):
    connected = Signal()
    received = Signal(object)
    disconnected = Signal()

    def __init__(self):
        """
        Constructor for the Server class.
        """
        super().__init__()
        self.response = ""
        self.exit = False

    def start(self):
        """
        Starts the server and listens for incoming connections.
        """
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to a specific address and port
        server_socket.bind(('localhost', 40322))
        # Set the socket to listen mode with a backlog of 1 connection
        server_socket.listen(1)

        # Set a timeout on blocking socket operations
        server_socket.settimeout(0.1)

        # Main server loop
        while not self.exit:
            try:
                # Accept a new connection
                client_socket, address = server_socket.accept()
                # Emit connected signal
                self.connected.emit()
                # Receive data from the client
                data = client_socket.recv(1024).decode()
                # Emit received signal with the received data
                self.received.emit(data)

                # Loop for handling the connected client
                while True:
                    if self.response != "":
                        self.response += "\n"
                        client_socket.settimeout(0.1)
                        # Send the response to the client
                        client_socket.sendall(self.response.encode())
                        self.response = ""

                    try:
                        # Receive data from the client
                        data = client_socket.recv(1024).decode()
                        if data:
                            # Emit received signal with the received data
                            self.received.emit(data)
                            if data == '{"connection": "not_active"}':
                                break
                    except TimeoutError:
                        print("recv timed out")
                        break
                    except socket.error:
                        break

                    if self.exit:
                        break

                # Emit disconnected signal
                self.disconnected.emit()
                # Close the client socket
                client_socket.close()

            except TimeoutError:
                pass

        # Close the server socket
        server_socket.close()
