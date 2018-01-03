import socket


class Networking:
    def __init__(self,host_ip_address,port,nb_connections):
        self.host_ip_address = host_ip_address
        self.port = port
        self.nb_connections = nb_connections
        self.L_sockets = []
        self.host_socket = None
        self.num_player = 0

    def run_server_side(self,ball_coefs):
        self.coef_x, self.coef_y = ball_coefs
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serversocket.bind((self.host_ip_address, self.port))
        # Define socket with nb_connections max connexions
        serversocket.listen(self.nb_connections)
        print('Server started: Waiting for users')

        # Waiting for all players connections
        for i in range(self.nb_connections):
            connection, address = serversocket.accept()
            # Send to the player his number
            connection.send(str(i+2))
            connection.recv(1024)
            # Send the ball direction to player to synchronize everybody
            connection.send(str(self.coef_x))
            connection.recv(1024)
            connection.send(str(self.coef_y))
            connection.recv(1024)
            self.L_sockets.append(connection)
        for sock in self.L_sockets:
            sock.settimeout(0.01)
        print('All players connected')
        self.server_socket = serversocket
        #buf = connection.recv(1024).decode()
        #if len(buf) > 0:
        #    print buf
        #    break
        #return buf

    def server_broadcast_message(self,exception,msg):
        for i in range(len(self.L_sockets)):
            if i+2!=exception:
                self.L_sockets[i].send(str(i+2)+':'+str(msg))

    def server_send_data_to_all_players(self,data):
        for client_socket in self.L_sockets:
            client_socket.send(data)

    def server_receive_data(self,client_socket):
        data = client_socket.recv(1024)

    # Detect if a client message was sent and then send it to all other players
    def server_detect_if_client_sent_message(self):
        for i in range(len(self.L_sockets)):
            buf=''
            try:
                buf = self.L_sockets[i].recv(1024)
            except:
                pass
            if len(buf)>0:
                for j in range(len(self.L_sockets)):
                    if j!=i:
                        self.L_sockets[j].send(str(i+2)+':'+str(buf))
                return str(i+2)+':'+str(buf)
        return ''

    def run_client_side(self):
        host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_socket.connect((self.host_ip_address,self.port))
        self.num_player = int(host_socket.recv(1024))
        host_socket.send('OK')
        self.coef_x = int(host_socket.recv(1024))
        host_socket.send('OK')
        self.coef_y = int(host_socket.recv(1024))
        host_socket.send('OK')
        host_socket.settimeout(0.01)
        self.host_socket = host_socket

    def client_send_data(self,data):
        self.host_socket.send(str(self.num_player)+':'+str(data))

    def client_receive_data(self,data):
       data = self.host_socket.recv(1024)
       return data

    def client_detect_if_server_sent_message(self):
        buf=''
        try:
            buf = self.host_socket.recv(1024)
        except:
            pass
        if len(buf)>0:
            return buf
        return ''


