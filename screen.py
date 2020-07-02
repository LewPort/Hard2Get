import pygame
ASPECT_RATIO = 1.33
HEIGHT = 160
WIDTH = int(HEIGHT*ASPECT_RATIO)

REAL_HEIGHT = 1080
REAL_WIDTH = int(REAL_HEIGHT*ASPECT_RATIO)
print('Game res = %i x %i' % (WIDTH, HEIGHT))
print('Screen res = %i x %i' % (REAL_WIDTH, REAL_HEIGHT))
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
DISPLAY = SCREEN.copy()
SCREEN = pygame.display.set_mode((REAL_WIDTH, REAL_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
FPS = 30
