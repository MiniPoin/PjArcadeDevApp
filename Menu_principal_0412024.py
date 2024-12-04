import pygame
import time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

# Charger les images et dÃ©finir les rectangles
titres = []
titresr = []

# Charger les images
titre = pygame.image.load("titre.png").convert_alpha()
titre1 = pygame.image.load("casse_briques.png").convert_alpha()
titre2 = pygame.image.load("snake.png").convert_alpha()
titre3 = pygame.image.load("demineur.png").convert_alpha()
options = pygame.image.load("options.png").convert_alpha()
quitte = pygame.image.load("quitter.png").convert_alpha()
select = pygame.image.load("select.png").convert_alpha()

# Ajouter les images dans les listes
titres.extend([titre, titre1, titre2, titre3, options, quitte])

# Calculer les rectangles centrÃ©s pour chaque option
for i in range(len(titres)):
    rect = titres[i].get_rect(center=(screen.get_width() / 2, (i + 1) * (screen.get_height() / 7)))
    titresr.append(rect)

# Rectangle de sÃ©lection alignÃ© avec la premiÃ¨re option
select_rect = select.get_rect(center=(titresr[0].centerx, titresr[0].centery))

selection = 1  # Indice de l'option sÃ©lectionnÃ©e

# Boucle principale
while True:
    dt = clock.tick(60) / 1000
    screen.fill((0, 0, 0))  # Remplir l'Ã©cran de noir
    
    # Afficher les options et le rectangle de sÃ©lection
    for i in range(len(titresr)):
        if i == selection:
            select_rect.centery = titresr[i].centery  # Placer le rectangle de sÃ©lection
            screen.blit(select, select_rect)
        screen.blit(titres[i], titresr[i])

    # GÃ©rer les Ã©vÃ©nements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.key == pygame.K_SPACE:
                if titres[selection] == titre1:
                    time.sleep(1)
                    # On lance le casse briques
                if titres[selection] == titre2:
                    time.sleep(1)
                    # On lance le snake
                if titres[selection] == titre3:
                    time.sleep(1)
                    # On lance le démineur
            elif event.key == pygame.K_s and selection < len(titres) - 1:
                selection += 1
            elif event.key == pygame.K_z and selection > 1:
                selection -= 1
    
    pygame.display.flip()
        