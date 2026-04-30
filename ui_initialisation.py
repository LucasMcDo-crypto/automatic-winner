"""Programme d'interface utilisateur pour se connecter et lancer une partie

Fait par Lucas"""
import tkinter as tk
import server

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

    def Get_to_Vue_Client(self):
        self.controle.show_frame(Vue_Client)


class Vue_Host(tk.Frame):
    """Vue Host"""

    def __init__(self, master, controle):
        super().__init__(master)
        self.controle = controle

        self.titre = tk.Label(self, text="Host")
        self.texte = tk.Label(self, text="")
        self.bouton_retour = tk.Button(self, text="Retour", command=lambda: self.controle.show_frame(Vue1))
        self.bouton_quitter = tk.Button(self, text="Quitter", command=self.controle.quitter)

        self.titre.grid(row=0, column=1)
        self.texte.grid(row=1, columnspan=2)
        self.bouton_retour.grid(row=2, column=0)
        self.bouton_quitter.grid(row=2, column=1)


class Vue_Client(tk.Frame):
    """Vue Client"""

    def __init__(self, master, controle):
        super().__init__(master)
        self.controle = controle

        self.titre = tk.Label(self, text="Client")
        self.entree = tk.Entry(self)
        self.texte = tk.Label(self, text="")
        self.bouton_retour = tk.Button(self, text="Retour", command=lambda: self.controle.show_frame(Vue1))
        self.bouton_quitter = tk.Button(self, text="Quitter", command=self.controle.quitter)

        self.titre.grid(row=0, column=1)
        self.entree.grid(row=1, column=1)
        self.texte.grid(row=2, columnspan=2)
        self.bouton_retour.grid(row=3, column=0)
        self.bouton_quitter.grid(row=3, column=1)


class Controle(tk.Tk):
    """Contrôle du programme"""

    def __init__(self):
        super().__init__()

        self.title("UNO")

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

    def quitter(self):
        """Quitter"""
        self.destroy()

def test():
    server.user = input("host or client ? \n")

    if server.user.lower() not in ("host", "client"):
        raise Exception("Misinput, try again")
    
    match server.user.lower():
        case "host":
            server.host = Host()
            server.host.game_state = fake_state
            server.host.start()
            
        case "client":
            server.client = Client()
            server.client.start()

if __name__ == "__main__":
    Controle().mainloop()
