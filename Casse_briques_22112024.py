import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True
start_g = False # quand l'utilisateur appuie sur la touche droite ou gauche (demarre)


# création mask pour les collisions et rect pour les positions
rect = pygame.Rect((int(screen.get_width() / 2)-100), (int(screen.get_height() / 2))+300,200,5)

cercleR = pygame.image.load("cercle_rouge.png").convert_alpha()
# Taille redimensionné car le cercle est importé d'un fichier
new_width = int(cercleR.get_width() * 0.1)  
new_height = int(cercleR.get_height() * 0.1) 
cercleR = pygame.transform.scale(cercleR, (new_width, new_height))
cercleR_rect = cercleR.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))


#Definit la direction de la balle
i = random.randint(0,1)
j = 0 # la balle va commence toujours par le haut


def bouge(r): # Permet a la plateforme de bouger si les touches sont appuyés
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s] and r.left > 0:
        r.move_ip(-350 * dt, 0)
    if keys[pygame.K_d] and r.right < screen.get_width():
        r.move_ip(350 * dt, 0)
    return

def bouge_c_dep(r,i,j): # Définit la direction de la balledef bouge_c_dep(r, i, j):
    if j == 0:
        r.move_ip(0, -400 * dt)
    else:
        r.move_ip(0, 400* dt)
    if i == 0:
        r.move_ip(-400 * dt, 0)
    else:
        r.move_ip(400 * dt, 0)
        
    return
    

def check_window_collision(circle_rect, window_width, window_height,i,j): # Collision sur les bords de la fenêtre
    if circle_rect.left < 0 or circle_rect.right > window_width:
        i = (i+1)%2
        
    elif circle_rect.top < 0 or circle_rect.bottom > window_height:
        j = (j+1)%2
    return i,j
    
   
while running:
        
    for event in pygame.event.get(): # Quitte la fenetre
        if event.type == pygame.QUIT:
            running = False

    if not start_g: # Jeu pas démarré tant qu'aucune touche n'est appuyée
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] or keys[pygame.K_d]:
            start_g = True

    
    screen.fill("blue") # Fond de test
    pygame.draw.rect(screen, (0, 0, 0), rect)  # Dessine la plateforme
    pygame.draw.rect(screen, (255, 0, 0), cercleR_rect, 2)
    
    if start_g: # Jeu démarré
        dt = clock.tick(120) / 1000 # Pour un déplacement non saccadé
        bouge(rect) # Permet de faire bouger la plateforme
        bouge_c_dep(cercleR_rect,i,j) # Permet de faire bouger la balle
        screen.blit(cercleR, cercleR_rect) # Affiche la balle à l'écran avec sa position grâce au rect
        if rect.colliderect(cercleR_rect):
            if cercleR_rect.bottom <= rect.bottom:
                j = (j+1)%2
                screen.fill("purple")
            
        
        # Changement de direction si le bord est touché
        i,j = check_window_collision(cercleR_rect, screen.get_width(), screen.get_height(),i,j)
        
    pygame.display.flip()

pygame.quit()