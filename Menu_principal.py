import pygame
import Casse_briques
import Snakefinal
import demineur
import crédits
import Menu_options_0312024_2
import time

def lancement():
    # Les touches par défaut pour les jeux
    touches = [[pygame.key.name(pygame.K_UP), pygame.key.name(pygame.K_DOWN), pygame.key.name(pygame.K_LEFT), pygame.key.name(pygame.K_RIGHT)],
               [pygame.key.name(pygame.K_LEFT), pygame.key.name(pygame.K_RIGHT)]]
    touchesx = [[pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT],
               [pygame.K_LEFT, pygame.K_RIGHT]]
    # pygame setup
    pygame.init()
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    # Charger les images et définir les rectangles
    titres = []
    titresr = []

    # Charger les images
    titre = pygame.image.load("titre.png").convert_alpha()
    titre1 = pygame.image.load("casse_briques.png").convert_alpha()
    titre2 = pygame.image.load("snake.png").convert_alpha()
    titre3 = pygame.image.load("demineur.png").convert_alpha()
    options = pygame.image.load("options.png").convert_alpha()
    Crédits = pygame.image.load("credits.png").convert_alpha()
    quitte = pygame.image.load("quitter.png").convert_alpha()
    select = pygame.image.load("select.png").convert_alpha()

    # Ajouter les images dans les listes
    titres.extend([titre, titre1, titre2, titre3, options, Crédits, quitte])

    # Calculer les rectangles centrés pour chaque option
    for i in range(len(titres)):
        rect = titres[i].get_rect(center=(screen_width / 2, (i + 1) * (screen_height / 8)))
        titresr.append(rect)

    # Rectangle de sélection aligné avec la première option
    select_rect = select.get_rect(center=(titresr[0].centerx, titresr[0].centery))

    selection = 1  # Indice de l'option sélectionnée

    cdt = True
    # Boucle principale
    while cdt:
        dt = clock.tick(60) / 1000
        screen.fill((0, 0, 0))  # Remplir l'écran de noir
        
        # Afficher les options et le rectangle de sélection
        for i in range(len(titresr)):
            if i == selection:
                select_rect.centery = titresr[i].centery  # Placer le rectangle de sélection
                screen.blit(select, select_rect)
            screen.blit(titres[i], titresr[i])

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                        return
                elif event.key == pygame.K_SPACE:
                    if titres[selection] == titre1:
                        time.sleep(0.5)
                        if not Casse_briques.lancement(touchesx[1]):
                            cdt = False
                    elif titres[selection] == titre2:
                        time.sleep(0.5)
                        if not Snakefinal.main(touchesx[0]):
                            cdt = False
                    elif titres[selection] == titre3:
                        time.sleep(0.5)
                        if not demineur.main():
                            cdt = False
                    elif titres[selection] == options:
                        time.sleep(0.5)
                        touches,touchesx = Menu_options_0312024_2.lancement(touches,touchesx)
                    elif titres[selection] == Crédits:
                        time.sleep(0.5)
                        crédits.main()
                    else:
                        return
                elif event.key == pygame.K_DOWN:
                    selection += 1
                    if selection == 7:
                        selection = 1
                elif event.key == pygame.K_UP:
                    selection -= 1
                    if selection == 0:
                        selection = len(titres)-1
        pygame.display.flip()
    return
lancement()
pygame.quit()
