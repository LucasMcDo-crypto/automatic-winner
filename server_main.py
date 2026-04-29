"""Programme principal qui créer une partie complète avec plusieurs joueurs

"""
import server
import Logic
import game_state_empty

1. créer GameServer
2. écouter connexions (stocke les joueurs)
3. créer partie quand joueurs prêts
4. boucle infinie

def Initialisation_Server():
  server.Host().start()

def Initialisation_Client():
  server.Client().start()

def Game_Loop():
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
  
