"""Programme de chatroom de test. Changer l'adresse IP chez le client pour essayer le code.

Il suffit de changer le type de données à envoyer afin de communiquer les règles du jeu avec les clients et le serveur.
Actuellement, le programeme ne sert que de chatroom.

fait par Kevin DAO"""

import socket
import threading
import json
from fake_state import fake_state


class Host:
    """classe du serveur 'host'"""
    ip = socket.gethostbyname(socket.gethostname())
    PORT = 65432

    def __init__(self):
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.ip , self.PORT))
        self.server.listen()
        
        self.clients: dict[socket.socket, str] = {}
        self.running = True

        self.game_state =  {}
        

    def start(self) -> None:
        """Lancer le serveur. Lorsque Ctrl+C est pressé, le programme est arrêté."""
        print(f"Server started on ip address: {self.ip} and port: {self.PORT}")

        try:
            self._accept_client()
        except KeyboardInterrupt:
            print("\nStopping server...")
        finally:
            self.stop()
            

    def get_state(self) -> dict:
        """Retourner le Game State actuel."""
        return self.game_state
    

    def get_player_list(self) -> list:
        """Retourner la liste des pseudos des joueurs."""
        player_list = [self.clients[client] for client in self.clients]
        return player_list

        
    def _accept_client(self) -> None:
        """Accepter la connexion d'un client et reçoit son pseudonyme."""
        print("Server listening...")
        self.server.settimeout(1)

        while self.running:
            try:
                client, _ = self.server.accept()

                data = client.recv(4192)
                data_json = json.loads(data.decode())
                
                if data_json['type'] == "nickname":
                    nickname = data_json['name']
                    self.clients[client] = nickname

                self.broadcast({
                    "type": "system",
                    "nickname": nickname,
                    "message": f"{nickname} joined the game"
                })
                
                print("Connected by", self.clients[client])
                
                thread = threading.Thread(target=self._handle_client, args=(client,), daemon=True)
                thread.start()
                
            except socket.timeout:
                continue

            
    def _handle_client(self, client: socket.socket) -> None:
        """Gérer le reçu des messages et la déconnexion des clients."""
        nickname = self.clients.get(client, "Unknown")

        try:
            while True:
                data = client.recv(4192)
                if not data:
                    break
                data_json = json.loads(data.decode())

                if data_json['type'] == "play":
                    self.change_state(top_card=data_json['discard'], current_player=data_json['player_name'])
                    self.broadcast(self.game_state) # affichage de test pour le game state
                else:
                    self.broadcast(data_json)

        except ConnectionResetError:
            print(f"A connexion error occured with client {nickname}")
            
        finally:
            self._disconnect_client(client)

    
    def change_state(self, top_card: str, current_player: str) -> None:
        """Changer le game state avec la dernière carte jouée et les cartes restantes en main."""
        self.game_state.update({"discard": top_card})
        for player in self.game_state["players"]:
            if player["name"] == current_player:
                player["cards"].remove(top_card)


    def _disconnect_client(self, client: socket.socket) -> None:
        """Gérer la déconnexion des clients"""
        nickname = self.clients.get(client, "Unknown")
        
        if client in self.clients:
            del self.clients[client]

        client.close()
        
        print(f"Connection closed with {nickname}")

        self.broadcast({
            "type": "system",
            "nickname": "",
            "message": f"{nickname} left the game"
        })

            
    def broadcast(self, message: dict) -> None:
        """Envoyer le message à tous les clients"""
        data = (json.dumps(message) + "\n").encode()

        for client in list(self.clients):
            try:
                client.sendall(data)
            except:
                self._disconnect_client(client)


    def stop(self) -> None:
        """Gérer la fermeture du serveur et ferme tous les clients."""
        self.running = False

        for client in list(self.clients):
            client.close()
        
        self.server.close()
        print("Server closed")
        

class Client:
    """classe du client"""
    def __init__(self):
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True
        

    def start(self) -> None:
        """Activer la connexion et la gestion des messages"""
        try:
            self._connect()
            self._start_receiving()
            self._send_loop()
        except KeyboardInterrupt:
            print("\nClosing client...")
        finally:
            self.stop()
            
    
    def send_nickname(self) -> None:
        """Envoyer le pseudonyme au serveur"""
        self.nickname = input("enter your nickname: ")
        msg = {
            "type": "nickname",
            "name": self.nickname
        }
        self.socket.sendall(json.dumps(msg).encode())


    def _connect(self) -> None:
        """Connecter le client au serveur serveur"""
        self.socket.connect((Host.ip, Host.PORT))
        self.send_nickname()
        print("Connected to server")


    def _start_receiving(self) -> None:
        """Recevoir plusieurs messages avec un thread"""
        thread = threading.Thread(target=self._receive, daemon=True)
        thread.start()

    
    def _send_loop(self) -> None:
        """Envoyer un message au serveur qui l'affiche aux autres utilisateurs et déconnecter lorsque
           le client écrit 'quit'"""
        
        print("type 'quit' or press Ctrl+C to end connexion with server")

        while self.running:
            message = input()
            if message.lower() == "quit":
                self.running = False
                break
            elif message.lower() == "send": # envoyer send pour tester le changement de Game State
                self.send_state("Blue-8")
            
            msg = {
                "type": "chat",
                "nickname": self.nickname,
                "message": message
            }

            try:
                self.socket.sendall(json.dumps(msg).encode())
            except OSError:
                break


    def send_state(self, card_played: str) -> None:
        """Envoyer les informations du joueur au serveur"""
        state = {
            "type": "play",
            "discard": card_played,
            "player_name": self.nickname
        }

        try:
            self.socket.sendall(json.dumps(state).encode())
        except OSError:
            pass

    
    def _receive(self) -> None:
        """Recevoir les messages des autres clients"""
        buffer = ""

        while self.running:
            try:
                data = self.socket.recv(4192)

                if not data:
                    break

                buffer += data.decode()

                while "\n" in buffer:
                    msg_str, buffer = buffer.split("\n", 1)
                    msg = json.loads(msg_str)

                    if msg['type'] == "chat":
                        print(f"{msg['nickname']} said : {msg['message']}")
                    elif msg['type'] == "state":
                        print(msg)
                    else:
                        print(msg["message"])

            except (OSError, json.JSONDecodeError):
                break

        self.running = False
        
            
    def stop(self) -> None:
        """Gérer la déconnexion"""
        self.running = False
        
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except:
            pass

        self.socket.close()
        print("Connexion with server has been terminated")
    
    
if __name__ == "__main__":
    user = input("host or client ? \n")

    if user.lower() not in ("host", "client"):
        raise Exception("Misinput, try again")
    
    match user.lower():
        case "host":
            host = Host()
            host.game_state = fake_state
            host.start()
            
        case "client":
            client = Client()
            client.start()
            

