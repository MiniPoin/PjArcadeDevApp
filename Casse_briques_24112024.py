import pygame
import random

# pygame setup
pygame.init()
pygame.font.init()  # Initialiser le module font de pygame
font = pygame.font.Font(None, 74)
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
start_g = False # quand l'utilisateur appuie sur la touche droite ou gauche (demarre)
crea = 0
angle = False

#Definit la direction de la balle
i = random.randint(0,1)
j = 0 # la balle va commence toujours par le haut

class Rectangle():
    """Classe rectangle contenant les attributs Rect de pygame
    Des points de vie et de score ont été rajoutés"""
    def __init__(self,rect,vie):
        self.rect = rect
        self.vie = vie
        self.pt = 1000
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
            self.rgb = [255, 165, 0]  # Orange pour 2 vies
        elif self.vie == 3:
            self.rgb = [255, 255, 0]  # Jaune pour 3 vies
        return
        
    
    def get_pos(self):
        return [self.rect.x, self.rect.y] # Position coin haut gauche
    
    def cote_pos(self): # Liste des 4 cotés
        return [self.rect.top,self.rect.bottom,self.rect.left,self.rect.right]
    
    def deplacement(self,x,y):
        return self.rect.move_ip(x,y)

#Définition de la plateforme
rect = pygame.Rect((int(screen.get_width() / 2)-100), (int(screen.get_height() / 2))+300,200,5)
plateforme = Rectangle(rect,3)
#Chargement de l'image
cercleR = pygame.image.load("cercle_rouge.png").convert_alpha()
# Taille redimensionné car le cercle est importé d'un fichier
new_width = int(cercleR.get_width() * 0.1)  
new_height = int(cercleR.get_height() * 0.1)
#Cercle rétrécie
cercleR = pygame.transform.scale(cercleR, (new_width, new_height))
cercleR_rect = cercleR.get_rect(center=(screen.get_width() // 2, (screen.get_height() // 2)+100))
cercle = Rectangle(cercleR_rect,0)

def creation():
    l = []
    nbm = 84 #14*6 soit 5 lignes de 12 briques maximum
    nb = 0
    for i in range(14):
        for j in range(6):
            a = random.randint(0,1)
            if a == 1 and nb < nbm:
                nb+=1
                val = Rectangle(pygame.Rect((0+j*160), (0+i*30),160,30),1)
                val2 = Rectangle(pygame.Rect((1920-(1+j)*160), (0+i*30),160,30),1)
                
                vie_proba = random.randint(1,100)
                if vie_proba%2 == 0:
                    val.set_pv(2)
                    val.couleur()
                elif vie_proba%3 == 0:
                    val.set_pv(3)
                    val.couleur()
                else:
                    val.set_pv(1)
                l.append(val)
                
                vie_proba = random.randint(1,100)
                if vie_proba%2 == 0:
                    val2.set_pv(2)
                    val2.couleur()
                elif vie_proba%3 == 0:
                    val2.set_pv(3)
                    val2.couleur()
                else:
                    val2.set_pv(1)
                l.append(val2)
    return l

def bouge(r): # Permet a la plateforme de bouger si les touches sont appuyés
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s] and r.cote_pos()[2] > 0:
        r.deplacement(-400 * dt, 0)
    if keys[pygame.K_d] and r.cote_pos()[3] < screen.get_width():
        r.deplacement(400 * dt, 0)
    return

def afficher_score(score):
    # 2. Créer le texte en fonction du score
    texte = font.render(f"Score: {score}", True, (255, 255, 255))  # Texte en blanc
    # 3. Positionner le texte sur l'écran
    screen.blit(texte, (50, 50))  # Position du score (x=50, y=50)
    return

def bouge_c_dep(r,i,j,angle):
    dx = random.random()# Définit la direction de la balledef bouge_c_dep(r, i, j):
    if j == 0:
        r.deplacement(0, -400 * dt)
    else:
        r.deplacement(0, 400 * dt)
        
    if i == 0:
        if angle == True:
            r.deplacement((400 * dt)-5*dx,-5*dx)
            angle = False
        else:
            r.deplacement(400 * dt,0)
            
    else:
        if angle == True:
            r.deplacement((-400 * dt)+5*dx,-5*dx)
            angle = False
        else:
            r.deplacement(-400 * dt,0)
        
    return angle
    

def check_window_collision(circle, window_width, window_height,i,j): # Collision sur les bords de la fenêtre
    
    if circle.cote_pos()[2] < 7 or circle.cote_pos()[3] > window_width-10:
        i = (i+1)%2
        
    elif circle.cote_pos()[0] < 7 or circle.cote_pos()[1] > window_height-10:
        j = (j+1)%2
    return i,j

def touche_bri(l, cercle, i, j,score):
    for brique in l:
        x = brique.get_rect(); y = cercle.get_rect()
        if x.colliderect(y):
            score += 1000# Vérifie s'il y a collision
            # Calcul des distances entre les bords de la balle et ceux de la brique
            distance_bottom = x.top - y.bottom
            distance_top = y.top - x.bottom
            distance_right = x.left - y.right
            distance_left = y.left - x.right

            # Trouver la collision la plus proche
            if abs(distance_bottom) < 10:  # Collision par le bas
                j = (j+1) % 2
            elif abs(distance_top) < 10:  # Collision par le haut
                j = (j+1) % 2
            elif abs(distance_right) < 10:  # Collision par la droite
                i = (i+1) % 2
            elif abs(distance_left) < 10:  # Collision par la gauche
                i = (i+1) % 2
            # Une fois la collision détectée, on peut casser la brique (optionnel)
            if brique.vie == 1:
                l.remove(brique)# Supprimer la brique après collision
            else:
                brique.perte()
                brique.couleur()
            break
            # On s'arrête après une collision pour éviter de multiples détections

    return i, j, score

score = 0

while running:
        
    for event in pygame.event.get(): # Quitte la fenetre
        if event.type == pygame.QUIT:
            running = False

    if not start_g: # jeu pas démarré tant qu'aucune touche n'est appuyée
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] or keys[pygame.K_d]:
            start_g = True

    screen.fill("blue") # fond qui va être remplacée par une image soon
    #(int((screen.get_width() / 2)-100), (int(screen.get_height() / 2))) var test
    pygame.draw.rect(screen, (0, 0, 0), plateforme.get_rect())  # Dessine la plateforme
    pygame.draw.rect(screen, (255, 0, 0), cercle.get_rect(), 2)
    
    if start_g: # jeu démarré
        dt = clock.tick(60) / 1000 # Pour un déplacement non saccadé
        bouge(plateforme) # permet de faire bouger la plateforme
        
        if crea == 0:
            l = creation()
            crea+=1
        for k in range(len(l)):
            pygame.draw.rect(screen, (l[k].rgb[0], l[k].rgb[1], l[k].rgb[2]), l[k].get_rect())
            
        angle = bouge_c_dep(cercle,i,j,angle) # permet de faire bouger la balle
        screen.blit(cercleR, cercle.get_rect())# affiche la balle à l'écran avec sa position grâce au rect
        
        if plateforme.get_rect().colliderect(cercle.get_rect()):
            if cercle.cote_pos()[1] >= plateforme.cote_pos()[0]:
                cercle.rect.bottom = plateforme.rect.top
                angle = True
                j = (j+1)%2
                screen.fill("purple")
          # Déplace la balle légèrement vers le haut pour éviter qu'elle ne reste collée
            
        i,j,score = touche_bri(l,cercle,i,j,score)
        afficher_score(score)
        
        # changement de direction si le bord est touché
        i,j = check_window_collision(cercle, screen.get_width(), screen.get_height(),i,j)
        
    pygame.display.flip()

pygame.quit()