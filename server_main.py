"""Programme principal qui créer une partie complète avec plusieurs joueurs
Fait par Lucas"""
import server
import Logic
from ui_initialisation import Controle
import threading
from fake_state import fake_state
 
 
def game_loop(host, app):
    noms = host.get_player_list()
    if len(noms) < 2:
        app.afficher("Il faut au moins 2 joueurs !")
        return
 
    partie = Logic.Partie(tuple(noms))
    app.afficher(f"Partie lancée avec {noms}")
 
    while partie.vainqueur is None:

        joueur = partie.obtenir_prochain()

        # appliquer immédiatement les +2/+4
        joueur.piocher_debut()

        # envoyer l'état APRÈS mise à jour complète
        game_state = creer_game_state(partie)

        host.broadcast({
            "type": "state",
            "state": game_state
        })

        while True:
            player_name, action = host.action_queue.get()
            if player_name == joueur.nom:
                break
        
        joueur.piocher_debut()
 
        # Gère le cas où on pose une carte
        if action["type"] == "PLAY_CARD":
            try:
                joueur.poser(action["card"])
 
                # Si la carte demande un choix de couleur
                if joueur.choix:
                    host.broadcast({
                        "type": "choose_color",
                        "player": joueur.nom
                    })
 
                    while True:
                        player_name, action = host.action_queue.get()
                        if (
                            player_name == joueur.nom
                            and action["type"] == "CHOOSE_COLOR"
                        ):
                            joueur.choisir(action["color"])
                            break
 
            except ValueError as e:
                print(f"Carte invalide : {e}")
 
        # Gère le cas où le joueur prend une carte et passe son tour
        elif action["type"] == "DRAW_CARD":
            joueur.passer_tour()
            
 
    # Diffuser l'état final avec le gagnant
    host.broadcast({
        "type": "state",
        "state": creer_game_state(partie)
    })
 
 
def on_game_start(host, app):
    """Appelé quand le host clique sur 'Lancer la partie'."""
    thread = threading.Thread(
        target=game_loop,
        args=(host, app),
        daemon=True
    )
    thread.start()
 
 
def creer_game_state(partie):
    """Convertit une instance de Logic.Partie en game_state JSON-compatible."""
 
    players = []
 
    for joueur in partie.joueurs:
 
        # Cartes jouables ou non
        etat_main = []
 
        if joueur == partie._joueur_jeu:
            cartes_possibles = joueur.cartes_possibles()
            for carte in joueur.main:
                if str(carte) in cartes_possibles:
                    etat_main.append("normal")
                else:
                    etat_main.append("disabled")
        else:
            etat_main = ["disabled"] * len(joueur.main)
 
        players.append({
            "name": joueur.nom,
            "cards": [str(carte) for carte in joueur.main],
            "etat_main": etat_main
        })
 
    # Calcul de la défausse — EN DEHORS de la boucle for
    # Si la carte est un Wild (ss) ou Wild+4 (s+4), Logic a pu changer
    # sa couleur via choisir() : on force le préfixe 's' pour retrouver
    # le bon nom de fichier image.
    defausse = partie.carte_defausse
    if defausse.chiffre == Logic.Chiffre.SPECIAL:
        discard_str = 'ss'  # 'ss' 
    elif defausse.chiffre == Logic.Chiffre.PLUS_QUATRE:
        discard_str = 's+4' #'s+4'
    else:
        discard_str = str(defausse)
 
    game_state = {
        "discard": discard_str,
        "direction": 1 if partie._sens_horaire else -1,
        "current_player": partie._joueur_jeu.nom,
        "players": players,
        "draw_stack": partie._joueur_jeu.pioche,
        "winner": None if partie.vainqueur is None else partie.vainqueur.nom
    }
 
    return game_state
 
 
def main():
    app = Controle(on_game_start=lambda: on_game_start(app.host, app))
    app.mainloop()
 
 
if __name__ == "__main__":
    main()
