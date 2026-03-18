""""Programme principal qui créer un client complet à partir de server_main

"""
import ui
from fake_state import fake_state
from server import client

1. créer fenêtre Tk
2. créer controller
3. connecter serveur
4. lancer UI loop

client = Client()
client.connect()
client.start_receiving()

root, controle = ui.affichage(fake_state)

controle.send_action = client.send_action


def client_loop():

    state = client.get_state()

    if state:
        controle.recevoir_game_state(state)

    root.after(50, client_loop)


root.after(50, client_loop)
root.mainloop()

if __name__ == "__main__":
    client_loop(fake_state)
