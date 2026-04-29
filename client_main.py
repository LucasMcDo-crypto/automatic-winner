""""Programme principal qui créer un client complet à partir de server_main

Fait par Lucas"""
import ui
from fake_state import fake_state
from server import Client


client = Client()
client._connect()
client._start_receiving()

root, controle = ui.affichage(fake_state)

controle.send_action = client.send_action


def client_loop():

    game_state, player_name = client.get_state()

    if game_state:
        controle.recevoir_game_state(game_state, player_name)

    root.after(50, client_loop)


root.after(50, client_loop)
root.mainloop()

if __name__ == "__main__":
    client_loop(fake_state)
