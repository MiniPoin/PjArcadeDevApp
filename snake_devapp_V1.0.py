import pygame
import random

# Initialisation de la fenêtre de pygame.
pygame.init()

#Initialisation du module font de pygame afin d'integrer du texte au jeu.
pygame.font.init()
font = pygame.font.Font(None, 40)

#Taille de l'écran du jeu.
screen_x = 1300
screen_y = 700

# Création d'une fenêtre de taille 1280*720.
screen = pygame.display.set_mode((screen_x, screen_y))

# Initialisation de la variable permettant de garder le jeu allumé.
running = True

#Initialisation de l'horloge du jeu.
clock = pygame.time.Clock()

# Initialisation de la position du serpent au milieu de la fenêtre.
serpent_pos = pygame.Vector2(screen_x / 2, screen_y / 2)
serpent_rect = pygame.Rect(serpent_pos.x, serpent_pos.y, 50, 50)

# Initialisation de la postion de la pomme à une postion aléatoire sur l'écran.
pomme_pos = pygame.Vector2(random.randrange(0,screen_x, 50), random.randrange(0,screen_y, 50))
pomme_rect = pygame.Rect(pomme_pos.x, pomme_pos.y, 50, 50)

#Variable direction, vu qu'aucune direction n'est utilisé alors celle-ci est vide.
direction = ''

#Classe regroupant touts les rectangles composant la queue du serpent.
class Queue_serpent():
    
    def __init__(self, rect):
        self.rect = rect
    
    def get_queue(self):
        return self.rect
    
    def set_queue(self, rect):
        self.rect = rect

#l est une liste de classe regroupant toutes les parties qui composent le serpent.
l = []
#Compteur d'élément dans le serpent commançant à 0.
l_queue = 0
#Integration de la tête du serpent dans la liste.
l.append(Queue_serpent(serpent_rect))

#Fonction permettant de créer la fenêtre de jeu.
def draw_screen():
    
    # Remplissage de la fenêtre en vert.
    screen.fill([0,200,0])
    
    #Les deux prochaines boucles permettent de créer la grille disponible sur l'écran.
    for i in range(50, screen_y, 50):
        pygame.draw.lines(screen, (0,150,0), True, ((0, i), (screen_x, i)))
        
    for i in range(50, screen_x, 50):
        pygame.draw.lines(screen, (0,150,0), True,((i, 0), (i, screen_y)))

#Fonction gerant les mouvements du serpent.
def mouv_serpent():
    
    #Recuperation de la variable global touche_ecran afin de pouvoir la modifier dans cette fonction.
    global touche_ecran
    
    #tete_x et tete_y recuperent les coordonnées de la tête du serpent.
    tete_x = l[0].get_queue().x
    tete_y = l[0].get_queue().y
    
    #Permet de deplacer le serpent de 50 pixels vers la direction donné par le joueur.
    if direction == 'RIGHT':
        tete_x += 50
    if direction == 'LEFT':
        tete_x -= 50
    if direction == 'UP':
        tete_y -= 50
    if direction == 'DOWN':
        tete_y += 50
    
    #Creer un rectangle avec les coordonnées de la nouvelle tête du serpent 
    nouv_tete = Queue_serpent(pygame.Rect(tete_x, tete_y, 50, 50))
    #Insert les nouvelles coordonnées à l'emplacement de l'ancienne tête, décalant toutes les classes d'un rang de 1.
    l.insert(0, nouv_tete)
    
    #Supprime la dernière valeur, n'existant plus dans le jeu. Sinon cela dupliquerai la longeur du serpent.
    l.pop()
    
    #Si le serpent se cogne contre les bords de la fênetre alors touche_ecran devient True, cela permettra ensuite d'afficher l'écran de game over.
    if tete_x < 0 :
        touche_ecran = True
        return touche_ecran
    if tete_x + 50 > screen_x:
        touche_ecran = True
        return touche_ecran
    if tete_y < 0:
        touche_ecran = True
        return touche_ecran
    if tete_y + 50 > screen_y:
        touche_ecran = True
        return touche_ecran

#Fonction qui affiche le serpent.
def affiche_serpent():

    #Recupere les coordonnées des rectangles et les affiches un par un.
    for segment in l:
        pygame.draw.rect(screen, (0, 0, 0), (segment.get_queue().x, segment.get_queue().y, 50, 50))

def mouv_pomme(l_queue):

    #Verifie si le rectangle de la tête est en colision avec le rectangle de la pomme.
    if l[0].get_queue().colliderect(pomme_rect) :
        # Change la position de la pomme sur une nouvelle coordonnée aléatoire.
        pomme_pos.x = random.randrange(0,screen_x, 50)
        pomme_pos.y = random.randrange(0,screen_y, 50)
        
        #Ajoute un rectangle dans la liste afin d'augmenter la longueur du serpent à l'écran.
        queue = Queue_serpent(pygame.Rect(l[l_queue].get_queue().x - 50, l[l_queue].get_queue().y, 50, 50))
        l_queue = l_queue + 1
        l.append(queue)
        
    #Verifie que la pomme ne soit pas à l'exterieur de l'écran et la bloque dans celui-ci.
    if pomme_pos.x < 0:
        pomme_pos.x = 0
    if pomme_pos.x + 50 > screen_x:
        pomme_pos.x = 1280 - 50
    if pomme_pos.y < 0:
        pomme_pos.y = 0
    if pomme_pos.y + 50 > screen_y:
        pomme_pos.y = screen_y - 50
        
    #Modifie la position du rectangle de la pomme.
    pomme_rect.topleft = pomme_pos

#Fonction qui affiche la pomme à l'écran.
def affiche_pomme():
    pygame.draw.rect(screen, [200,0,0], (pomme_pos.x, pomme_pos.y, 50, 50))

#Fonction de game_over afin de terminer le jeu.
def game_over(touche_ecran):
    
    #Si la variable touche_ecran est vraie alors le jeu affiche un message de game over avec le score affiché (nombre de pomme mangé).
    if touche_ecran :

        while True :

            screen.fill([0,0,0])
            texte = font.render(f"Qui à mis un mur en plein millieu de ce champs ?! Vous avez mangé {len(l)-1} pomme(s)", True, (255,255,255))
            screen.blit(texte, (0, screen_y/2))

            for event in pygame.event.get():
                key = pygame.key.get_pressed()
                if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                    return True

            pygame.display.flip()
            clock.tick(10)
    
    #Verifie si la tête ne rentre pas en colision avec le corps. Si c'est le cas alors le message de game over est affiché avec le scrore.
    for i in range(1,len(l)-1):

        if l[0].get_queue().colliderect(l[i].get_queue()):

            while True :

                screen.fill([0,0,0])
                texte = font.render(f"C'est le serpent qui se mord la queue ! Vous avez mangé {len(l)-1} pomme(s)", True, (255,255,255))
                screen.blit(texte, (0, screen_y/2))

                for event in pygame.event.get():
                        key = pygame.key.get_pressed()
                        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                            return True

                pygame.display.flip()
                clock.tick(10)

    return False

#Boucle permettant de garder le jeu allumé tant que le joueur n'appuie pas sur échap ou qu'il clique sur la croix rouge.
while running:
    
    #Boucle permettant de recuperer les clé pressé.
    for event in pygame.event.get():

        #Si la touche échap est pressée alors on arrête le jeu.
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Gérer les changements de direction
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
    
    touche_ecran = False
    
    #Appel de toute les fonctions vu plus haut, permettant le bon fonctionnement du jeu.
    draw_screen()
    
    mouv_serpent()
    affiche_serpent()
    
    mouv_pomme(l_queue)
    affiche_pomme()
    
    #Si game_over est vrai alors on arrête le jeu.
    if game_over(touche_ecran) :
        running = False
    
    # Rafraichissement de l'écran pour afficher les modification.
    pygame.display.flip()
    
    #Attend 10 tick, le temps de 10 fps, pour réactualiser le jeu.
    clock.tick(10)

# Fermeture de la fenêtre pygame.
pygame.quit()