import random
import pygame
import levels
import objects
import screen
import sys

import animations


pygame.init()

CLOCK = pygame.time.Clock()
MUSIC = False

grey = (50,50,50)

    
class Key_commands:
        
    def process_inputs(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move('jump')
        if keys[pygame.K_a]:
            player.move('left')
        if keys[pygame.K_d]:
            player.move('right')

def gameloop():
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        levels.FLOOR_LEVEL_LIST = levels.update_floor_height()
        for bg in objects.BG_LIST:
            bg.update()
        keys.process_inputs()
        for object in objects.STATIC_LIST:
            object.update()
        player.update()
        resized_window = pygame.transform.scale(screen.DISPLAY, (screen.REAL_WIDTH, screen.REAL_HEIGHT))
        screen.SCREEN.blit(resized_window, (0, 0))
        pygame.display.update()
        CLOCK.tick(screen.FPS)

bg = objects.Background(animations.bg, 0, 0, velX=0.2, falls=False)
bg2 = objects.Background(animations.bg, - screen.WIDTH, 0, velX=0.2, falls=False)
player = objects.Player(animations.playerAnimationRepertoire, screen.WIDTH/2, screen.HEIGHT/2, 0, 0, 0.5)
for i in range(4):
    objects.Static(animations.palmAnimationRepertoire, random.randint(0, screen.WIDTH), screen.HEIGHT - 21,
                   falls=True, collisions=False)
for i in range(10):
    objects.Static(animations.box1AnimationRepertoire,
                   random.randint(0, screen.WIDTH), random.randint(0, levels.FLOOR_LEVEL), falls=False)

keys = Key_commands()

if __name__ == '__main__':
    playing = True
    gameloop()
    pygame.quit()
    sys.exit()
