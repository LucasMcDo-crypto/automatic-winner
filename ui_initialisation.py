"""Programme d'interface utilisateur pour se connecter et lancer une partie

Fait par Lucas"""
import tkinter as tk
import threading
import server
from fake_state import fake_state

start_game_state = fake_state


class Vue1(tk.Frame):
    """Menu principal"""

    def __init__(self, master, controle):
        super().__init__(master)
        self.controle = controle

        self.titre = tk.Label(self, text="UNO")
        self.bouton_Host = tk.Button(self, text="Host", command=self.Get_to_Vue_Host)
        self.bouton_Client = tk.Button(self, text="Client", command=self.Get_to_Vue_Client)
        self.bouton_quitter = tk.Button(self, text="Quitter", command=self.controle.quitter)

        self.titre.grid(row=0, column=1)
        self.bouton_Host.grid(row=1, column=1)
        self.bouton_Client.grid(row=2, column=1)
        self.bouton_quitter.grid(row=3, column=1)

    def Get_to_Vue_Host(self):
        self.controle.show_frame(Vue_Host)

        self.controle.host = server.Host(callback=self.controle.afficher)
        self.controle.host.game_state = start_game_state

        thread = threading.Thread(target=self.controle.host.start, daemon=True)
        thread.start()

    def Get_to_Vue_Client(self):
        self.controle.show_frame(Vue_Client)

        self.controle.client = server.Client()

        # Connexion au serveur dans un thread (sans input)
        thread = threading.Thread(target=self.controle.client._connect, daemon=True)
        thread.start()


class Vue_Host(tk.Frame):
    """Vue Host"""

    def __init__(self, master, controle):
        super().__init__(master)
        self.controle = controle

        self.titre = tk.Label(self, text="Host")
        self.texte = tk.Label(self, text="")
        self.bouton_retour = tk.Button(self, text="Retour", command=lambda: self.controle.retour_host())
        self.bouton_quitter = tk.Button(self, text="Quitter", command=self.controle.quitter)

        self.titre.grid(row=0, column=1)
        self.texte.grid(row=1, columnspan=2)
        self.bouton_retour.grid(row=2, column=0)
        self.bouton_quitter.grid(row=2, column=1)

    def afficher(self, message):
        self.texte.config(text=message)


class Vue_Client(tk.Frame):
    """Vue Client"""

    def __init__(self, master, controle):
        super().__init__(master)
        self.controle = controle

        self.titre = tk.Label(self, text="Client")
        self.entree = tk.Entry(self)
        self.texte = tk.Label(self, text="")

        # Bouton pour envoyer le pseudo
        self.bouton_pseudo = tk.Button(self, text="Valider pseudo", command=self.envoyer_pseudo)

        self.bouton_retour = tk.Button(self, text="Retour", command=lambda: self.controle.retour_client())
        self.bouton_quitter = tk.Button(self, text="Quitter", command=self.controle.quitter)

        self.titre.grid(row=0, column=1)
        self.entree.grid(row=1, column=1)
        self.bouton_pseudo.grid(row=2, column=1)
        self.texte.grid(row=3, columnspan=2)
        self.bouton_retour.grid(row=4, column=0)
        self.bouton_quitter.grid(row=4, column=1)

    def envoyer_pseudo(self):
        pseudo = self.entree.get()

        if not pseudo:
            self.afficher("Veuillez entrer un pseudo")
            return

        if not self.controle.client:
            self.afficher("Client non connecté")
            return

        try:
            self.controle.client.send_nickname(pseudo)
            self.afficher(f"Connecté en tant que {pseudo}")
        except Exception:
            self.afficher("Connexion au serveur en cours...")

    def afficher(self, message):
        self.texte.config(text=message)


class Controle(tk.Tk):
    """Contrôle du programme"""

    def __init__(self):
        super().__init__()

        self.title("UNO")
        self.host = None
        self.client = None

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.frames = {}

        for F in (Vue1, Vue_Host, Vue_Client):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Vue1)

        self.bind('<Control-q>', lambda e: self.quitter())

    def show_frame(self, vue):
        """Changer de vue"""
        frame = self.frames[vue]
        frame.tkraise()
    
    def retour_host(self):
        """Déconnecte le host et retourne à la vue1."""
        if self.host:
            self.host.stop()
            self.host = None
        self.show_frame(Vue1)
    
    def retour_client(self):
        """Déconnecte le client et retourne à la vue1."""
        if self.client:
            self.client.stop()
            self.client = None
        self.show_frame(Vue1)
    
    def afficher(self, message):
        """Affichage thread-safe pour le host"""
        self.after(0, lambda: self.frames[Vue_Host].afficher(message))

    def quitter(self):
        """Quitter"""
        self.destroy()


if __name__ == "__main__":
    Controle().mainloop()
