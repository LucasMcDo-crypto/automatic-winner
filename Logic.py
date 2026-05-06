"""Règles du jeu UNO

Première version: 04.02.2026
Dernière version: 25.04.2026
Auteur: Alexis
"""

from __future__ import annotations
from enum import Enum
from random import sample


CARTES_PAR_JOUEUR = 7
NOMBRE_CARTES_SPECIALES = 2
MULTIPLICATEUR_DECK = 1


def _donnee(action: str, joueur: str, objet: str) -> dict:
    """Retourner les données d'une action."""
    return {"action": action,
            "joueur": joueur,
            "objet": objet}


class Couleur(str, Enum):
    """Couleur UNO"""
    ROUGE = 'r'
    BLEU = 'b'
    VERT = 'v'
    JAUNE = 'j'
    SPECIAL = ''
    
    @classmethod
    def obtenir_normal(cls) -> tuple:
        """Obtenir les couleurs. La couleur spéciale n'est pas prise en compte."""
        valeurs = ()
        for member in cls.__members__:
            if cls.__members__[member].name != 'SPECIAL':
                valeurs += (cls.__members__[member],)
        return valeurs
    
    @classmethod
    def obtenir_special(cls) -> tuple:
        """Obtenir la couleur spéciale."""
        return (cls.SPECIAL,)
    
    @classmethod
    def invalide_premier(cls) -> tuple:
        """Obtenir la couleur invalide pour être la première carte de défausse."""
        return cls.obtenir_special()
    
    @classmethod
    def obtenir(cls, couleur: str) -> Couleur:
        """Obtenir la couleur à partir de sa valeur str."""
        for member in cls.__members__:
            if cls.__members__[member].value == couleur.lower():
                return cls.__members__[member]
        raise ValueError("Couleur invalide")


class Chiffre(str, Enum):
    """Chiffre UNO"""
    ZERO = '0'
    UN = '1'
    DEUX = '2'
    TROIS = '3'
    QUATRE = '4'
    CINQ = '5'
    SIX = '6'
    SEPT = '7'
    HUIT = '8'
    NEUF = '9'
    PLUS_DEUX = '+2'
    PLUS_QUATRE = '+4'
    CHANGE_SENS = '__'
    PASSE = 'o'
    SPECIAL = 'S'
    
    @classmethod
    def obtenir_normal(cls) -> tuple:
        """Obtenir les chiffres. Les chiffres spéciaux ne sont pas pris en compte."""
        valeurs = ()
        for member in cls.__members__:
            if cls.__members__[member].name not in ('SPECIAL', 'PLUS_QUATRE'):
                valeurs += (cls.__members__[member],)
        return valeurs
    
    @classmethod
    def obtenir_special(cls) -> tuple:
        """Obtenir les chiffres spéciaux."""
        return (cls.SPECIAL, cls.PLUS_QUATRE)
    
    @classmethod
    def invalide_premier(cls) -> tuple:
        """Obtenir les chiffres invalides pour être la première carte de défausse."""
        return (cls.obtenir_special(), cls.PLUS_DEUX, cls.CHANGE_SENS, cls.PASSE)
    
    @classmethod
    def obtenir(cls, chiffre: str) -> Chiffre:
        """Obtenir le chiffre à partir de sa valeur str."""
        for member in cls.__members__:
            if cls.__members__[member].value == chiffre:
                return cls.__members__[member]
        raise ValueError("Chiffre invalide")
 

_COMBINAISONS_POSSIBLES = {Couleur.obtenir_normal(): Chiffre.obtenir_normal(),
                           Couleur.obtenir_special(): Chiffre.obtenir_special()}


def _verifier_combinaison(couleur: str, chiffre: str) -> bool:
    """Vérifier si la combinaison couleur/chiffre est possible."""
    for couleurs in _COMBINAISONS_POSSIBLES:
        if couleur in couleurs:
            if chiffre in _COMBINAISONS_POSSIBLES[couleurs]:
                return True
    return False


class Carte():
    """Carte UNO"""
    couleur: Couleur
    chiffre: Chiffre
    
    def __init__(self, couleur: Couleur, chiffre: Chiffre):
        """Créer une carte UNO avec une COULEUR et un CHIFFRE."""
        if couleur not in (Couleur.obtenir_special() + Couleur.obtenir_normal()):
            raise ValueError("Couleur invalide")
        if chiffre not in (Chiffre.obtenir_special() + Chiffre.obtenir_normal()):
            raise ValueError("Chiffre invalide")
        if not _verifier_combinaison(couleur, chiffre):
            raise ValueError("La couleur et le chiffre ne peuvent pas être combinées.")
        self.couleur = couleur
        self.chiffre = chiffre
    
    def __repr__(self):
        return "Carte(" + str(self.couleur) + ", " + str(self.chiffre) + ")"
        
    def __str__(self):
        return str(self.couleur.value) + str(self.chiffre.value)
    
    def __eq__(self, other):
        if self.couleur == other.couleur and self.chiffre == other.chiffre:
            return True
        return False
    
    def compatible(self, other: Carte) -> bool:
        """Vérifier la compatibilité couleur/chiffre entre 2 cartes."""
        if self.couleur in (other.couleur, *Couleur.obtenir_special()) or self.chiffre in (other.chiffre, *Chiffre.obtenir_special()):
            return True
        return False
    
    def consequence(self) -> dict:
        """Obtenir la conséquence d'une carte.
        Retourne un dictionnaire avec les données des conséquences.
        """
        choix = False
        pioche = 0
        change_sens = False
        passe = 0
        if self.couleur == Couleur.SPECIAL:
            choix = True
        if self.chiffre in (Chiffre.PLUS_DEUX, Chiffre.PLUS_QUATRE):
            pioche = int(self.chiffre)
        if self.chiffre == Chiffre.CHANGE_SENS:
            change_sens = True
        if self.chiffre == Chiffre.PASSE:
            passe = 1
        return {"choix": choix,
                "pioche": pioche,
                "change_sens": change_sens,
                "passe": passe} 

class Deck():
    """Deck de cartes UNO"""
    cartes: list[Carte]
    
    def __init__(self, speciales: int = NOMBRE_CARTES_SPECIALES, multiplicateur: int = MULTIPLICATEUR_DECK):
        """Créer un deck de cartes UNO.
        SPECIALES est le nombre de cartes spéciales.
        MULTIPLICATEUR multiplie chaque carte du deck.
        """
        c = []
        for couleur in Couleur.obtenir_normal():
            for chiffre in Chiffre.obtenir_normal():
                c.append(Carte(couleur, chiffre))
        for _ in range(speciales):
            c.append(Carte(Couleur.obtenir_special()[0], Chiffre.obtenir_special()[0]))
            c.append(Carte(Couleur.obtenir_special()[0], Chiffre.obtenir_special()[1]))
        c = sample(c, counts=list(multiplicateur for _ in range(len(c))), k=len(c))
        self.cartes = c
    
    def __repr__(self):
        return str(list(self.cartes))
    
    def __str__(self):
        cartes2 = []
        for c in self.cartes:
            cartes2.append(str(c))
        return str(list(cartes2))
    
    def melanger(self) -> None:
        """Mélanger les cartes du deck."""
        c = list(self.cartes)
        c = sample(c, counts=list(1 for _ in range(len(c))), k=len(c))
        self.cartes = c
    
    def premiere_carte_valide(self) -> None:
        """Remélanger le deck tant que la première carte est invalide pour débuter la partie."""
        c = list(self.cartes)
        while c[0].couleur in Couleur.invalide_premier() or c[0].chiffre in Chiffre.invalide_premier():
            self.melanger()
            
    def piocher(self) -> Carte|None:
        """Piocher la première carte du deck.
        Retourne None si le deck est vide.
        """
        if len(self.cartes) > 0:
            c = self.cartes[0]
            self.cartes.remove(c)
            return c
        else:
            return None


class Joueur():
    """Joueur UNO"""
    nom: str
    partie: Partie|None
    main: list[Carte]
    choix: bool
    pioche: int
    
    def __init__(self, nom: str):
        """Créer un joueur UNO avec un NOM."""
        self.nom = nom
        self.partie = None
        self.main = []
        self.choix = False
        self.pioche = 0
    
    def __str__(self):
        if self.partie is not None:
            texte = []
            for carte in self.main:
                texte.append(str(carte))
            return self.nom + ": " + str(texte) + "\nchoix: " + str(self.choix) + "\npioche: " + str(self.pioche)
        return self.nom
    
    def etat(self) -> dict:
        """Obtenir l'état du joueur."""
        if self.partie is not None:
            return {"nom": self.nom,
            "main": self.obtenir_main(),
            "choix": self.choix,
            "pioche": self.pioche}
        return {"nom": self.nom}
    
    def obtenir_main(self) -> list[str]:
        """Obtenir la liste des cartes (str) du joueur."""
        cartes = []
        if self.partie is not None:
            for carte in self.main:
                cartes.append(str(carte))
        return cartes
    
    def cartes_possibles(self) -> list[str]:
        """Obtenir la liste des cartes (str) possibles à jouer."""
        cartes = []
        if self.partie is not None:
            for carte in self.main:
                if carte.compatible(self.partie.carte_defausse):
                    cartes.append(str(carte))
        return cartes
    
    def piocher(self) -> dict|None:
        """Piocher une carte du deck de la partie et l'ajouter à la main du joueur.
        Retourne les données de l'action. Retourne None si le joueur n'est pas dans
        une partie ou si le joueur n'est pas le joueur en jeu.
        Met à jour automatiquement la partie.
        Si le deck est vide, la main du joueur n'est pas changée mais la partie est mise à jour.
        """
        if self.partie is not None:
            carte = self.partie.deck.piocher()
            if carte is not None:
                self.main.append(carte)
            if self.pioche == 0:
                self.partie.mettre_a_jour()
            return _donnee("piocher", self.nom, str(carte))
        return None
    
    def piocher_debut(self) -> tuple|None:
        """Piocher des cartes si la carte posée précédemment a un chiffre +2 ou +4.
        Cette fonction doit être appelée au début du tour du joueur.
        Retourne les données de l'action. Retourne None si le joueur n'est pas dans
        une partie ou si le joueur n'est pas le joueur en jeu.
        """
        if self.partie is not None and self == self.partie.obtenir_prochain():
            d = ()
            for _ in range(self.pioche):
                d += (self.piocher(),)
                self.pioche -= 1
            return d
        return None
                    
    def poser(self, carte: str|Carte) -> dict|None:
        """Poser une carte sur la défausse.
        CARTE peut être la valeur str de la carte à jouer ou une instance de la classe Carte.
        Retourne les données de l'action. Retourne None si le joueur n'est pas dans
        une partie ou si le joueur n'est pas le joueur en jeu.
        Met à jour automatiquement la partie.
        """
        if type(carte) == str:
            c = Carte(Couleur.obtenir(carte[0]), Chiffre.obtenir(carte[1:]))
        elif type(carte) == Carte:
            c = carte
        if self.partie is not None and self == self.partie.obtenir_prochain():
            if c not in self.main:
                raise ValueError("Le joueur ne possède pas cette carte.")
            if not c.compatible(self.partie.carte_defausse):
                raise ValueError("Cette carte n'est pas compatbile avec la carte de défausse.")
            self.main.remove(c)   
            self._mettre_a_jour(c)
            return _donnee("poser", self.nom, str(c))
        return None
    
    def choisir(self, couleur: Couleur|str) -> dict|None:
        """Choisir la couleur de la partie si le joueur a le droit.
        COULEUR peut être la valeur str de la couleur ou une instance de la classe Couleur.
        Retourne les données de l'action.
        Retourne None si le joueur n'est pas dans une partie ou si le joueur n'a pas le droit.
        """
        if self.partie is not None and self.choix:
            if type(couleur) != Couleur:
                c = Couleur.obtenir(couleur)
            else:
                c = couleur
            if c in Couleur.obtenir_normal():
                self.partie.carte_defausse.couleur = c
                self.choix = False
            else:
                raise ValueError("Couleur invalide")
            return _donnee("choisir", self.nom, str(c))
        return None
    
    def _mettre_a_jour(self, carte: Carte) -> None:
        if self.partie is not None and self == self.partie.obtenir_prochain():
            consequence = carte.consequence()
            self.choix = consequence["choix"]
            if len(self.main) == 0:
                self.partie.vainqueur = self
            self.partie.mettre_a_jour(carte)
        
        
class Robot(Joueur):
    """Robot UNO"""
    def jouer(self) -> dict|None:
        """Poser une carte si possible, sinon piocher une carte.
        Retourne les données de l'action. Retourne None si le joueur n'est pas dans
        une partie ou si le joueur n'est pas le joueur en jeu.
        """
        if self.partie is not None and self == self.partie.obtenir_prochain():
            carte_jouer = None
            for carte in self.main:
                if carte.compatible(self.partie.carte_defausse):
                    carte_jouer = carte
            if carte_jouer is not None:
                self.main.remove(carte_jouer)
                self._mettre_a_jour(carte_jouer)
                if self.choix:
                    self.choisir(self.main[0].couleur)
                return _donnee("poser", self.nom, str(carte_jouer))
            else:
                return self.piocher()
        return None
    
    
class Partie():
    """Partie UNO"""
    vainqueur: Joueur|None
    deck: Deck
    joueurs: list[Joueur]
    carte_defausse: Carte
    
    def __init__(self, joueurs: tuple[str], robots: tuple[str]|None = None, cartes_par_joueur: int = CARTES_PAR_JOUEUR):
        """Créer une partie.
        JOUEURS est les noms des joueurs.
        ROBOTS est le nom des robots.
        CARTES_PAR_JOUEURS est le nombre de cartes par joueur.
        """
        self.vainqueur = None
        self.deck = Deck()
        self.joueurs = []
        self._sens_horaire = True
        
        for j in joueurs:
            joueur = Joueur(j)
            joueur.partie = self
            joueur.main = list((self.deck.piocher() for _ in range(cartes_par_joueur)))
            self.joueurs.append(joueur)
        
        if robots is not None:
            for r in robots:
                joueur = Robot(r)
                joueur.partie = self
                joueur.main = list((self.deck.piocher() for _ in range(cartes_par_joueur)))
                self.joueurs.append(joueur)
       
        self._joueur_jeu = self.joueurs[0]
        self._prochain_joueur = self._joueur_jeu
        self.deck.premiere_carte_valide()
        
        c = self.deck.piocher()
        if c is None:
            raise Exception("Le deck est vide.")
        self.carte_defausse = c
    
    def __str__(self):
        texte = ""
        for joueur in self.joueurs:
            texte += str(joueur.nom) + ": nombre de cartes = " + str(len(joueur.main)) + "\n"
        return str(texte) + "joueur en jeu: " + str(self._joueur_jeu.nom) + "\ncarte défausse: " + str(self.carte_defausse) + "\nsens horaire: " + str(self._sens_horaire)
    
    def joueurs_etats(self) -> list[dict]:
        """Obtenir les états des joueurs de la partie."""
        etats = []
        for joueur in self.joueurs:
            etats.append({"nom": joueur.nom, "nombre de cartes": len(joueur.main)})
        return etats
    
    def etat(self) -> dict:
        """Obtenir l'état de la partie."""
        return {"vainqueur": self.vainqueur,
        "carte de défausse": str(self.carte_defausse),
        "joueur en jeu": self._joueur_jeu.nom,
        "sens horaire": self._sens_horaire,
        "joueurs": self.joueurs_etats()}
    
    def mettre_a_jour(self, carte: Carte|None = None) -> dict:
        """Mettre à jour la partie en fonction de la carte posée afin de déterminer le prochain joueur.
        Retourne le nouvel état de la partie.
        Cette fonction est appelée lorsqu'un joueur pioche ou pose une carte.
        """
        pioche = 0
        change_sens = False
        passe = 0
        if carte is not None:
            consequence = carte.consequence()
            pioche = consequence["pioche"]
            change_sens = consequence["change_sens"]
            passe = consequence["passe"]
            self.carte_defausse = carte
        if change_sens:
            self._sens_horaire = not self._sens_horaire
        if self._sens_horaire:
            i = (self.joueurs.index(self._joueur_jeu) + 1 + passe) % len(self.joueurs)
        else:
            i = (self.joueurs.index(self._joueur_jeu) - 1 - passe) % len(self.joueurs)
        joueur = self.joueurs[i]
        if len(joueur.main) == 0:
            for _ in range(len(self.joueurs)):
                i += 1
                joueur = self.joueurs[i]
                if len(joueur.main) != 0:
                    break
        joueur.pioche += pioche
        self._prochain_joueur = joueur
        return self.etat()
            
    def obtenir_prochain(self) -> Joueur:
        """Obtenir le prochain joueur qui doit jouer."""
        self._joueur_jeu = self._prochain_joueur
        return self._joueur_jeu
            
        
def _creer_partie():
    return Partie(("joueur1",), robots=("robot1",))


def _jouer_partie(partie):
    while partie.vainqueur is None:
        joueur = partie.obtenir_prochain() #obtenir le prochain joueur qui doit jouer
        print(joueur.piocher_debut()) #piocher si la carte jouée précédemment était par exemple +2
        print(partie.etat())
        print(joueur.etat())
        print(joueur.cartes_possibles())
        if type(joueur) == Robot:
            print(joueur.jouer()) #le robot joue automatiquement
        else:
            carte = input("carte à jouer: ")
            if carte in joueur.cartes_possibles():
                print(joueur.poser(carte))
            else:
                print(joueur.piocher()) #piocher si aucune carte ne peut être posée
            if joueur.choix: #si le joueur peut choisir une couleur
                couleur = input("Couleur: ")
                print(joueur.choisir(couleur)) #le joueur choisit la couleur si il a le droit
        print()
    print("Vainqueur: " + str(partie.vainqueur.nom))


if __name__ == "__main__":
    exemple = _creer_partie()
    _jouer_partie(exemple)

