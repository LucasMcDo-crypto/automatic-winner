""""Programme principal qui créer un client complet à partir de server_main

"""
import ui
from fake_state import fake_state

1. créer fenêtre Tk
2. créer controller
3. connecter serveur
4. lancer UI loop

def initialisation(game_state):
    ui.affichage(game_state)

def boucle_client():
    if game_change == True:
        ui.controle.recevoir_game_state(game_state)
        
    else:
        continue

if __name__ == "__main__":
    initialisation(fake_state)
    client_loop(fake_state)
