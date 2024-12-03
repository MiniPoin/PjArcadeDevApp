import pygame

# Fonction pour gérer l'entrée des touches
def entree_touches(touches, choix_touche, key):
    if key != pygame.K_ESCAPE:
        touches[choix_touche[0]][choix_touche[1]] = pygame.key.name(key)
    return touches

def lancement():

    # Initialisation de Pygame
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    # Liste des titres et rectangles associés
    titres = []
    titresr = []

    # Chargement des images
    titre = pygame.image.load("Options.png").convert_alpha()
    titre1 = pygame.image.load("snake.png").convert_alpha()
    titre2 = pygame.image.load("casse_briques.png").convert_alpha()
    titre3 = pygame.image.load("demineur.png").convert_alpha()
    quitte = pygame.image.load("quitter.png").convert_alpha()
    select = pygame.image.load("select.png").convert_alpha()
    haut = pygame.image.load("haut.png").convert_alpha()
    bas = pygame.image.load("bas.png").convert_alpha()
    gauche = pygame.image.load("gauche.png").convert_alpha()
    droite = pygame.image.load("droite.png").convert_alpha()

    # Ajout des images dans les listes
    titres.extend([titre1, titre2, titre3, haut, bas, gauche, droite, titre, select, quitte])
    titres_sec = [haut, bas, gauche, droite]
    titres_principaux = []
    font = pygame.font.Font(None, 74)

    # Positionnement des rectangles des options principales et secondaires
    for i in range(2):
        rect = titres[i].get_rect(center=((2 * (i + 1)) * (screen.get_width() / 6), 3 * (screen.get_height() / 12)))
        titres_principaux.append(rect)
        if i == 0:
            titresr.extend([titres[j].get_rect(center=(titres_principaux[i].centerx - 150, titres_principaux[i].centery + (j - 2) * 100)) for j in range(3, 7)])
        else:
            titresr.extend([titres[j].get_rect(center=(titres_principaux[i].centerx - 150, titres_principaux[i].centery + (j - 4) * 100)) for j in range(5, 7)])

    # Définition des touches par défaut
    touches = [[pygame.key.name(pygame.K_UP), pygame.key.name(pygame.K_DOWN), pygame.key.name(pygame.K_LEFT), pygame.key.name(pygame.K_RIGHT)],
               [pygame.key.name(pygame.K_LEFT), pygame.key.name(pygame.K_RIGHT)]]

    # Rectangle de sélection
    select_rect = select.get_rect(center=(titres_principaux[0].centerx - 30, titres_principaux[0].centery))
    select_rect = select_rect.inflate(2, 2)

    # Variables de contrôle
    attente_select = False
    choix = 0
    cdt = True
    niveau_selection = "principal"
    sous_selection = 0
    temp = None

    # Position des rectangles "Options" et "Quitter"
    rect_quitter = titres[9].get_rect(center=(screen.get_width() / 2, screen.get_height() - 200))
    rect_options = titres[7].get_rect(center=(screen.get_width() / 2, screen.get_height() / 10))

    # Boucle principale
    while cdt:
        text = None

        if niveau_selection == "changement":
            screen.fill((93, 65, 123))
        else:
            screen.fill((0, 0, 0))

        screen.blit(titres[7], rect_options)
        screen.blit(titres[9], rect_quitter)
        text_rem = font.render("Espace pour choisir, echap pour sortir", True, (255, 255, 255))
        screen.blit(text_rem, text_rem.get_rect(center = (rect_quitter.centerx-550,screen.get_height()-100)).inflate(-200,-20))
        dt = clock.tick(60) / 1000

        # Affichage des options principales
        for i in range(len(titres_principaux)):
            if i == choix and niveau_selection == "principal" and temp != 0:
                select_rect.centerx = titres_principaux[i].centerx
            screen.blit(titres[i], titres_principaux[i])

        # Affichage des options secondaires
        for j in range(len(titresr)):
            if j == 0:
                screen.blit(titres_sec[0], titresr[j])
                text = font.render(touches[0][0], True, (255, 255, 255))
            elif j == 1:
                screen.blit(titres_sec[1], titresr[j])
                text = font.render(touches[0][1], True, (255, 255, 255))
            elif j in [2, 4]:
                screen.blit(titres_sec[2], titresr[j])
                text = font.render(touches[0][2] if j == 2 else touches[1][0], True, (255, 255, 255))
            elif j in [3, 5]:
                screen.blit(titres_sec[3], titresr[j])
                text = font.render(touches[0][3] if j == 3 else touches[1][1], True, (255, 255, 255))
            text_rect = text.get_rect(center=(titresr[j].right + 80, titresr[j].centery))
            screen.blit(text, text_rect)

        # Affichage du rectangle de sélection
        screen.blit(select, select_rect)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if niveau_selection == "principal":
                    if event.key == pygame.K_RIGHT and temp != 0:
                        choix = (choix + 1) % len(titres_principaux)
                    elif event.key == pygame.K_ESCAPE:
                        cdt = False
                    elif event.key == pygame.K_DOWN and temp != 0:
                        temp = 0
                        select_rect.centerx = rect_quitter.centerx
                        select_rect.centery = rect_quitter.centery
                    elif event.key == pygame.K_UP and temp == 0:
                        temp = None
                        select_rect.centerx = titres_principaux[choix].centerx
                        select_rect.centery = titres_principaux[choix].centery
                    elif event.key == pygame.K_LEFT and temp != 0:
                        choix = (choix - 1) % len(titres_principaux)
                    elif event.key == pygame.K_SPACE:
                        if temp == 0:
                            cdt = False
                        niveau_selection = "sous_choix"
                        sous_selection = 0
                        if choix == 0:
                            debut_sous_choix, nb_sous_choix = 0, 4
                        elif choix == 1:
                            debut_sous_choix, nb_sous_choix = 4, 2
                        select_rect.centery = titresr[debut_sous_choix + sous_selection].centery

                elif niveau_selection == "sous_choix":
                    if event.key == pygame.K_ESCAPE:
                        niveau_selection = "principal"
                        select_rect.centery = titres_principaux[choix].centery
                    else:
                        if event.key == pygame.K_DOWN:
                            sous_selection = (sous_selection + 1) % nb_sous_choix
                        elif event.key == pygame.K_UP:
                            sous_selection = (sous_selection - 1) % nb_sous_choix
                        elif event.key == pygame.K_SPACE:
                            attente_select = True
                            option_choisi = [choix, sous_selection]
                            niveau_selection = "changement"
                            continue
                        select_rect.centery = titresr[debut_sous_choix + sous_selection].centery

                elif niveau_selection == "changement":
                    niveau_selection = "sous_choix"
                    touches = entree_touches(touches, option_choisi, event.key)
                    select_rect.centery = titresr[debut_sous_choix + sous_selection].centery

        pygame.display.flip()
    pygame.quit()
    return touches
lancement()
