"""Programme de chatroom de test. Changer l'adresse IP chez le client pour essayer le code.

Il suffit de changer le type de données à envoyer afin de communiquer les règles du jeu avec les clients et le serveur

fait par Kevin DAO"""

import socket, threading, json

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
PORT = 65432


class Host:
    """classe du serveur 'host'"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clients: dict[socket.socket, str] = {}
    def __init__(self):
        self.server.bind((ip , PORT))
        self.server.listen()
        self.close_server()
        
    def accept_client(self):
        """Accepter la connexion d'un client et reçoit son pseudonyme."""
        print("Server listening...")
        self.server.settimeout(1)
        while True:
            try:
                client, _ = self.server.accept()
                nickname = client.recv(1024).decode()
                self.clients[client] = nickname
                
                for client in self.clients:
                    msg = {
                        "nickname": nickname,
                        "message": f"{nickname} joined the game"
                        }
                    client.sendall(json.dumps(msg).encode())
                
            except socket.timeout:
                continue
            print("Connected by", self.clients[client])
            
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()
            
    def handle_client(self, client):
        "Gérer le reçu des messages et la déconnexion des clients."
        with client:
            while True:
                try:
                    data = client.recv(1024)
                    if not data:
                        break
                    self.send(data)
                except ConnectionResetError:
                    print(f"A connexion error occured with client {self.clients[client]}")
                    break
        print(f"Connection closed with {self.clients[client]}")
        if client in self.clients:
            del self.clients[client]

    def close_server(self):
        """Fermer le serveur lorsque le programme est arrêté avec Ctrl+C."""
        try:
            self.accept_client()
        except KeyboardInterrupt:
            print("\nStopping server...")
        finally:
            self.server.close()
            
    def send(self, data):
        """Envoyer le message à tous les clients"""
        for client in list(self.clients):
            try:
                client.sendall(data)
            except:
                del self.clients[client]
        
        
class Client:
    """classe du client"""
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self):
        #ip_serveur = input("please type the ip address of the server: ")
        self.nickname = input("enter your nickname: ")
        
        self.test_socket.connect(("10.134.55.139", PORT))
        self.test_socket.sendall(self.nickname.encode())
        
        thread = threading.Thread(target=self.receive)
        thread.daemon = True
        thread.start()
        
        self.send()
        
    def send(self):
        """Envoyer un message au serveur qui l'affiche aux autres utilisateurs et déconnecter lorsque
           le client écrit 'quit'"""
        print("type 'quit' to end connexion with server")
        while True:
            message = input("")
            if message.lower() == "quit":
                self.quit()
                break
            
            msg = {
                "nickname": self.nickname,
                "message": message
                }
            
            serialized_msg = json.dumps(msg).encode()
        
            try:
                self.test_socket.sendall(serialized_msg)
            except OSError:
                break
            
    def quit(self):
        msg = {
            "nickname": "SERVER",
            "message": f"{self.nickname} left the game"
            }
        self.test_socket.sendall(json.dumps(msg).encode())
        self.test_socket.shutdown(socket.SHUT_RDWR)
        self.test_socket.close()
        print("Connexion with server has been terminated")
        
    def receive(self):
        """Recevoir les messages des autres clients"""
        while True:
            try:
                data = self.test_socket.recv(1024)
                if not data:
                    break
                deserialized_data = json.loads(data.decode())
                print(f"{deserialized_data['nickname']} said : {deserialized_data['message']}")
            except OSError:
                break
    
    
if __name__ == "__main__":
    #print(ip)
    user = input("host or client ? \n")
    if user.lower() not in ("host", "client"):
        raise Exception("Misinput, try again")
    match user.lower():
        case "host":
            Host()
        case "client":
            Client()
            
    
