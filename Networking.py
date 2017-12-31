import socket


class Networking:
    def __init__(self,host_ip_address,port,nb_connections):
        self.host_ip_address = host_ip_address
        self.port = port
        self.self.nb_connections = nb_connections
        self.L_sockets = []

    def run_server_side(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((self.host_ip_address, self.port))
        # Define socket with nb_connections max connexions
        serversocket.listen(self.nb_connections)
        print('Server started: Waiting for users')

        while True:
            # Waiting for all players connections
            for i in range(self.nb_connections):
                connection, address = serversocket.accept()
                self.L_sockets.append(connection)
            print('All players connected')
            self.server_socket = serversocket
            #buf = connection.recv(1024).decode()
            #if len(buf) > 0:
            #    print buf
            #    break
            #return buf
    def server_send_data(self,client_socket,data):
        client_socket.send(data)
        buf = self.client_socket.recv(1024)
        if buf=='received':
            return 'Transmitted'
        else:
            return 'Non Transmitted'

    def server_receive_data(self,client_socket):
        data = client_socket.recv(1024)
        client_socket.send('received')

    def run_client_side(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host_ip_address,self.port))
        self.current_client_socket = client_socket

    def client_send_data(self,data):
        self.current_client_socket.send(data)
        buf = client_socket.recv(1024)
        if buf=='received':
            return 'Transmitted'
        else:
            return 'Non Transmitted'

    def client_receive_data(self,data):
       data = self.current_client_socket.recv(1024)
       current_client_socket.send('received')
       return data




