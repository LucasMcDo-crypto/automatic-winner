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
  game_state = server.Host.get_state
  liste_joueurs = [player["name"] for player in game_state["players"]]
  Logic.Partie(liste_joueurs)
  #Convertir le dict de fin de partie 

def Game_Loop():
  while (len(player["cards"]) == 0 for player in fake_state["players"]):
    
  #Phase où quelqu'un a gagné
  
