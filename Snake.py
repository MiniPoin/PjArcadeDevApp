import pygame
import random

#Classe regroupant touts les rectangles composant la queue du serpent.
class Queue_serpent():
    
    def __init__(self, rect):
        self.rect = rect
    
    def get_queue(self):
        return self.rect
    
    def set_queue(self, rect):
        self.rect = rect

#Classe permettant de connaître l'état global du jeu.
class Arret_Jeu() :

    def __init__(self):
        self.touche_ecran = False
        self.stop = False

#Fonction permettant de créer la fenêtre de jeu.
def draw_screen(screen, game_surface, screen_x, screen_y):
    
    # Remplissage de la fenêtre en vert.
    screen.fill([0,0,0])
    
    # Dessiner la surface de jeu en vert
    game_surface.fill([0, 200, 0])
    
    #Les deux prochaines boucles permettent de créer la grille disponible sur l'écran.
    for i in range(0, screen_y, 50):
        pygame.draw.lines(game_surface, (0,150,0), True, ((0, i), (screen_x, i)))
        
    for i in range(0, screen_x, 50):
        pygame.draw.lines(game_surface, (0,150,0), True,((i, 0), (i, screen_y)))

    # Obtenir la position pour centrer la surface de jeu
    screen_width, screen_height = screen.get_size()
    game_pos_x = (screen_width - screen_x) // 2
    game_pos_y = (screen_height - screen_y) // 2

    # Dessiner la surface de jeu sur l'écran
    screen.blit(game_surface, (game_pos_x, game_pos_y))

    return game_pos_x, game_pos_y

#Fonction gerant les mouvements du serpent.
def mouv_serpent(serpent, direction, game_surface_x, game_surface_y, arret_jeu, screen_x, screen_y):

    #tete_x et tete_y recuperent les coordonnées de la tête du serpent.
    tete_x = serpent[0].get_queue().x
    tete_y = serpent[0].get_queue().y
    
    #Permet de deplacer le serpent de 50 pixels vers la direction donné par le joueur.
    if direction == 'RIGHT':
        tete_x += 50
    if direction == 'LEFT':
        tete_x -= 50
    if direction == 'UP':
        tete_y -= 50
    if direction == 'DOWN':
        tete_y += 50
    else :
        tete_x += 0
        tete_y += 0
    
    #Creer un rectangle avec les coordonnées de la nouvelle tête du serpent 
    nouv_tete = Queue_serpent(pygame.Rect(tete_x, tete_y, 50, 50))
    #Insert les nouvelles coordonnées à l'emplacement de l'ancienne tête, décalant toutes les classes d'un rang de 1.
    serpent.insert(0, nouv_tete)
    
    #Supprime la dernière valeur, n'existant plus dans le jeu. Sinon cela dupliquerai la longeur du serpent.
    serpent.pop()
    
    #Si le serpent se cogne contre les bords de la fênetre alors touche_ecran devient True, cela permettra ensuite d'afficher l'écran de game over.
    if (tete_x < game_surface_x
        or tete_x + 50 > game_surface_x+screen_x
        or tete_y < game_surface_y
        or tete_y + 50 > game_surface_y+screen_y):
        arret_jeu.touche_ecran = True

#Fonction qui affiche le serpent.
def affiche_serpent(serpent, screen):
    i=200
    #Recupere les coordonnées des rectangles et les affiches un par un.
    for segment in serpent:
        i -= 10
        if i < 0:
            i = 200
        pygame.draw.rect(screen, (0, 0, i), (segment.get_queue().x, segment.get_queue().y, 50, 50))

def mouv_pomme(serpent, l_queue, pomme_rect, pomme_pos, game_surface_x, game_surface_y, screen_x, screen_y):

    #Verifie si le rectangle de la tête est en colision avec le rectangle de la pomme.
    if serpent[0].get_queue().colliderect(pomme_rect) :
        # Change la position de la pomme sur une nouvelle coordonnée aléatoire.
        pomme_pos.x = random.randrange(game_surface_x, game_surface_x+screen_x, 50)
        pomme_pos.y = random.randrange(game_surface_y, game_surface_y+screen_y, 50)
        
        #Ajoute un rectangle dans la liste afin d'augmenter la longueur du serpent à l'écran.
        queue = Queue_serpent(pygame.Rect(serpent[l_queue].get_queue().x - 50, serpent[l_queue].get_queue().y, 50, 50))
        l_queue = l_queue + 1
        serpent.append(queue)
        
    #Verifie que la pomme ne soit pas à l'exterieur de l'écran et la bloque dans celui-ci.
    if pomme_pos.x < game_surface_x:
        pomme_pos.x = game_surface_x
    if pomme_pos.x + 50 > game_surface_x + screen_x:
        pomme_pos.x = game_surface_x + screen_y - 50
    if pomme_pos.y < game_surface_y:
        pomme_pos.y = game_surface_y
    if pomme_pos.y + 50 > game_surface_y + screen_y:
        pomme_pos.y = game_surface_y + screen_y - 50
    
    for i in range(0, len(serpent)-1):
        if serpent[i].get_queue().colliderect(pomme_rect) :
            pomme_pos.x = random.randrange(game_surface_x, game_surface_x+screen_x, 50)
            pomme_pos.y = random.randrange(game_surface_y, game_surface_y+screen_y, 50)
        
    #Modifie la position du rectangle de la pomme.
    pomme_rect.topleft = pomme_pos

#Fonction qui affiche la pomme à l'écran.
def affiche_pomme(pomme_pos, screen):
    pygame.draw.rect(screen, [200,0,0], (pomme_pos.x, pomme_pos.y, 50, 50))

#Fonction de game_over afin de terminer le jeu.
def game_over(screen, screen_height, screen_weigth, clock, serpent, font, font2, arret_jeu):

    #Si la variable touche_ecran est vraie alors le jeu affiche un message de game over avec le score affiché (nombre de pomme mangé).
    if arret_jeu.touche_ecran :

        while not arret_jeu.stop :

            screen.fill([0,0,0])
            texte = font.render("Qui à mis un mur en plein millieu de ce champs ?!", True, (255,255,255))
            screen.blit(texte, (screen_weigth//2 - texte.get_width()//2, screen_height//3))
            texte = font.render(f"Vous avez mangé {len(serpent)-1} pomme(s)", True, (255,255,255))
            screen.blit(texte, (screen_weigth//2 - texte.get_width()//2, screen_height//2))
            texte = font2.render("Appuyer sur ESPACE pour lancer un nouvelle partie !", True, (255,255,255))
            screen.blit(texte, (screen_weigth//2 - texte.get_width()//2, screen_height*3//4))

            arret_jeu.stop = True

            pygame.display.flip()
            clock.tick(10)
    
    #Verifie si la tête ne rentre pas en colision avec le corps. Si c'est le cas alors le message de game over est affiché avec le scrore.
    for i in range(1,len(serpent)-1):

        if serpent[0].get_queue().colliderect(serpent[i].get_queue()):

            while not arret_jeu.stop :

                screen.fill([0,0,0])
                texte = font.render("C'est le serpent qui se mord la queue !", True, (255,255,255))
                screen.blit(texte, (screen_weigth//2 - texte.get_width()//2, screen_height//3))
                texte = font.render(f"Vous avez mangé {len(serpent)-1} pomme(s)", True, (255,255,255))
                screen.blit(texte, (screen_weigth//2 - texte.get_width()//2, screen_height//2))
                texte = font2.render("Appuyer sur ESPACE pour lancer un nouvelle partie !", True, (255,255,255))
                screen.blit(texte, (screen_weigth//2 - texte.get_width()//2, screen_height*3//4))

                arret_jeu.stop = True

                pygame.display.flip()
                clock.tick(10)

def nv_partie():
    
    loop = True
    
    #Boucle pour savoir si le joueur souhaite arrêter ou continuer de jouer.
    while loop :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_nv = False
                loop = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_nv = False
                    loop = False

                elif event.key == pygame.K_SPACE:
                    running_nv = True
                    loop = False
                
    return running_nv

#Fonction affichant le score actuel du joueur dans le coin en haut à gauche de l'écran.
def affiche_score(font, serpent, screen):
    texte = font.render(f"Score : {len(serpent)-1}", True, (255,255,255))
    screen.blit(texte, (0, 0))

#Fonction permettant de creer une nouvelle pomme, remettre le serpent au millieu avec seulement sa tête.
def remise_zero(serpent, l_queue, arret_jeu, serpent_pos, game_surface_x, game_surface_y, screen_x, screen_y):
    serpent_pos = pygame.Vector2(game_surface_x+(screen_x/2), game_surface_y+(screen_y/2))
    serpent_rect = pygame.Rect(serpent_pos.x, serpent_pos.y, 50, 50)
    
    for i in range(0, len(serpent)):
        serpent.pop()

    serpent_nv = Queue_serpent(serpent_rect)
    serpent.append(serpent_nv)
    l_queue -= l_queue

    arret_jeu.touche_ecran = False
    arret_jeu.stop = False

#Fonction principale du programme.
def main(touchesx):
    
    #Initialisation de pygame.
    pygame.init()
    pygame.font.init()
    
    
    #Initialisation de toutes les variables graphiques.
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    
    screen_x, screen_y = 800, 800
    game_surface = pygame.Surface((screen_x, screen_y))
    
    pygame.display.set_caption("Snake")
    font = pygame.font.Font(None, 40)
    font2 = pygame.font.Font(None, 30)
    clock = pygame.time.Clock()
    game_surface_x, game_surface_y = draw_screen(screen, game_surface, screen_x, screen_y)

    #Initialisation des variables du jeu.
    running = True
    arret_jeu = Arret_Jeu()
    serpent_pos = pygame.Vector2(game_surface_x+(screen_x/2), game_surface_y+(screen_y/2))
    serpent_rect = pygame.Rect(serpent_pos.x, serpent_pos.y, 50, 50)
    pomme_pos = pygame.Vector2(random.randrange(game_surface_x, game_surface_x+screen_x, 50), random.randrange(game_surface_y, game_surface_y+screen_y, 50))
    pomme_rect = pygame.Rect(pomme_pos.x, pomme_pos.y, 50, 50)
    serpent = [Queue_serpent(serpent_rect)]
    l_queue = 0
    direction = ''

    #Boucle principale du jeu.
    while running:
        
        #Appel de toutes les fonctions du jeu.
        game_surface_x, game_surface_y = draw_screen(screen, game_surface, screen_x, screen_y)
        mouv_serpent(serpent, direction, game_surface_x, game_surface_y, arret_jeu, screen_x, screen_y)
        affiche_serpent(serpent, screen)
        mouv_pomme(serpent, l_queue, pomme_rect, pomme_pos, game_surface_x, game_surface_y, screen_x, screen_y)
        affiche_pomme(pomme_pos, screen)
        affiche_score(font, serpent, screen)
        game_over(screen, screen_height, screen_width, clock, serpent, font, font2, arret_jeu)

        #Regarde quelle touche le joueur à touché et agit en fonction.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                elif event.key == touchesx[0] and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == touchesx[1] and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == touchesx[2] and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == touchesx[3] and direction != 'LEFT':
                    direction = 'RIGHT'
        
        #Permet au joueur de choisir entre quitter le jeu ou le continuer si il a perdu.
        if arret_jeu.stop:
            continuer = nv_partie()
            
            if continuer == False :
                return True

            if continuer == True :

                remise_zero(serpent, l_queue, arret_jeu, serpent_pos, game_surface_x, game_surface_y, screen_x, screen_y)
                direction = ''

        pygame.display.flip()
        clock.tick(10)
    return False

pygame.quit()
