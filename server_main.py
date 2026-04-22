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
  server.Client.start()
  game_state = server.Host.get_state
  Logic.Partie(game_state)
  
