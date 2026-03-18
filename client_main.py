""""Programme principal qui créer un client complet à partir de server_main

"""
import ui

1. créer fenêtre Tk
2. créer controller
3. connecter serveur
4. lancer UI loop

def affichage(game_state):
    """Affiche la UI avec un GameState."""

    root = Tk.Tk()
    root.title("MVC - UNO TEST")
    root.state("zoomed")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    controle = Controle(root)

    # ---------------------------
    # GAME STATE 
    # ---------------------------
  
    # Injecte l'état 
    controle.recevoir_game_state(game_state)

    root.mainloop()

if __name__ == "__main__":
    _test()
