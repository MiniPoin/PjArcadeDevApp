import pygame
import random

class Demineur:
    def __init__(self,taille_ecran,num_mines):
        self.taille_ecran = taille_ecran
        self.num_mines = num_mines
        self.grille = [[0 for _ in range(taille_ecran)] for _ in range(taille_ecran)]
        self.decouvert = [[False for _ in range(taille_ecran)] for _ in range(taille_ecran)]
        self.flag = [[False for _ in range(taille_ecran)] for _ in range(taille_ecran)]
        self.game_over = False
        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        ajout_mines = self.num_mines
        while ajout_mines > 0:
            x = random.randint(0, self.taille_ecran - 1)
            y = random.randint(0, self.taille_ecran - 1)
            if self.grille[x][y] != 9:
                self.grille[x][y] = 9
                ajout_mines -= 1

    def calculate_numbers(self):
        for x in range(self.taille_ecran):
            for y in range(self.taille_ecran):
                if self.grille[x][y] != 9:
                    self.grille[x][y] = self.compte_mines_proches(x, y)

    def compte_mines_proches(self, x, y):
        prochaines_case = [
            (x-1, y-1), (x-1, y), (x-1, y+1),
            (x, y-1),           (x, y+1),
            (x+1, y-1), (x+1, y), (x+1, y+1)
        ]
        return sum(1 for i, j in prochaines_case if 0 <= i < self.taille_ecran and 0 <= j < self.taille_ecran and self.grille[i][j] == 9)

    def decouvre_case(self, x, y):
        if self.decouvert[x][y] or self.flag[x][y]:
            return
        self.decouvert[x][y] = True
        if self.grille[x][y] == 9:
            self.game_over = True
        elif self.grille[x][y] == 0:
            self.decouvre_cases_proche(x, y)
            
    def niveau(self,x,y,niv, RESTART_X, ECART_X, RESTART_Y, ECART_Y, CELL_SIZE):
        coord_x = RESTART_X + ECART_X//4
        coord_y = RESTART_Y//2 - 10
        if  coord_x + 0.5*ECART_X >= x >= coord_x and coord_y - ECART_Y + CELL_SIZE * 2 >= y >= coord_y - ECART_Y :
            return 1
        elif coord_x + 0.5*ECART_X >= x >= coord_x and coord_y + CELL_SIZE * 2 >= y >= coord_y:
            return 2
        elif coord_x + 0.5*ECART_X >= x >= coord_x and coord_y + ECART_Y + CELL_SIZE * 2 >= y >= coord_y + ECART_Y :
            return 3
        elif ECART_X//4 + 0.5*ECART_X >= x >= ECART_X//4 and coord_y - ECART_Y + CELL_SIZE * 2 >= y >= coord_y - ECART_Y :
            return 0
        return niv
    
    def coordonee(self, x, y,est_fini, niv, CELL_SIZE, taille_ecran):
        if taille_ecran + 1 >= y >= taille_ecran and x < taille_ecran :
            return 1
        elif x >= taille_ecran or y > taille_ecran + 1 or x < 0 or y < 0:
            return     
        elif est_fini :
            return
        else :
            self.decouvre_case(x,y)
            return 2

    def decouvre_cases_proche(self, x, y):
        prochaines_case = [
            (x-1, y-1), (x-1, y), (x-1, y+1),
            (x, y-1),           (x, y+1),
            (x+1, y-1), (x+1, y), (x+1, y+1)
        ]
        for i, j in prochaines_case:
            if 0 <= i < self.taille_ecran and 0 <= j < self.taille_ecran:
                self.decouvre_case(i, j)

    def est_une_mine(self, x, y, nb_mine_devine, est_fini, NUM_MINES, taille_ecran):
        if taille_ecran + 1 >= y >= taille_ecran and x < taille_ecran :
            return 1
        elif x >= taille_ecran or y > taille_ecran + 1 or x < 0 or y < 0 or est_fini :
            return     
        elif not self.decouvert[x][y]:
            if not self.flag[x][y] and nb_mine_devine == NUM_MINES :
                return
            self.flag[x][y] = not self.flag[x][y]
            if self.flag[x][y] == True :
                return 2
            return 3

    def verif_gagner(self):
        for x in range(self.taille_ecran):
            for y in range(self.taille_ecran):
                if self.grille[x][y] != 9 and not self.decouvert[x][y]:
                    return False
        return True
    
def compteur(game,part_gagner,nb_mine_devine,secondes, ECART_X, ECART_Y, CELL_SIZE, RESTART_X, font, screen, BLANC):
    mine = "mine :  " + str(nb_mine_devine)
    mine = font.render(mine, True, BLANC)
    screen.blit(mine, (ECART_X , ECART_Y - CELL_SIZE-10))
    part_str = "gagner :  " + str(part_gagner)
    part = font.render(part_str, True, BLANC)
    screen.blit(part,(RESTART_X - part.get_width(), ECART_Y - CELL_SIZE-10))
    temps_min = secondes // 60
    temps_sec = secondes % 60
    temps_str = str(temps_min) + " : " + str(temps_sec)
    temps = font.render(temps_str, True, BLANC)
    screen.blit(temps,(((RESTART_X - ECART_X)//2 + ECART_X - temps.get_width()), ECART_Y - CELL_SIZE-10))
    

def restart(game,niv, ECART_X, ECART_Y, RESTART_Y, RESTART_X, CELL_SIZE, screen, font2, font3, GRIS, NOIR, GRIS_FONCEE):
    fond2 = pygame.Rect(ECART_X , RESTART_Y + 5 , RESTART_X - ECART_X , CELL_SIZE * 2 - 10)
    pygame.draw.rect(screen,GRIS,fond2)
    restart = font3.render("RESTART", True, NOIR)
    screen.blit(restart, ((RESTART_X - ECART_X)//2 + ECART_X - restart.get_width()//2, RESTART_Y + 12))
    
    fond1 = pygame.Rect(ECART_X//4 - 5, RESTART_Y//2 - ECART_Y - 5, 0.5*ECART_X + 10, CELL_SIZE * 2 )
    pygame.draw.rect(screen,GRIS_FONCEE,fond1)
    fond2 = pygame.Rect(ECART_X//4, RESTART_Y//2 - ECART_Y , 0.5*ECART_X , CELL_SIZE * 2 - 10)
    pygame.draw.rect(screen,GRIS,fond2)
    menu = font2.render("MENU", True, NOIR)
    screen.blit(menu, (ECART_X//2 - menu.get_width()//2, RESTART_Y//2 - ECART_Y + 10))
    
    n1 = n2 = n3 = NOIR
    if niv == 1:
        n1 = GRIS_FONCEE
    elif niv == 2:
        n2 = GRIS_FONCEE
    else :
        n3 = GRIS_FONCEE
        
    fond1 = pygame.Rect(RESTART_X + ECART_X//4 - 5, RESTART_Y//2 - ECART_Y - 5, 0.5*ECART_X + 10, CELL_SIZE * 2 )
    pygame.draw.rect(screen,n1,fond1)
    fond2 = pygame.Rect(RESTART_X + ECART_X//4, RESTART_Y//2 - ECART_Y , 0.5*ECART_X , CELL_SIZE * 2 - 10)
    pygame.draw.rect(screen,GRIS,fond2)
    restart2 = font2.render("NIVEAU 1", True, NOIR)
    screen.blit(restart2, (RESTART_X + ECART_X//2 - restart2.get_width()//2, RESTART_Y//2 - ECART_Y + 10))
    
    fond1 = pygame.Rect(RESTART_X + ECART_X//4 - 5, RESTART_Y//2 - 5, 0.5*ECART_X + 10, CELL_SIZE * 2 )
    pygame.draw.rect(screen,n2,fond1)
    fond2 = pygame.Rect(RESTART_X + ECART_X//4, RESTART_Y//2 , 0.5*ECART_X , CELL_SIZE * 2 - 10)
    pygame.draw.rect(screen,GRIS,fond2)
    restart3 = font2.render("NIVEAU 2", True, NOIR)
    screen.blit(restart3, (RESTART_X + ECART_X//2 - restart3.get_width()//2, RESTART_Y//2 + 10))
    
    fond1 = pygame.Rect(RESTART_X + ECART_X//4 - 5, RESTART_Y//2 + ECART_Y - 5, 0.5*ECART_X + 10, CELL_SIZE * 2 )
    pygame.draw.rect(screen,n3,fond1)
    fond2 = pygame.Rect(RESTART_X + ECART_X//4, RESTART_Y//2 + ECART_Y , 0.5*ECART_X , CELL_SIZE * 2 - 10)
    pygame.draw.rect(screen,GRIS,fond2)
    restart4 = font2.render("NIVEAU 3", True, NOIR)
    screen.blit(restart4, (RESTART_X + ECART_X//2 - restart4.get_width()//2, RESTART_Y//2 + ECART_Y + 10))

def dessin_grille(game,part_gagner,nb_mine_devine,secondes,niv, ECART_X, ECART_Y, RESTART_X, RESTART_Y, CELL_SIZE, screen, font, font2, font3, font4, GRIS_FONCEE, NOIR, GRIS, ROUGE, BLANC):
    rect1 = pygame.Rect(ECART_X - 5, ECART_Y - 5, RESTART_X - ECART_X + 10, RESTART_Y - ECART_Y + CELL_SIZE * 2 + 5)
    pygame.draw.rect(screen,NOIR,rect1)
    for x in range(game.taille_ecran):
        for y in range(game.taille_ecran):
            rect = pygame.Rect(x*CELL_SIZE+ ECART_X, y*CELL_SIZE + ECART_Y , CELL_SIZE, CELL_SIZE)            
            if game.decouvert[x][y]:
                pygame.draw.rect(screen, GRIS if game.grille[x][y] == 0 else GRIS_FONCEE, rect)
                if game.grille[x][y] > 0:
                    fond = font4.render(str(game.grille[x][y]), True, NOIR)
                    screen.blit(fond, (x*CELL_SIZE + ECART_X + 5, y*CELL_SIZE + ECART_Y + 5))
            elif game.flag[x][y]:
                pygame.draw.rect(screen, ROUGE, rect)
            else:
                pygame.draw.rect(screen, BLANC, rect)
                
            pygame.draw.rect(screen,NOIR, rect, 1)
    restart(game,niv, ECART_X, ECART_Y, RESTART_Y, RESTART_X, CELL_SIZE, screen, font2, font3, GRIS, NOIR, GRIS_FONCEE)
    compteur(game,part_gagner,nb_mine_devine,secondes, ECART_X, ECART_Y, CELL_SIZE, RESTART_X, font, screen, BLANC)

def ecran_perdu(game,niv, CELL_SIZE, ECART_X, ECART_Y, RESTART_X, RESTART_Y, taille_ecran, screen, font2, font3, large_font, large_font2, GRIS, VERT, ROUGE, ORANGE, NOIR, GRIS_FONCEE):
    for x in range(game.taille_ecran):
        for y in range(game.taille_ecran):
            rect = pygame.Rect(x*CELL_SIZE+ ECART_X, y*CELL_SIZE + ECART_Y , CELL_SIZE, CELL_SIZE)            
            if game.grille[x][y] == 9:
                if game.flag[x][y] :
                    pygame.draw.rect(screen, VERT, rect)
                else :    
                    pygame.draw.rect(screen, ROUGE, rect)
            else :
                if game.flag[x][y] :
                    pygame.draw.rect(screen, ORANGE, rect)
            pygame.draw.rect(screen, NOIR, rect, 1)
    restart(game,niv, ECART_X, ECART_Y, RESTART_Y, RESTART_X, CELL_SIZE, screen, font2, font3, GRIS, NOIR, GRIS_FONCEE)
    
    text = large_font.render("PERDU !", True, ROUGE)
    screen.blit(text, ((RESTART_X - ECART_X)//2 + ECART_X- text.get_width()//2, (RESTART_Y)//2 + ECART_Y- text.get_width()//2))
    
    text = large_font2.render("PERDU !", True, NOIR)
    screen.blit(text, ((RESTART_X - ECART_X)//2 + ECART_X - text.get_width()//2, (RESTART_Y)//2 + ECART_Y- text.get_width()//2))


def ecran_gagner(game,niv, CELL_SIZE, ECART_X, ECART_Y, RESTART_X, RESTART_Y, screen, font2, font3, large_font, large_font2, GRIS, NOIR, GRIS_FONCEE, VERT):
    for x in range(game.taille_ecran):
        for y in range(game.taille_ecran):
            rect = pygame.Rect(x*CELL_SIZE+ ECART_X, y*CELL_SIZE + ECART_Y , CELL_SIZE, CELL_SIZE)            
            if game.grille[x][y] == 9:
                pygame.draw.rect(screen, VERT, rect)
            pygame.draw.rect(screen, NOIR, rect, 1)
    restart(game,niv, ECART_X, ECART_Y, RESTART_Y, RESTART_X, CELL_SIZE, screen, font2, font3, GRIS, NOIR, GRIS_FONCEE)
    
    text = large_font.render("GAGNÉ !", True, VERT)
    screen.blit(text, ((RESTART_X - ECART_X)//2 + ECART_X - text.get_width()//2, (RESTART_Y)//2 + ECART_Y- text.get_width()//2))
    
    text = large_font2.render("GAGNÉ !", True, NOIR)
    screen.blit(text, ((RESTART_X - ECART_X)//2 + ECART_X - text.get_width()//2, (RESTART_Y)//2 + ECART_Y- text.get_width()//2))


def main(part_gagner = 0,niv = 1):
    
    # Couleurs
    BLANC = (255, 255, 255)
    NOIR = (0, 0, 0)
    GRIS = (192, 192, 192)
    GRIS_FONCEE = (128, 128, 128)
    ROUGE = (255, 0, 0)
    VERT = (0, 255, 0)
    ORANGE = (200,200,50)

    # Initialisation Pygame
    pygame.init()

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
    font = pygame.font.SysFont("Monospace",24,True)
    font2 = pygame.font.SysFont("Monospace",20,True)
    font3 = pygame.font.SysFont("Monospace",26,True)
    font4 = pygame.font.SysFont("Monospace",20,True)
    large_font = pygame.font.SysFont(None, 123)
    large_font2 = pygame.font.SysFont(None, 120)
    
    NUM_MINES = niv * 30
    game = Demineur(taille_ecran,NUM_MINES)
    clock = pygame.time.Clock()
    temps = False
    temps2 = True
    est_fini = False
    nb_mine_devine = 0
    secondes = 0
    run = True
    while run:
        if temps2 and temps:
            depart = pygame.time.get_ticks()
            temps2 = False
            
        if temps and not temps2:
            secondes = (pygame.time.get_ticks() - depart) // 1000
            
        if game.game_over:
            ecran_perdu(game,niv, CELL_SIZE, ECART_X, ECART_Y, RESTART_X, RESTART_Y, taille_ecran, screen, font2, font3, large_font, large_font2, GRIS, VERT, ROUGE, ORANGE, NOIR, GRIS_FONCEE)
            temps = False
            est_fini = True
            
        elif game.verif_gagner() and not est_fini:
            ecran_gagner(game,niv, CELL_SIZE, ECART_X, ECART_Y, RESTART_X, RESTART_Y, screen, font2, font3, large_font, large_font2, GRIS, NOIR, GRIS_FONCEE, VERT)
            part_gagner += 1
            temps = False
        
        else:
            image = pygame.image.load('fontpyg.jpg')
            image = pygame.transform.scale(image, (LARGEUR_ECRAN + ECART_X, LONGUEUR_ECRAN + ECART_Y))
            screen.blit(image, (0, 0))
            dessin_grille(game,part_gagner,nb_mine_devine,secondes,niv, ECART_X, ECART_Y, RESTART_X, RESTART_Y, CELL_SIZE, screen, font, font2, font3, font4, GRIS_FONCEE, NOIR, GRIS, ROUGE, BLANC)
            
        if game.verif_gagner():
            ecran_gagner(game,niv, CELL_SIZE, ECART_X, ECART_Y, RESTART_X, RESTART_Y, screen, font2, font3, large_font, large_font2, GRIS, NOIR, GRIS_FONCEE, VERT)
    
        est_fini = game.verif_gagner()
               
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            
            elif event.type == pygame.MOUSEBUTTONDOWN :
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grille_x = (mouse_x - ECART_X) // CELL_SIZE
                grille_y = (mouse_y - ECART_Y) // CELL_SIZE
                niv = game.niveau(mouse_x,mouse_y,niv, RESTART_X, ECART_X, RESTART_Y, ECART_Y, CELL_SIZE)
                if niv == 0 :
                    #retour menu
                    return True
                if event.button == 1:  #clic gauche
                    a = game.coordonee(grille_x, grille_y, est_fini,niv, CELL_SIZE, taille_ecran)
                    if a == 1:
                        main(part_gagner,niv)
                        run = False
                    elif a == 2 and not temps:
                        temps = True 
                elif event.button == 3:  #clic droit
                    a = game.est_une_mine(grille_x, grille_y, nb_mine_devine, est_fini,NUM_MINES, taille_ecran)
                    if a == 1:
                        main(part_gagner,niv)
                        run = False
                    elif a == 2 :
                        nb_mine_devine += 1
                        temps = True 
                    elif a == 3 :
                        nb_mine_devine -= 1
                        temps = True 
        pygame.display.flip()
        clock.tick(100)
    return False
pygame.quit()