import socket
import threading

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            print(f"\n📩 {message}")
        except:
            print("Disconnected from server.")
            client.close()
            break


threading.Thread(target=receive_messages, daemon=True).start()

print("✅ Connected to Server")
print("Type your messages below:\n")

while True:
    message = input()
    client.send(message.encode())