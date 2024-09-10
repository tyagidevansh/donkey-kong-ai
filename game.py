import pickle
import pygame
import neat
import random
from player import Player
from barrel import Barrel
from settings import *
from utils import *

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
        #player.nearestBarrels(barrels)
        
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
    framesSinceSwitch = 0
    clock = pygame.time.Clock()

    font = pygame.font.Font("assets/fonts/Tiny5-Regular.ttf", 36) 
    lastY = window_height - 200
    lastScore = 0
    dk = dk2
    dkPos = (75, 105)
    peach = peach2
    
    best_fitness = -float('inf')  
    best_genome = None
    
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
            dk = dk1
            barrels.append(Barrel(screen, platforms, ladders, 110, 215))
            i = 0
            while i < len(barrels):
                if not barrels[i].isAlive:
                    barrels.pop(i)
                    i -= 1
                i += 1
        
        for x, player in enumerate(players):
            player.gravity(platforms, dt)

            inputs = [player.playerRect.x, player.playerRect.y, player.isClimbing, player.isJumping, player.isNearLadder, player.closestLadder]
            
            nearest = player.nearestBarrels(barrels)
            for entry in nearest:
                inputs.append(entry[1])
                inputs.append(entry[2])

            inputs = [int(val) if isinstance(val, bool) else val for val in inputs]

            if len(inputs) != 10:
                print("wrong input count")                

            #print(inputs)

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
            player.update(dt)
            
        timeSinceLastSpawn += dt
        
        if 0.5 < timeSinceLastSpawn < 1:
            dk = dk2
            dkPos = (75, 105)
        if timeSinceLastSpawn > 1.5:
            dk = dk3
            dkPos = (80, 112)

        for barrel in barrels:
            barrel.update(dt)
            barrel.draw()

        for x, player in enumerate(players):
            if player.checkBarrelCollision(barrels):
                ge[x].fitness -= 100 
                players.pop(x)
                nets.pop(x)
                ge.pop(x)
            else:
                height_diff = player.lastY - player.playerRect.y
                if height_diff > 0:
                    ge[x].fitness += height_diff * 0.1 

                    if player.isClimbing:
                        ge[x].fitness += 5  
                    
                    if player.has_reached_new_platform():
                        ge[x].fitness += 100  

                    if player.playerRect.y < player.highest_y:
                        ge[x].fitness += (player.highest_y - player.playerRect.y) * 0.5

                    ge[x].fitness -= player.time_on_current_platform * 0.1  

                    player.lastY = player.playerRect.y
                # else:
                #     ge[x].fitness -= height_diff * 0.1
                    
                if player.isClimbing:
                    ge[x].fitness += 5
                
                score_diff = player.score - player.lastScore
                #print("score_diff = ", score_diff)
                ge[x].fitness += score_diff * 10 
                player.lastScore = player.score #score already includes reward for pauline and jumping over barrels
                
                ge[x].fitness += 0.1 #just for survival


                if ge[x].fitness > best_fitness:
                    best_fitness = ge[x].fitness
                    best_genome = ge[x]

        if len(players) == 0:
            break
        
        if framesSinceSwitch < 16:
            screen.blit(fire_barrel1, (barrelX, barrelY))
        else:
            screen.blit(fire_barrel2, (barrelX, barrelY))
        
        framesSinceSwitch = (framesSinceSwitch + 1) % 32 

        fitness_text = font.render(f'Best Fitness: {int(best_fitness)}', True, (255, 255, 255))
        screen.blit(fitness_text, (100, 10))

        pygame.display.flip()
        dt = clock.tick(30) / 1000

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

    def eval_genomes_wrapper(genomes, config):
        fitnesses = eval_genomes(genomes, config)
        
        fitness_scores = [genome.fitness for _, genome in genomes]
        best_fitness = max(fitness_scores) if fitness_scores else 0
        avg_fitness = sum(fitness_scores) / len(fitness_scores) if fitness_scores else 0
        species_count = len(population.species.species)
        
        generation = population.generation
        log_generation(generation, best_fitness, avg_fitness, species_count)
        
        return fitnesses

    winner = population.run(eval_genomes_wrapper, 2)  # number of generations
    
    visualize_net(winner, config)
    with open('winner.pkl', 'wb') as f:
        pickle.dump(winner, f)
    pygame.quit()

    return winner, stats

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
    #main()