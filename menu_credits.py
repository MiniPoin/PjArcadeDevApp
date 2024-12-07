import pygame

def dessin(x,y,ECART_X,ECART_Y,RESTART_X,RESTART_Y,ORANGE,NOIR,BLEU,font4,font5,screen):
    GRIS = (192, 192, 192)
    GRIS_FONCEE = (128, 128, 128)
    large_font = pygame.font.SysFont("Monospace", 80)
    rect1 = pygame.Rect(ECART_X - 5, ECART_Y - 50, RESTART_X - ECART_X + 10, RESTART_Y - ECART_Y + 55)
    pygame.draw.rect(screen,BLEU,rect1)
    
    credit(x,y,ECART_Y,RESTART_Y,ORANGE,font4,font5,screen)
    
    rect1 = pygame.Rect(ECART_X - 5, ECART_Y - 50, RESTART_X - ECART_X + 10,100)
    pygame.draw.rect(screen,BLEU,rect1)
    text = large_font.render("CRÉDITS", True, ORANGE)
    screen.blit(text, ((RESTART_X - ECART_X)//2 + ECART_X - text.get_width()//2, ECART_Y//2 +70))
    
    rect1 = pygame.Rect(ECART_X - 5, RESTART_Y - 50, RESTART_X - ECART_X + 10,50)
    pygame.draw.rect(screen,BLEU,rect1)
    
    fond1 = pygame.Rect(ECART_X//4 - 5, ECART_Y*2 - 5,(ECART_X//2) +10,60)
    pygame.draw.rect(screen,GRIS_FONCEE,fond1)
    fond2 = pygame.Rect(ECART_X//4, ECART_Y*2,ECART_X//2,50)
    pygame.draw.rect(screen,GRIS,fond2)
    menu = font4.render("MENU", True, NOIR)
    screen.blit(menu, (ECART_X//2 - menu.get_width()//2, ECART_Y*2+ 10))


def credit(x,y,ECART_Y,RESTART_Y,ORANGE,font4,font5,screen):
    credits = [
        ("SNAKE", "KIERANE BOUTTEMANT"),
        ("DEMINEUR", "AXEL ANDRE"),
        ("CASSE BRIQUE", "ISMAEL BERGHIOUA"),
        ("MENU CRÉDITS", "AXEL ANDRE"),
        ("MENU PRINCIPAL", "ISMAEL BERGHIOUA"),
        ("MENU OPTION", "ISMAEL BERGHIOUA"),
        ("ADAPTATION DES FICHIERS", "KIERANE BOUTTEMANT"),
        ("PROF DE L'ANNEE","R.TOMCZACK")
    ]
    
    for titre, auteur in credits:
        titre_text = font5.render(titre, True, ORANGE)
        auteur_text = font4.render(auteur, True, ORANGE)

        # Afficher le titre si dans les limites
        if ECART_Y - 50 <= y <= RESTART_Y -50:
            screen.blit(titre_text, (x - titre_text.get_width()//2, y))
        y += titre_text.get_height() + 10  # Espacement après le titre

        # Afficher l'auteur si dans les limites
        if ECART_Y - 50 <= y <= RESTART_Y - 50 :
            screen.blit(auteur_text, (x - auteur_text.get_width()//2 , y))
        y += auteur_text.get_height() + 30  # Espacement après l'auteur

    
def main():
    # Initialisation Pygame
    pygame.init()
    
    # Couleurs
    BLANC = (255, 255, 255)
    NOIR = (0, 0, 0)
    ORANGE = (200,200,50)
    BLEU = (0, 0, 25)
    
    #Style
    font4 = pygame.font.SysFont("Monospace",30,True)
    font5 = pygame.font.SysFont("Monospace",40,True)

    # Dimensions
    CELL_SIZE = 25
    taille_ecran = 25  # 25x25 grille
    screen_info = pygame.display.Info()
    LONGUEUR_ECRAN = screen_info.current_h
    LARGEUR_ECRAN = screen_info.current_w
    ECART_X = (LARGEUR_ECRAN - taille_ecran*CELL_SIZE)//2 - 50
    ECART_Y = (LONGUEUR_ECRAN - taille_ecran*CELL_SIZE)//2 
    RESTART_X = taille_ecran * CELL_SIZE + ECART_X #630
    RESTART_Y = taille_ecran * CELL_SIZE + ECART_Y
    screen = pygame.display.set_mode((LARGEUR_ECRAN , LONGUEUR_ECRAN + ECART_Y), pygame.FULLSCREEN)
    pygame.display.set_caption("Démineur")
    clock = pygame.time.Clock()
    image = pygame.image.load('fontpyg.jpg')
    image = pygame.transform.scale(image, (LARGEUR_ECRAN + ECART_X, LONGUEUR_ECRAN + ECART_Y))
    screen.blit(image, (0, 0))
    run = True
    x =  RESTART_X//2 + (RESTART_X - ECART_X)//2
    y = RESTART_Y + 25
    
    x_quit = ECART_X//4 - 5 
    y_quit = ECART_Y*2- 5 
    while run :
        y = y - 1
        if(y <= -ECART_Y *3):
            y = RESTART_Y + 25
        screen.blit(image, (0, 0))
        dessin(x,y,ECART_X,ECART_Y,RESTART_X,RESTART_Y,ORANGE,NOIR,BLEU,font4,font5,screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN :
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if x_quit <= mouse_x <= x_quit + (ECART_X//2) +10 and y_quit <= mouse_y <= y_quit + 60 :
                    return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
        pygame.display.flip()
        clock.tick(100)
    return False
main()
pygame.quit()
