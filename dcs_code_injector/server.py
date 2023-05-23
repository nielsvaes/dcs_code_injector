from PySide6.QtCore import *
import socket


class Server(QObject):
    connected = Signal()
    received = Signal(object)
    disconnected = Signal()

    def __init__(self):
        super().__init__()
        self.response = ""
        self.exit = False

    #some messy server code, but too lazy to try and make it prettier right now
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 40322))
        server_socket.listen(1)

        server_socket.settimeout(0.1)

        while not self.exit:
            try:
                client_socket, address = server_socket.accept()
                self.connected.emit()
                data = client_socket.recv(1024).decode()
                self.received.emit(data)

                while True:
                    if self.response != "":
                        self.response += "\n"
                        client_socket.settimeout(0.1)
                        client_socket.sendall(self.response.encode())
                        self.response = ""

                    try:
                        data = client_socket.recv(1024).decode()
                        if data:
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

                self.disconnected.emit()
                client_socket.close()

            except TimeoutError:
                pass

        server_socket.close()