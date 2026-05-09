""""Programme principal qui créer un client complet à partir de server_main

Fait par Lucas"""
from ui import affichage
from ui_initialisation import Controle as LobbyControle
import threading

def main():
    def on_client_ready(client, pseudo):
        client._start_receiving()

        def attendre_et_ouvrir():
            state, pname = None, None
            while state is None:
                state, pname = client.get_state()
            lobby.after(0, lambda: ouvrir_jeu(client, state, pname))

        threading.Thread(target=attendre_et_ouvrir, daemon=True).start()

    def ouvrir_jeu(client, state, player_name):
        lobby.destroy()
        root, controle = affichage(state, player_name)
        controle.send_action = client.send_action

        def client_loop():
            gs, pn = client.get_state()
            if gs:
                if isinstance(gs, dict) and gs.get("type") == "choose_color":
                    if gs.get("player") == pn:
                        controle.demander_couleur()
                else:
                    controle.recevoir_game_state(gs, pn)
            root.after(50, client_loop)

        root.after(50, client_loop)
        root.mainloop()

    lobby = LobbyControle(on_client_ready=on_client_ready)
    lobby.mainloop()

if __name__ == "__main__":
    main()
