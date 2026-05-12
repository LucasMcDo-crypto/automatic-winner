""""Programme principal qui créer un client complet à partir de server_main

Fait par Lucas"""
from ui import affichage
from ui_initialisation import Controle as LobbyControle
import threading

def main():
    """Gère le lien complet entre server_main et les ui des joueurs une fois l'initialisation des rôles terminée."""
    def on_client_ready(client, pseudo):
        """Lance la fonction ouvrir_jeu une fois le game_state reçu."""
        client._start_receiving()

        def attendre_et_ouvrir():
            state, pname = None, None
            while state is None:
                state, pname = client.get_state()
            lobby.after(0, lambda: ouvrir_jeu(client, state, pname))

        threading.Thread(target=attendre_et_ouvrir, daemon=True).start()

    def ouvrir_jeu(client, state, player_name):
        """Détruit l'interface de ui_initialisation et la remplace par celle de ui avec le joueur qu'elle doit gérer."""
        lobby.destroy()
        root, controle = affichage(state, player_name)
        controle.send_action = client.send_action

        def client_loop():
            """Traite chaque réception de game_state et gère le cas où le joueur doit choisir une couleur."""
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
