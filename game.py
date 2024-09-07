import pickle
import pygame
import neat
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
    
    font = pygame.font.Font("assets/fonts/Tiny5-Regular.ttf", 36)
    
    lastScore = 0
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
        
        text = font.render('Score: ' + str(player.score), True, (255, 0, 20))
        text_rect = text.get_rect(center = (450, 20))
        
        textLast = font.render('Last Run: ' + str(lastScore), (True), (255, 0, 20))
        textLast_rect = text.get_rect(center = (450, 80))
        
        screen.fill((0, 0, 0))
        platforms, ladders = drawMap()
        screen.blit(dk, dkPos)
        screen.blit(peach, peachPos)
        screen.blit(barrel_stack, (20, 130))
        screen.blit(text, text_rect)
        screen.blit(textLast, textLast_rect)
        
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
        
        if timeSinceLastSpawn > (random.randint(20, 50) / 10):
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
        
        if player.checkBarrelCollision(barrels) or player.gameWon:
            if not player.gameWon:
                lastScore = player.score
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

def eval_genomes(genomes, config):
    nets = []
    players = []
    ge = []
    barrels = []
    timeSinceLastSpawn = 0
    dt = 0
    clock = pygame.time.Clock()

    #font = pygame.font.Font("assets/fonts/Tiny5-Regular.ttf", 36)
    
    lastScore = 0
    dk = dk2
    dkPos = (75, 105)
    peach = peach2
    
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Player(screen)) 
        genome.fitness = 0
        ge.append(genome)
    
    running = True
    while running and len(players) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        platforms, ladders = drawMap()
        screen.blit(dk, dkPos)
        screen.blit(peach, peachPos)
        screen.blit(barrel_stack, (20, 130))
        
        timeSinceLastSpawn += dt
        if timeSinceLastSpawn > (random.randint(20, 50) / 10):
            timeSinceLastSpawn = 0
            barrels.append(Barrel(screen, platforms, ladders, 110, 215))
        
        for x, player in enumerate(players):
            player.gravity(platforms, dt)

            inputs = [player.playerRect.x, player.playerRect.y, player.isClimbing, player.isJumping, player.isNearLadder]
            
            nearest = player.nearestBarrels(barrels)
            for entry in nearest:
                inputs.extend(entry)

            if len(inputs) != 20:
                print("wrong input count")                

            output = nets[x].activate(inputs)
            if output[0] > 0.5:  
                player.jump(dt)
            if output[1] > 0.5:  
                player.moveRight(ladders, dt)
            if output[2] > 0.5:  
                player.moveLeft(ladders, dt)
            if output[3] > 0.5:
                player.climb(ladders, True, dt) #climb up
            if output[4] > 0.5:
                player.climb(ladders, False, dt) #climb down

            player.draw()

        for barrel in barrels:
            barrel.update(dt)
            barrel.draw()

        for x, player in enumerate(players):
            if player.checkBarrelCollision(barrels):
                ge[x].fitness -= 1
                players.pop(x)
                nets.pop(x)
                ge.pop(x)
            else:
                ge[x].fitness += 1  # Reward survival

        if len(players) == 0:
            break

        pygame.display.flip()
        dt = clock.tick(30) / 1000

    pygame.quit()

def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path
    )

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, 50)

    with open('winner.pkl', 'wb') as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
    #main()
