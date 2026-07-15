import socket
import threading


HOST = "127.0.0.1"
PORT = 5000


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

server.bind(
    (HOST, PORT)
)

server.listen()


clients = {}

lock = threading.Lock()



# ---------- Send Online Users ----------

def send_user_list():

    with lock:

        users = list(clients.values())


        print(
            "ONLINE USERS:",
            users
        )


        data = "USERS:" + ",".join(users)


        for client in list(clients.keys()):

            try:

                client.sendall(
                    data.encode()
                )


            except:

                remove_client(client)



# ---------- Broadcast Message ----------

def broadcast(message, sender=None):

    for client in list(clients.keys()):

        if client != sender:

            try:

                client.sendall(
                    message
                )


            except:

                remove_client(client)



# ---------- Remove Client ----------

def remove_client(client):

    with lock:

        if client in clients:

            username = clients[client]

            print(
                f"🔴 {username} disconnected"
            )


            del clients[client]


    try:

        client.close()

    except:

        pass


    send_user_list()



# ---------- Handle Each Client ----------

def handle_client(client):

    try:

        # receive username

        username = client.recv(
            1024
        ).decode().strip()


        if not username:

            client.close()
            return



        with lock:

            clients[client] = username



        print(
            f"🟢 {username} joined"
        )


        # update online users

        send_user_list()



        # notify others

        broadcast(
            f"🟢 {username} joined the chat".encode(),
            client
        )



        while True:


            message = client.recv(
                1024
            )


            if not message:

                break



            print(
                f"{username}: {message.decode()}"
            )



            broadcast(
                message,
                client
            )



    except Exception as e:

        print(
            "Error:",
            e
        )



    finally:

        remove_client(client)



# ---------- Start Server ----------

def receive():

    print(
        f"✅ Server Started on {HOST}:{PORT}"
    )


    while True:


        client, address = server.accept()


        print(
            f"🔗 Connected: {address}"
        )


        thread = threading.Thread(
            target=handle_client,
            args=(client,)
        )


        thread.daemon = True

        thread.start()



if __name__ == "__main__":

    receive()