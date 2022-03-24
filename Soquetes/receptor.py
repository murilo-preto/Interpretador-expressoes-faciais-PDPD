import socket
import pickle

header_len = 10
ip = "127.0.0.1"
port = 1500

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, port))

client_socket.setblocking(False)


def send_type(type):
    data = bytes(type, "utf-8")

    header = bytes(f"{len(data):<{header_len}}", "utf-8")
    msg = header+data

    client_socket.send(msg)


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


################################# Logic ################################
send_type("receptor")
print("Receptor conectado ao servidor. Esperando por dados.")
while True:
    fex_dict = recv_dict(client_socket)

    if fex_dict == False:
        pass
    else:
        print(fex_dict)