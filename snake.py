from fltk import *
from time import sleep
from random import randint
import sys

# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases

ACCUEIL = True

def case_vers_pixel(case):
    """
	Fonction recevant les coordonnées d'une case du plateau sous la 
	forme d'un couple d'entiers (ligne, colonne) et renvoyant les 
	coordonnées du pixel se trouvant au centre de cette case. Ce calcul 
	prend en compte la taille de chaque case, donnée par la variable 
	globale taille_case.
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pommes):
    """
    Fonction qui permet l'affiche des pommes sur le plateau de jeu.
    """
    for pomme in pommes:
        x, y = case_vers_pixel(pomme)
        cercle(x, y, taille_case/2,
               couleur='darkred', remplissage='red')
        rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
                  couleur='darkgreen', remplissage='darkgreen')

def ajouter_pommes():
    """
    Fonction qui ajoute des pommes de manière aléatoire sur le plateau de jeu.
    """
    while True:
        ajout = (randint(0, 39), randint(0,29)) # Permet d'ajouter des pommmes
        # de manières aléatoire sur le plateau de jeu
        if ajout not in serpent and ajout not in pommes:
            pommes.append(ajout)
            return

def affiche_obstacles(obstacles):
    """
    Fonction qui permet l'affichage du des obstacles sur le
    plateau de jeu.
    """
    for obstacle in obstacles:
        x, y = case_vers_pixel(obstacle)
        rectangle(x-5, y-taille_case*.9, x+5, y- taille_case*.18,
                 couleur='blue', remplissage='blue')

def ajouter_obstacles():
    """
    Fonction qui ajoute de manière aléatoire des obstacles rectangulaires
    sur le plateau de jeu.
    """
    while True:
        ajoute = (randint(0, 38), randint(0,28))
        #i,j Coordonnées de la tête du serpent
        i = serpent[0][0]
        j = serpent[0][1]
        #Définition d'une zone de protection de 3 cases autour de la tête du serpent
        #Cela évite le surgissement d'obstacles rendant le jeux injouable
        zone_protection = [(i-3,j-3),(i+3,j+3)]
        zone2 = [(500,0),(600,5)]
        #Si l'obstacle n'est pas dans la zone de protection et pas dans les obstacles existants,
        #Alors on l'ajoute sinon on boucle pour en choisir un autre
        if not(zone_protection[0][0] <= ajoute[0] and ajoute[0] <= zone_protection[1][0] and \
           zone_protection[0][1] <= ajoute[1] and ajoute[1] <= zone_protection[1][1]) and \
           ajoute not in obstacles:
            if not(zone2[0][0] <= ajoute[0] and ajoute[0] <= zone2[1][0] and \
               zone2[0][1] <= ajoute[1] and ajoute[1] <= zone2[1][1]):
                obstacles.append(ajoute)
                return
        
def affiche_serpent(serpent):
    """
    Fonction qui prend en compte la taille du serpent à renvoie une nouvelle taille
    au serpent lorsque celui-ci mange une pomme.
    """
    for boule in range(len(serpent)):
        x, y = case_vers_pixel(serpent[boule])
        cercle(x, y, taille_case/2 + 1,
                couleur='darkgreen', remplissage='green')


def deplacement_serpent(serpent_lst, direction):
    """
    Fonction qui prend en compte une liste serpent et une direction
    et renvoie une coordonnée en fonction de la direction choisie.
    D'autre part, cette fonction est bassé sur le modèle de Pacman.
    Enfin, elle interagit avec la focntion affiche_pommes() et affiche_obstacles().
    """
    x_tete, y_tete = serpent_lst[-1]
    abscisse = x_tete + direction[0]
    ordonnee = y_tete + direction[1]
    # utilisation du mode Pacman pour le déplacement du serpent
    if 0 > ordonnee:
        ordonnee = 30
    elif ordonnee > 29:
        ordonnee = 0
    if 0 > abscisse:
        abscisse = 40
    elif abscisse > 39:
        abscisse = 0
    
    if (abscisse, ordonnee) in serpent and len(serpent) > 1: # Losque le serpent touche sa queue le jeu s'arrête. 
        return False
    elif (abscisse, ordonnee) in obstacles: # Lorsque le serpent touche un obstacle le jeu s'arrête.
        return False
    elif (abscisse,ordonnee) in pommes: # lorsque le serpent mange une pomme le serpent augmente sa taille.
        # De plus, une nouvelle pomme est ajouter aléatoirement sur le plateau de jeu.
        pommes.remove((abscisse,ordonnee))
        ajouter_pommes()
    else:
        serpent.pop(0)
    serpent.append((abscisse, ordonnee))
    return True


def change_direction(direction, touche):
    """
    Fonction qui prend en compte les touches directionnelles
    pour controler les  directions du serpent
    sur sur l'espace de jeu dédier au snake
    """
    if touche == 'Up':
        return (0, -1)
    elif touche == 'Down':
        return (0, 1)
    elif touche == 'Left':
        return (-1, 0)  
    elif touche == 'Right':
        return (1, 0)
    else:
        return direction


# programme principal
if __name__ == "__main__":
    while ACCUEIL == True:
        # initialisation du jeu
        # Variables et valeurs prises en compte par le programme pour jouer au snake.
        framerate = 10    # taux de rafraîchissement du jeu en images/s
        direction = (0, 0)  # direction initiale du serpent
        pommes = [(30,10)] # liste des coordonnées des cases contenant des pommes
        obstacles = []# liste des coordonnées des cases contenant des obstacles
        serpent = [(5, 20)] # liste des coordonnées de cases adjacentes décrivant le serpent
        cree_fenetre(taille_case * largeur_plateau,
                         taille_case * hauteur_plateau)
        efface_tout()
        rectangle(0, 0, 600, 500, couleur='grey', remplissage='grey') #Fond d'écran de la page d'accueil
 
        # boucle principale
        bouton_start = [(250,250),(350,300)] # Création d'un bouton start pour pouvoir lancer le jeu.
        rectangle(bouton_start[0][0], bouton_start[0][1], bouton_start[1][0], bouton_start[1][1],\
                  couleur='white', remplissage='white', epaisseur=1, tag='accueil')
        texte(280, 260, f"Start", taille =15, couleur = 'black')
        texte(170, 170, f"Welcome to the game 'Snake'\n   Press start button to play", taille = 15, couleur = 'white') # Texte descriptif de début de partie
        jouer = False
        while True: # Boucle while pour savoir si l'utilisateur à cliquer sur le bouton_start pour commencer la partie.
            appuyer = attend_clic_gauche()
            if bouton_start[0][0] <= appuyer[0] and appuyer[0] <= bouton_start[1][0] and \
               bouton_start[0][1] <= appuyer[1] and appuyer[1] <= bouton_start[1][1]:
                efface_tout()
                jouer = True
                break
        cpt = 1
        while jouer :
            # affichage des objets
            efface_tout()
            affiche_pommes(pommes)
            affiche_obstacles(obstacles)
            affiche_serpent(serpent)
            longueur_before = len(serpent)
            texte(500, 5, f"score: {len(serpent)-1}", taille = 15, couleur = 'black', tag = "score") # Ceci permet d'obtenir un score qui est affiche en haut à droite.
            if (cpt % 20) == 0:
                ajouter_obstacles()
            mise_a_jour()
                
            # gestion des événements
            ev = donne_ev()
            ty = type_ev(ev)
            if ty == 'Quitte':
                jouer = False
            elif ty == 'Touche':
                direction = change_direction(direction, touche(ev))
            if not deplacement_serpent(serpent, direction):
                break
            cpt += 1
            #Accélération de 20% à partir d'une longueur 5, à chaque fois que l'on mange une pomme
            if len(serpent) > longueur_before and len(serpent)>= 5:
                framerate = framerate * 1.2
                texte(250, 200, f"BOOST !", taille = 30, couleur = 'red', tag = "boost")
                mise_a_jour()
            sleep(1/framerate)
        efface_tout()
        rectangle(0 ,0 , 600, 500, couleur = 'grey', remplissage='grey') # Fond d'écran de la page de fin de Jeu
        texte(140, 125, f"          Game Over !\n             Score: {len(serpent)-1}\nDo you want to play again ?", taille = 20, couleur ='white')
        bouton_yes = [(130,230),(250,300)] # Création du bouton yes , pour recommmencer une nouvelle partie
        bouton_no = [(330,230),(450,300)] # Création du bouton no , pour finir définitive la partie et sortir du programme
        # Paramètre du bouton yes
        rectangle(bouton_yes[0][0], bouton_yes[0][1], bouton_yes[1][0], bouton_yes[1][1],\
                  couleur='green', remplissage='green', epaisseur = 1, tag='Yes')
        texte(170, 250, f"Yes", taille = 15, couleur = 'white')
        # Paramètre du bouton no
        rectangle(bouton_no[0][0], bouton_no[0][1], bouton_no[1][0], bouton_no[1][1],\
                  couleur='red', remplissage='red', epaisseur = 1 , tag='No')
        texte(380, 250, f"No", taille = 15, couleur = 'white')
        while True:
            appuyer = attend_clic_gauche()
            if bouton_yes[0][0] <= appuyer[0] and appuyer[0] <= bouton_yes[1][0] and \
               bouton_yes[0][1] <= appuyer[1] and appuyer[1] <= bouton_yes[1][1]:
                efface_tout()
                ACCUEIL = True
                break
            if bouton_no[0][0] <= appuyer[0] and appuyer[0] <= bouton_no[1][0] and \
               bouton_no[0][1] <= appuyer[1] and appuyer[1] <= bouton_no[1][1]:
                efface_tout()
                ACCUEIL = False
                break
        mise_a_jour()
        # fermeture de la fenetre
        ferme_fenetre()
    #sortie du programme
    sys.exit()
