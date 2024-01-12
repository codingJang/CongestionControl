import pygame
from components.graph import Graph

pygame.init()
logo = pygame.image.load('images/logo_32x32.png')
pygame.display.set_icon(logo)
pygame.display.set_caption('Congestion Control Simulation')
screen = pygame.display.set_mode((960, 960))
clock = pygame.time.Clock()
graph = Graph(3, 3)
running = True
while running:
    for event in pygame.event.get():
        # only do something if the event is of type QUIT
        if event.type == pygame.QUIT:
            # change the value to False, to exit the main loop
            running = False
    screen.fill((0, 0, 0))
    graph.step(screen=screen)
    pygame.display.flip()
    clock.tick(30)
