import pygame


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

rect = pygame.Rect((int(screen.get_width() / 2)-100), (int(screen.get_height() / 2))+300,200,5)
cercleR = pygame.image.load("cercle_rouge.png").convert_alpha()
# Taille redimensionné car le cercle est importé d'un fichier
new_width = int(cercleR.get_width() * 0.1)  
new_height = int(cercleR.get_height() * 0.1)
#Cercle rétrécit
cercleR = pygame.transform.scale(cercleR, (new_width, new_height))
cercleR_rect = cercleR.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("purple")
    pygame.display.flip()

    clock.tick(60)

pygame.quit()