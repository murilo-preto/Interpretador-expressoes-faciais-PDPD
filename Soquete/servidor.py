import pickle
import socket
import select

################################ Server config ################################
header_len = 10
ip = "127.0.0.1"
port = 1500

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((ip, port))
server_socket.listen(5)

sockets_list = [server_socket]
clients = {}

interpretador_list = []
receptor_list = []

print(f'Esperando conexões em {socket.gethostname()}:{port}')


################################ Funções ################################
def recv_dict(client_socket):

    try:
        msg_header = client_socket.recv(header_len)

        if not len(msg_header):
            return False

        msg_len = int((msg_header).decode("utf-8").strip())

        msg = client_socket.recv(msg_len)
        return pickle.loads(msg)
        
    except:
        return False


def recv_type(client_socket):

    try:
        msg_header = client_socket.recv(header_len)

        if not len(msg_header):
            return False

        msg_len = int((msg_header).decode("utf-8").strip())
        msg = client_socket.recv(msg_len)

        return msg.decode("utf-8")
        
    except:
        return False
 

def send_dict(header_len, dict, client_socket):
    data = pickle.dumps(dict)

    header = bytes(f"{len(data):<{header_len}}", "utf-8")
    msg = header+data

    client_socket.send(msg)


################################# Logic ################################
while True:
    r_list, w_list, x_list = select.select(sockets_list, [], sockets_list)

    for notified_socket in r_list:
        if notified_socket == server_socket:

            print("Conexão nova:", notified_socket)
            notified_socket, client_address = server_socket.accept()

            type = recv_type(notified_socket)

            clients[notified_socket] = type
            sockets_list.append(notified_socket)

            if type == "receptor":
                receptor_list.append(notified_socket)
                print("Receptor conectado!")
                continue

            elif type == "interpretador":
                interpretador_list.append(notified_socket)
                print("Interpretador conectado!")
                
        else:
            print("Recebendo dados:",notified_socket)
            type = clients[notified_socket]
            fex_dict = recv_dict(notified_socket)

            if fex_dict is False:
                sockets_list.remove(notified_socket)
                
                if type == "receptor":
                    receptor_list.remove(notified_socket)

                elif type == "interpretador":
                    interpretador_list.remove(notified_socket)

                del clients[notified_socket] 
                continue   

            print(fex_dict)

            for notified_socket in receptor_list:
                send_dict(header_len, fex_dict, notified_socket)
    
    for notified_socket in x_list:
        sockets_list.remove(notified_socket)

        type = clients[notified_socket]
        if type == "receptor":
            receptor_list.remove(notified_socket)

        elif type == "interpretador":
            interpretador_list.remove(notified_socket)

        del clients[notified_socket]   