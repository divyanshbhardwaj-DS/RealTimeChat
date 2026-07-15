import socket
import threading
from modules.chat import save_message
HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

clients = {}
lock = threading.Lock()


def send_online_users():
    """Send updated online users list to everyone."""
    with lock:
        usernames = ",".join(clients.values())
        data = f"USERS:{usernames}"

        for client in list(clients.keys()):
            try:
                client.sendall(data.encode())
            except:
                remove_client(client)


def broadcast(message, sender=None):
    """Send message to all clients except sender."""
    with lock:
        for client in list(clients.keys()):
            if client != sender:
                try:
                    client.sendall(message.encode())
                except:
                    remove_client(client)


def remove_client(client):
    """Disconnect client safely."""
    with lock:
        if client in clients:
            username = clients[client]
            print(f"🔴 {username} disconnected")
            del clients[client]

    try:
        client.close()
    except:
        pass
        save_message(
            "System",
            "Global",
            f"🔴 {username} left the chat."
        )
    send_online_users()


def handle_client(client):
    try:
        username = client.recv(1024).decode().strip()

        if username == "":
            client.close()
            return

        with lock:
            clients[client] = username

        print(f"🟢 {username} joined")
    
        send_online_users()

        broadcast(
            f"🟢 {username} joined the chat.",
            sender=client
        )

        while True:

            data = client.recv(1024)

            if not data:
                break

            text = data.decode()

            print(text)

            save_message(
                username,
                "Global",
                text
            )

            broadcast(
                text,
                sender=client
            )

    except Exception as e:
        print("ERROR:", e)

    finally:
        remove_client(client)


def start_server():
    print(f"✅ Server Started on {HOST}:{PORT}")

    while True:

        client, address = server.accept()

        print(f"🔗 Connected : {address}")

        thread = threading.Thread(
            target=handle_client,
            args=(client,),
            daemon=True
        )

        thread.start()

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n🛑 Server Stopped")
        server.close()