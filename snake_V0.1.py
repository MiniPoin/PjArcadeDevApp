import pygame
import random


#Initialisation de pygame.
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((1280, 720))

pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

dt = 0

#Initialisation des variables du jeu.
running = True
serpent_pos = pygame.Vector2(1280/2, 720/2)
pomme_pos = pygame.Vector2(random.randrange(0, 1280, 50), random.randrange(0, 720, 50))


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
    
    screen.fill([0, 255, 0])
    
    pygame.draw.rect(screen, (0,0,0),(serpent_pos.x, serpent_pos.y, 50, 50))
    pygame.draw.rect(screen, (255,0,0),(pomme_pos.x, pomme_pos.y, 50, 50))
    
    if direction == "UP" :
        serpent_pos.y -= 500*dt
    if direction == "DOWN" :
        serpent_pos.y += 500 * dt
    if direction == "RIGHT" :
        serpent_pos.x += 500 * dt
    if direction == "LEFT" :
        serpent_pos.x -= 500 * dt
    
    if serpent_pos.x < 0:
        serpent_pos.x = 0
    if serpent_pos.x + 50 > 1280 :
        serpent_pos.x = 1280 - 50
    if serpent_pos.y < 0:
        serpent_pos.y = 0
    if serpent_pos.y + 50 > 720 :
        serpent_pos.y = 720 - 50
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
