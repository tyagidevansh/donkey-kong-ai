import pygame
import random
from player import Player
from bridge import Bridge
from ladder import Ladder
from barrel import Barrel
from settings import *

def drawMap():
    platforms = []
    climbers = []
    ladder_objs = []
    bridge_objs = []

    ladders = levels[active_level]['ladders']
    bridges = levels[active_level]['bridges']

    for ladder in ladders:
        ladder_objs.append(Ladder(*ladder))
        if ladder[2] >= 3:
            climbers.append(ladder_objs[-1].body)
    for bridge in bridges:
        bridge_objs.append(Bridge(*bridge))
        platforms.append(bridge_objs[-1].top)

    return platforms, climbers

def main():
  
    clock = pygame.time.Clock()
    running = True
    dt = 0

    player = Player(screen)
    barrels = []
    timeSinceLastSpawn = 0
    framesSinceSwitch = 0
    timeSinceDeath = 0
    
    dk = dk2
    dkPos = (75, 105)
    peach = peach2
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.isMoving = False

        screen.fill((0, 0, 0))
        platforms, ladders = drawMap()
        screen.blit(dk, dkPos)
        screen.blit(peach, peachPos)
        

        player.gravity(platforms, dt)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.jump(dt)
        if keys[pygame.K_UP]:
            player.climb(ladders, True, dt)
        if keys[pygame.K_DOWN]:
            player.climb(ladders, False, dt)
        if keys[pygame.K_LEFT]:
            player.moveLeft(ladders, dt)
        if keys[pygame.K_RIGHT]:
            player.moveRight(ladders, dt)

        player.draw()
        
        timeSinceLastSpawn += dt
        
        if 0.5 < timeSinceLastSpawn < 1:
            dk = dk2
            dkPos = (75, 105)
        if timeSinceLastSpawn > 1.5:
            dk = dk3
            dkPos = (80, 112)
        
        if timeSinceLastSpawn > (random.randint(30, 60) / 10):
            timeSinceLastSpawn = 0
            dk = dk1
            barrels.append(Barrel(screen, platforms, ladders, 110, 215))
            i = 0
            while i < len(barrels):
                if not barrels[i].isAlive:
                    barrels.pop(i)
                    i -= 1
                i += 1
        
        for barrel in barrels:
            barrel.update(dt)
            barrel.draw()
        
        if player.checkBarrelCollision(barrels):
            player.reset()
            barrels.clear()
            pygame.time.wait(1000)
            
        if framesSinceSwitch < 16:
            screen.blit(fire_barrel1, (barrelX, barrelY))
        else:
            screen.blit(fire_barrel2, (barrelX, barrelY))
        
        framesSinceSwitch = (framesSinceSwitch + 1) % 32 

        pygame.display.flip()
        dt = clock.tick(30) / 1000
    
    pygame.quit()

if __name__ == "__main__":
    main()
