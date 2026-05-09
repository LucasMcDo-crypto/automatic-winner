"""Programme qui affiche la vue d'un joueur précis.

Fait par Lucas"""
import tkinter as Tk
import math
from PIL import Image, ImageTk
from fake_state import fake_state
import os

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, "images")

class Model:
    def __init__(self):
        self.ratio = 0.8   # proportion du diamètre du cercle par rapport à  la fenêtre


class Vue:
    def __init__(self, root, controle):
        self.controle = controle
        self.game_state = None

        # Frame principal
        self.frame = Tk.Frame(root)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.configure(background='white')

        # Configuration grid (IMPORTANT)
        for i in range(3):
            self.frame.rowconfigure(i, weight=1)
            self.frame.columnconfigure(i, weight=1)
        
        # Canvas central
        self.canvas = Tk.Canvas(self.frame, bg="white")
        self.canvas.grid(row=0, column=3, columnspan=1000, sticky="nsew")

        self.largeur = 1
        self.hauteur = 1

        self.canvas.bind("<Configure>", self.redimensionner)
        
        #Bouttons supplémentaires
        self.button_bas2 = Tk.Button(self.frame, text="Passer le tour et prendre une carte", state="disabled", font=("Arial", 15), command=self.controle.passer_tour)
        self.button_bas2.grid(row=2, columnspan=1000, sticky="nsew")
        

    #affichage de toutes les carte   
    
    def carte_en_jeu(self, carte):
        """Affiche la carte donnée qui vient d'être jouée."""
        if hasattr(self, "boutons_cartes1"):
            for btn in self.boutons_cartes1:
                btn.destroy()
        self.images_originales1 = []
        self.images_tk1 = []
        self.boutons_cartes1 = []
        img_path = os.path.join(IMAGES_DIR, f"{carte}.png")
        img = Image.open(img_path)
        self.images_originales1.append(img)

        img_tk = ImageTk.PhotoImage(img)
        self.images_tk1.append(img_tk)

        btn = Tk.Label(self.frame, image=img_tk)
        btn.grid(row=0, column=1)

        self.boutons_cartes1.append(btn)
        self.frame.columnconfigure(2, weight=2)
        
    def ma_main(self, list_main, état_main):
        """Affiche toutes les cartes du joueur concerné et autorise ou non la possibilité de les jouer."""
        # Détruire les anciens boutons
        if hasattr(self, "boutons_cartes"):
            for btn in self.boutons_cartes:
                btn.destroy()
        
        self.images_originales = []
        self.images_tk = []
        self.boutons_cartes = []
        for i in range(len(list_main)):
            img_path = os.path.join(IMAGES_DIR, f"{list_main[i]}.png")
            if not os.path.exists(img_path):
                print("Image introuvable :", img_path)
            img = Image.open(img_path)
            self.images_originales.append(img)

            img_tk = ImageTk.PhotoImage(img)
            self.images_tk.append(img_tk)
            
            if str(état_main[i]) == "disabled":
                couleur = 'red'
            else:
                couleur = 'green'

            btn = Tk.Button(self.frame, image=img_tk, bg=couleur, state=str(état_main[i]), command=lambda i=i: self.controle.jouer_carte(i))
            btn.grid(row=1, column=i)

            self.boutons_cartes.append(btn)
            self.frame.columnconfigure(i, weight=1)


    def adapter_images_cartes(self):
        """règle la taille des images des cartes pour les adapter aux différentes tailles des fenêtres."""
        if not hasattr(self, "boutons_cartes") or len(self.boutons_cartes) == 0:
            return
        largeur_case = self.frame.winfo_width() // len(self.boutons_cartes)
        hauteur_case = self.frame.winfo_height() // 4  # approx hauteur ligne cards

        for i, img_original in enumerate(self.images_originales):

            w, h = img_original.size

            ratio = min(largeur_case / w, hauteur_case / h)

            new_w = int(w * ratio)
            new_h = int(h * ratio)

            resized = img_original.resize((new_w, new_h), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(resized)

            self.images_tk[i] = img_tk  # garder référence
            self.boutons_cartes[i].configure(image=img_tk)

    def redimensionner(self, event):
        """Fait la mise à jour du programme en modifiant la taille des widgets et les variables"""
        self.largeur = event.width
        self.hauteur = event.height
        self.controle.mettre_a_jour()
        self.adapter_images_cartes()


    def dessiner(self, ratio, noms_joueurs, nbr_cartes, joueur_actif):
        """Affiche un cercle avec les joueurs,
        leur nombre de cartes restantes
        et le joueur qui est entrain de jouer"""
        self.canvas.delete("all")

        rayon = min(self.largeur, self.hauteur) * ratio / 2
        cx = self.largeur / 2
        cy = self.hauteur / 2

        self.canvas.create_oval(
            cx - rayon, cy - rayon,
            cx + rayon, cy + rayon,
            fill="lightgreen",
            outline=""
        )

        offset = 15

        for i in range(len(noms_joueurs)):
            angle = (2 * math.pi / len(noms_joueurs)) * (-i+2)
            x = cx + rayon * math.cos(angle)
            y = cy - rayon * math.sin(angle)

            couleur = "red" if i == joueur_actif else "black"

            self.canvas.create_text(x, y, text=noms_joueurs[i], fill=couleur, font=("Arial", 15))

            self.canvas.create_text(x, y + offset, text=f"{len(nbr_cartes[i])} carte(s)", fill=couleur, font=("Arial", 12))
    
    def set_bouton_tour(self, etat):
        self.button_bas2.configure(state=etat)


class Controle:
    def __init__(self, root):
        self.model = Model()
        self.vue = Vue(root, self)
        self.game_state = None
        self.player_name = None
        self.send_action = None
    
    def jouer_carte(self, index):
        joueur = next(
            (j for j in self.game_state["players"]
             if j["name"] == self.player_name),
            None
        )

        if joueur is None:
            print("Joueur introuvable")
            return

        carte = joueur["cards"][index]

        action = {
            "type": "PLAY_CARD",
            "card": carte
        }

        if self.send_action:
            self.send_action(action)
    
    def passer_tour(self):
        action = {
            "type": "DRAW_CARD"
        }

        if self.send_action:
            self.send_action(action)

    def mettre_a_jour(self):
        """Gère le changement des variables présentent dans la vue."""
        if not self.game_state:
            return

        noms = [p["name"] for p in self.game_state["players"]]
        nbr = [p["cards"] for p in self.game_state["players"]]
        
        joueur_actif = noms.index(self.game_state["current_player"])
        
        self.vue.dessiner(self.model.ratio, noms, nbr, joueur_actif)
        
        self.vue.carte_en_jeu(self.game_state["discard"])
        
        joueur = next(p for p in self.game_state["players"] if p["name"] == self.player_name)
        
        main = joueur["cards"]
        
        etat = joueur.get("etat_main", ["disabled"] * len(main))
        etat_bouton = "normal" if self.player_name == self.game_state["current_player"] else "disabled"
        
        
        self.vue.ma_main(main, etat)
        self.vue.set_bouton_tour(etat_bouton)
        
        
    def recevoir_game_state(self, state: dict, player_name: str):
        self.game_state = state
        self.player_name = player_name
        self.mettre_a_jour()
    
    def demander_couleur(self):
        """Popup pour choisir la couleur après une carte Wild."""
        popup = Tk.Toplevel()
        popup.title("Choisir une couleur")
        popup.grab_set()
        for nom, code, bg in [("Rouge","r","red"), ("Bleu","b","blue"),
                               ("Vert","v","green"), ("Jaune","j","yellow")]:
            Tk.Button(popup, text=nom, bg=bg, width=10,
                      command=lambda c=code, p=popup: self._choisir_couleur(c, p)
                      ).pack(side=Tk.LEFT, padx=5, pady=10)

    def _choisir_couleur(self, code, popup):
        if self.send_action:
            self.send_action({"type": "CHOOSE_COLOR", "color": code})
        popup.destroy()


def affichage(game_state, player_name):
    """Affiche la vue en fonction du game_state et du joueur qui possède la vue."""
    root = Tk.Tk()
    root.title("Client")

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    controle = Controle(root)

    controle.recevoir_game_state(game_state, player_name)

    return root, controle


def _test():
    """Affiche la UI avec un faux GameState et un joueur précis."""
    root, controle = affichage(fake_state, "Lucas")
    root.mainloop()


if __name__ == "__main__":
    _test()

