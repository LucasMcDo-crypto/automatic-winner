"""Programme principal qui créer une partie complète avec plusieurs joueurs

"""
import server
import Logic
import game_state_empty
from fake_state import fake_state

1. créer GameServer
2. écouter connexions (stocke les joueurs)
3. créer partie quand joueurs prêts
4. boucle infinie

def initialisation_server():
  host = server.Host()
  host.start()
  return host

def initialisation_client():
  client = server.Client()
  client.start()
  return client

def game_loop():
  liste_joueurs = server.Host().get_player_list()
  Logic.Partie(liste_joueurs)
  #Convertir le dict de fin de partie 
  while (len(player["cards"]) == 0 for player in fake_state["players"]):
    def send_state_to_all(self):

    for client, nickname in self.clients.items():

        msg = {
            "type": "state",
            "player_name": nickname,
            "game_state": self.game_state
        }

        client.sendall(
            (json.dumps(msg) + "\n").encode()
        )
  #Phase où quelqu'un a gagné
  
if __name__ == "__main__":
    user = input("host or client ? \n")

    if user.lower() not in ("host", "client"):
        raise Exception("Misinput, try again")
    
    match user.lower():
        case "host":
            host = initialisation_server()
            host.game_state = fake_state
            
        case "client":
            client = initialisation_client()
            
