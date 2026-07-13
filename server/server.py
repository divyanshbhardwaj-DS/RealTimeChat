import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)


def handle_client(client):
    while True:
        try:
            message = client.recv(1024)

            if not message:
                break

            print("📨", message.decode())

            broadcast(message,client)

        except:
            break

    if client in clients:
        clients.remove(client)

    client.close()

def receive():
    print(f"✅ Server Started on {HOST}:{PORT}")

    while True:
        client, address = server.accept()

        print(f"🔗 Connected : {address}")

        clients.append(client)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()