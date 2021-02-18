import pygame

pygame.init()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption("trafic simulation")
run = True
while run:
    for event in pygame.event.get():
        print(event)
        if event.type == 256: #quit event 
            run = False
        screen.fill((50,50,50))
        pygame.display.flip()
        



