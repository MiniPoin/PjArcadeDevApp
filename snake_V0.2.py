import pygame
import random

#Initialisation de pygame.
pygame.init()
pygame.font.init()

# Initialisation des variables graphiques.
screen_x = 1300
screen_y = 700
screen = pygame.display.set_mode((screen_x, screen_y))

pygame.display.set_caption("Snake")

clock = pygame.time.Clock()


#Initialisation des variables du jeu.
running = True
serpent_pos = pygame.Vector2(screen_x/2, screen_y/2)
serpent_rect = pygame.Rect(serpent_pos.x, serpent_pos.y, 50, 50)
pomme_pos = pygame.Vector2(random.randrange(0, screen_x, 50), random.randrange(0, screen_y, 50))
pomme_rect = pygame.Rect(pomme_pos.x, pomme_pos.y, 50, 50)

direction = ""

#Boucle principale du jeu.
while running:

    #Regarde quelle touche le joueur à touché et agit en fonction.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
    
    #Remoplie l'écran d'une couleur verte.
    screen.fill([0, 200, 0])
    
    #Les deux prochaines boucles permettent de créer la grille disponible sur l'écran.
    for i in range(50, screen_y, 50):
        pygame.draw.lines(screen, (0,100,0), True, ((0, i), (screen_x, i)))
        
    for i in range(50, screen_x, 50):
        pygame.draw.lines(screen, (0,100,0), True,((i, 0), (i, screen_y)))
    
    #Dessine le serpent en bleue et la pomme en rouge.
    pygame.draw.rect(screen, (0,0,200),(serpent_pos.x, serpent_pos.y, 50, 50))
    pygame.draw.rect(screen, (200,0,0),(pomme_pos.x, pomme_pos.y, 50, 50))
    
    #Fais bouger le serpent en fonction de sa direction.
    if direction == "UP" :
        serpent_pos.y -= 50
    if direction == "DOWN" :
        serpent_pos.y += 50
    if direction == "RIGHT" :
        serpent_pos.x += 50
    if direction == "LEFT" :
        serpent_pos.x -= 50
    
    #Bloque la pomme et le serpent dans les bords de la fenêtre.
    if serpent_pos.x < 0:
        serpent_pos.x = 0
    if serpent_pos.x + 50 > screen_x :
        serpent_pos.x = screen_x - 50
    if serpent_pos.y < 0:
        serpent_pos.y = 0
    if serpent_pos.y + 50 > screen_y :
        serpent_pos.y = screen_y - 50
    
    if pomme_pos.x < 0:
        pomme_pos.x = 0
    if pomme_pos.x + 50 > screen_x :
        pomme_pos.x = screen_x - 50
    if pomme_pos.y < 0:
        pomme_pos.y = 0
    if pomme_pos.y + 50 > screen_y :
        pomme_pos.y = screen_y - 50
    
    #Modifie la position des rectangles de la pomme et du serpent.
    serpent_rect.topleft = serpent_pos
    pomme_rect.topleft = pomme_pos
    
    #Verifie si le serpent à mangé la pomme, si oui alors une nouvelle pomme apparaît.
    if serpent_rect.colliderect(pomme_rect):
        pomme_pos = pygame.Vector2(random.randrange(0, screen_x, 50), random.randrange(0, screen_y, 50))
    
    #Modifie la position du rectangle de la pomme.
    pomme_rect.topleft = pomme_pos
    
    #Affiche les modifications à l'écran.
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
