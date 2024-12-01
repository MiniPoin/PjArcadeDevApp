import pygame
import random
import time
# pygame setup


class Rectangle():
    
    """Classe Rectangle contenant les attributs Rect de pygame, c'est à dire les hitboxs de nos élements.
    C'est la classe centrale permettant une meilleure gestion/clarté des tests et déplacements.
    Des points de vie et de score ont été rajoutés pour les briques avec des couleurs spécifiques.
    Un get et un set sont disponible et la perte de vie et changements de couleurs sont gérés automatiquement
    grâce aux fonctions du programme.
    
    Remarque importante: les coordonnées sont selon deux axes mais l'origine (0,0) est en haut à gauche.
    On se déplace donc de gauche à droite pour les abscisses mais de haut en bas pour les ordonnées."""
    
    def __init__(self,rect,vie):
        self.rect = rect
        self.vie = vie
        self.rgb = [0,0,0] # Couleur de la case
    
    def get_rect(self): # Retourne le Rect de l'instance
        return self.rect
    
    def set_pv(self,qtt): # Fixe la vie de la case
        self.vie = qtt
        return
        
    def perte(self): # Retire 1 point de vie
        self.vie -= 1
        return
    
    def couleur(self):
    # On définit des couleurs différentes selon le nombre de vies
        if self.vie == 1:
            self.rgb = [0, 0, 0]  # Noir pour 1 vie
        elif self.vie == 2:
            self.rgb = [49, 0, 53]  # Violet pour 2 vies
        elif self.vie == 3:
            self.rgb = [49, 114, 161]  # Bleu pour 3 vies
        return
        

    def get_pos(self):
        return [self.rect.x, self.rect.y] # Position du coin haut gauche
    
    def cote_pos(self): # Liste des 4 cotés
        return [self.rect.top,self.rect.bottom,self.rect.left,self.rect.right]
    
    def deplacement(self,x,y):
        return self.rect.move_ip(x,y)

def creation(screen_width, screen_height):
    l = []
    positions = set()  # Ensemble pour stocker les positions uniques
    nbm = 156  # 12*13 soit 13 lignes de 12 briques maximum
    nb = 0
    while nb < 100:
        for i in range(14):
            for j in range(6):
                a = random.randint(0, 1)
                if a == 1 and nb < nbm:  # nombre minimuim de briques
                    
                    """Générer deux positions : une pour la gauche (val) et une pour la droite (val2)
                    L'intéret ici est d'avoir des briques symétriques par esthétisme"""
                    
                    pos1 = (0 + j * (screen_width/12), 0 + i * (screen_height/36))
                    pos2 = (screen_width - (1 + j) * (screen_width/12), 0 + i * (screen_height/36))
                    
                    """Si la position n'est pas déjà dans l'ensemble pour éviter quelconque superposition,
                    on créer la brique"""
                    
                    if pos1 not in positions and nb < 100:
                        nb += 1
                        val = Rectangle(pygame.Rect(pos1[0], pos1[1], (screen_width/12), (screen_height/36)), 1) # Création du Rectangle avec les informations
                        
                        """ Création d'une vie aléatoire (max 3) de la brique. Voila les probabilitées:
                        2 vie: 1 chance sur 4
                        3 vie: 1 chance sur 7
                        1 vie: Les autres valeurs (Avant le changement la brique est créee noire par défaut"""
                        
                        vie_proba = random.randint(1, 100)
                        if vie_proba % 5 == 0:
                            val.set_pv(2)
                        elif vie_proba % 7 == 0:
                            val.set_pv(3)
                        val.couleur()
                        l.append(val)
                        positions.add(pos1)  # Ajouter la position à l'ensemble

                    if pos2 not in positions and nb < 100:
                        nb += 1
                        val2 = Rectangle(pygame.Rect(pos2[0], pos2[1], 160, 30), 1)
                        vie_proba = random.randint(1, 100)
                        if vie_proba % 2 == 0:
                            val2.set_pv(2)
                        elif vie_proba % 3 == 0:
                            val2.set_pv(3)
                        val2.couleur()
                        l.append(val2)
                        positions.add(pos2)  # Ajouter la position à l'ensemble
    return l


def bouge(r,dt,screen,screen_width):
    
    """ Regarde si une touche est pressée et selon si c'est la touche vers la gauche ou la droite déplace la plateforme
    grâce à la fonction de notre classe qui contient move_ip() dans déplacement()"""
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s] and r.cote_pos()[2] > 0:
        r.deplacement(-500* dt, 0)
    if keys[pygame.K_d] and r.cote_pos()[3] < screen_width:
        r.deplacement(500* dt, 0)
    return

def bouge_avant_partie(r,c,keys,screen,screen_width, screen_height,dt):
    
    """Permet de se déplacer avant la partie avec le cercle collé à la plateforme pour un meilleur positionnement"""

    if keys[pygame.K_s] and r.cote_pos()[2] > 0:
        r.deplacement(-500* dt, 0); c.deplacement(-500* dt, 0)
    if keys[pygame.K_d] and r.cote_pos()[3] < screen_width:
        r.deplacement(500* dt, 0); c.deplacement(500* dt, 0)
    return

def afficher_score(score, start_g,font,screen,screen_width, screen_height):
    # Créer le texte en fonction du score
    texte = font.render(f"Score: {score}", True, (255, 255, 255))  # Texte en blanc
    # Positionner le texte sur l'écran
    screen.blit(texte, (screen_width/50, screen_height - (screen_height/10)))
    
    if not start_g: # Texte du début de partie
        texte2 = font.render(f"Touche espace pour démarrer: ", True, (255, 255, 255))
        screen.blit(texte2, (screen_width/2-(screen_width/5), screen_height/2 - (screen_height/10)))  # Position du score (x=50, y=50)
    return

def bouge_c_dep(r,i,j,angle,dt):
    
    """ Génere un dx aléatoire puis selon i et j déplace la balle vers le haut/bas et gauche/droite
    Le dx permet une légère variation à peine détectable pour un peu de variation.
    Cette variation prend lieu uniquement en contact avec la plateforme et non les briques.
    on utilise angle pour faire la dissociation """
    
    dx = random.random()
    if j == 0: 
        r.deplacement(0, -500* dt)
    else:
        r.deplacement(0, 500* dt)
        
    if i == 0:
        if angle == True:
            r.deplacement((500* dt)-5*dx,-5*dx)
            angle = False
        else:
            r.deplacement(500* dt,0)
            
    else:
        if angle == True:
            r.deplacement((-500* dt)+5*dx,-5*dx)
            angle = False
        else:
            r.deplacement(-500* dt,0)
        
    return angle
    

def check_window_collision(circle, window_width, window_height,i,j):
    
    """ Vérifie une collision entre le cercle et les bords de la fenêtre.
    On effectue un leger deplacement puis on attend un peu pour éviter les bugs.
    En effet, le cercle peut trembler au bord de la fenêtre car pas le temps de se liberer de la condition"""
    
    if circle.cote_pos()[2] < 5:
        i = (i+1)%2 ; circle.deplacement(5,0)
    elif circle.cote_pos()[3] > window_width-5: # Marge de 5
        i = (i+1)%2 ; circle.deplacement(-5,0)
        
    elif circle.cote_pos()[0] < 5:
        j = (j+1)%2 ; circle.deplacement(0,-5)
    elif circle.cote_pos()[1] > window_height-5: # Marge de 5
        j = (j+1)%2 ; circle.deplacement(0,5)
    time.sleep(0.008)
    return i,j

def perdu(r,c):
    return (c.get_pos()[1]-80 >= r.cote_pos()[1]) # Si la balle passe en dessous

def touche_bri(l, cercle, i, j,score):
    
    """ Gère les interactions avec les briques. Prend les informations du cercle et de la liste avec les briques.
    Vérifie si y'a collisions puis dans ce cas calcule les distances de chaque côté et prend la plus petite
    (c'est à dire l'endroit ou le cercle rebondit).
    On change i et j, permettant de changer les directions.
    Ajoute 1000 au score à chaque contact et change la couleur de la brique si elle a plusieurs pv """
    
    for brique in l:
        x = brique.get_rect(); y = cercle.get_rect() # X = brique Y = cercle
        if x.colliderect(y):
            score += 1000 # Vérifie s'il y a collision
            # Calcul des distances entre les bords de la balle et ceux de la brique
            distance_top = x.top - y.bottom
            distance_bottom = y.top - x.bottom
            distance_right = y.left - x.right
            distance_left = x.left - y.right
            x = [abs(distance_bottom),abs(distance_top),abs(distance_right),abs(distance_left)]
            dist = x.index(min(x))
            if dist == 0:  # Collision par le bas
                j = (j+1) % 2
            elif dist == 1:  # Collision par le haut
                j = (j+1) % 2
            elif dist == 3:  # Collision par la droite
                i = (i+1) % 2
            else:  # Collision par la gauche
                i = (i+1) % 2
            if brique.vie == 1:
                l.remove(brique) # Supprimer la brique après collision et plus de vie et accorde une petite marge
            else:
                brique.perte()
                brique.couleur()
            time.sleep(0.01)
            break
            # On s'arrête après une collision pour éviter de multiples détections

    return i, j, score

def fin_jeu(font,screen,l, screen_width, screen_height):
    
    """Afficher un message pour redémarrer ou quitter selon si ESC est pressé ou pas et redémarre dans le cas échéant"""
    
    texte = font.render("Appuyez sur une touche pour rejouer ou sur ESC pour quitter", True, (255, 255, 255))
    texte2 = font.render("Vous avez gagné!! Appuyez sur une touche pour rejouer ou sur ESC pour quitter", True, (255, 255, 255))
    if len(l) == 0:
        screen.blit(texte2, (screen_width/2 - (screen_width/2.5), screen_height/2))
    else:
        screen.blit(texte, (screen_width/2 - (screen_width/2.5), screen_height/2))
    pygame.display.flip()
    
    en_attente = True
    while en_attente:
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                return False  # Quitter le jeu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False  # Quitter le jeu
                else:
                    return True  # Relancer le jeu


# Initialisation et création des rect (hitbox)

def lancement():
    pygame.init()
    clock = pygame.time.Clock()
    i = random.randint(0, 1)  # Vers gauche/droite
    j = 0  # Vers haut/bas (La balle va commencer toujours par le haut au début)
    pygame.font.init()  # Initialiser le module font de pygame
    font = pygame.font.Font(None, 74)
    
    # Initialisation des paramètres du jeu et de la fenêtre
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    running = True
    start_g = False  # Quand l'utilisateur appuie sur la touche droite ou gauche (démarre)
    crea = 0
    angle = False
    vie = 3
    score = 0
    # Chargement de l'image de la balle
    cercleR = pygame.image.load("cercle_rouge.png").convert_alpha()
    new_width = int(cercleR.get_width() * 0.1)
    new_height = int(cercleR.get_height() * 0.1)
    cercleR = pygame.transform.scale(cercleR, (new_width, new_height))
    # Initialisation et création des rect (hitbox)

    rect = pygame.Rect((int(screen_width / 2)-(screen_width / 19.2)), (int(screen_height / 2))+(screen_height / 2.7),(screen_width / 9.6),5)
    plateforme = Rectangle(rect,3)
    cercleR_rect = cercleR.get_rect(midbottom=(plateforme.get_pos()[0] + plateforme.rect.width // 2, plateforme.get_pos()[1]))
    cercle = Rectangle(cercleR_rect, 0)
    

    # Chargement de l'image de fond
    background_image = pygame.image.load('fontpyg.jpg')
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
    
    # Création des briques
    l = creation(screen_width, screen_height)
    pygame.draw.rect(screen, (0, 0, 0), plateforme.get_rect())  # Dessine la plateforme
    pygame.draw.rect(screen, (255, 0, 0), cercle.get_rect(), 2)
    while running and vie > 0:
        dt = clock.tick(60) / 1000  # Limite de 60 FPS
        screen.blit(background_image, (0, 0))  # Afficher le fond
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
        if running == True:
            if not start_g:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    start_g = True

                bouge_avant_partie(plateforme, cercle, keys,screen,screen_width, screen_height,dt)
                screen.blit(cercleR, cercle.get_rect())
                pygame.draw.rect(screen, (0, 0, 0), plateforme.get_rect())

            if crea == 0:
                l = creation(screen_width, screen_height)
                crea += 1
                
            for k in range(len(l)):
                pygame.draw.rect(screen, (0, 0, 0), l[k].get_rect())
                pygame.draw.rect(screen, (l[k].rgb[0], l[k].rgb[1], l[k].rgb[2]), l[k].get_rect().inflate(-4, -4))
            afficher_score(score, start_g,font,screen, screen_width, screen_height)

            if start_g:
                pygame.draw.rect(screen, (0, 0, 0), plateforme.get_rect())
                bouge(plateforme,dt,screen, screen_width)
                angle = bouge_c_dep(cercle, i, j, angle,dt)
                screen.blit(cercleR, cercle.get_rect())

                if plateforme.get_rect().colliderect(cercle.get_rect()):
                    if cercle.cote_pos()[1] >= plateforme.cote_pos()[0]:
                        j = (j + 1) % 2
                        cercle.rect.bottom = plateforme.rect.top - 5
                        angle = True

                i, j, score = touche_bri(l, cercle, i, j, score)
                afficher_score(score, start_g,font,screen,screen_width, screen_height)
                i, j = check_window_collision(cercle, screen_width, screen_height, i, j)

                if perdu(plateforme, cercle):
                    vie -= 1
                    start_g = False
                    cercle.rect = cercleR.get_rect(midbottom=(plateforme.get_pos()[0] + plateforme.rect.width // 2, plateforme.get_pos()[1]))


                if vie == 0:
                    running = fin_jeu(font,screen,l, screen_width, screen_height)
                    if running:
                        time.sleep(1)
                        vie = 3
                        score = 0
                        start_g = False
                        cercle.rect = cercleR.get_rect(center=(plateforme.get_pos()[0] + plateforme.rect.width // 2, plateforme.get_pos()[1] - 27))
                        crea = 0
                    else:
                        break

            pygame.display.flip()
pygame.quit()

lancement()
