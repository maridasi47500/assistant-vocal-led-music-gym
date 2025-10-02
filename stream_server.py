import socket
import threading
import requests

# Configuration du serveur
HOST = '0.0.0.0'  # Écoute sur toutes les interfaces réseau
PORT = 8001
RADIO_STREAM_URL = 'https://stunnel1.cyber-streaming.com:9162/stream?'  # Remplacez par l'URL du flux radio

def handle_client(client_socket):
    """Gère la connexion avec un client."""
    try:
        with requests.get(RADIO_STREAM_URL, stream=True) as stream:
            for chunk in stream.iter_content(chunk_size=1024):
                if not chunk:
                    break
                client_socket.sendall(chunk)
    except Exception as e:
        print(f"Erreur avec le client : {e}")
    finally:
        client_socket.close()

def start_server():
    """Démarre le serveur."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Serveur démarré sur {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Client connecté depuis {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == '__main__':
    start_server()

