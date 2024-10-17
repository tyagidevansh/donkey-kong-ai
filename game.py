import math
import pickle
import time
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
        
        #player.gravity(platforms, dt)
        player.update(dt, platforms)
        
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
    
    max_time = 60  # Maximum time for each generation in seconds
    start_time = time.time()

    while time.time() - start_time < max_time and len(players) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        platforms, ladders = drawMap()
        screen.blit(dk, dkPos)
        screen.blit(peach, peachPos)
        screen.blit(barrel_stack, (20, 130))
        
        timeSinceLastSpawn += dt
        
        if timeSinceLastSpawn > (random.randint(40, 80) / 10):
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
     
            inputs = [
                player.playerRect.x / window_width,
                player.playerRect.y / window_height,
                player.isClimbing,
                player.isJumping,
                player.isNearLadder,
                player.closestLadder / window_width
            ]
            
            #2 nearest barrels
            nearest = player.nearestBarrels(barrels)
            for entry in nearest:
                inputs.append(entry[1] / window_width)
                inputs.append(entry[2] / window_height)

            inputs = [int(val) if isinstance(val, bool) else val for val in inputs]

            if len(inputs) != 10:
                print("wrong input count")                

            #print(inputs)
            #convert outputs from NN to a range of 0 to 1
            def sigmoid(x):
                return 1/ (1 + math.exp(-x))
            
            output = nets[x].activate(inputs)
            output = [sigmoid(o) for o in output]
            
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
            player.update(dt, platforms)
            #print("player updated, platform: ", player.platforms_reached)
            
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

        x = 0
        while x < len(players):
            player = players[x]
            height_progress = (player.initial_y - player.highest_y) / window_height
            platform_progress = player.platforms_reached * (10000 / player.playerRect.top) #every small platform, not just after climbing ladders
            barrel_dodge_skill = player.barrels_dodged * 0.5 #too simple maybe
            climbing_skill = player.ladders_climbed * 0.3 #hope it doesnt just stick to the ladder
            survival_bonus = -player.time_alive * 0.1 #to punish standing in the corner or dilly dallying
            
            if player.playerRect.x < 50: #dont go stand in the corner
                ge[x].fitness -= 1000
            
            ge[x].fitness = (
                height_progress  +
                platform_progress +
                barrel_dodge_skill +
                climbing_skill +
                survival_bonus
            )
            
            #running to the left corner a huge problem

            # Bonus for reaching Pauline
            if player.playerRect.left < peachPos[1] + 90 and player.playerRect.bottom <= peachPos[0]:
                ge[x].fitness += 4000
                return  #end the generation immediately on victory

            # Penalty for barrel collision
            if player.checkBarrelCollision(barrels):
                ge[x].fitness -= 500
                players.pop(x)
                nets.pop(x)
                ge.pop(x)
            else:
                for barrel in barrels:
                    if player.playerRect.y < barrel.barrelRect.y and \
                    abs(player.playerRect.x - barrel.barrelRect.x) < 20:
                        player.dodge_barrel()

                if ge[x].fitness > best_fitness:
                    best_fitness = ge[x].fitness
                    best_genome = ge[x]

                x += 1  # Only increment x if no player was removed

        for x, player in enumerate(players):
            ge[x].fitness += player.score

        
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

def copy_genome(genome, new_id):
    """
    Create a complete copy of a genome with a new ID.
    """
    new_genome = neat.DefaultGenome(new_id)
    
    # Copy all attributes from the original genome
    new_genome.nodes = dict(genome.nodes)
    new_genome.connections = dict(genome.connections)
    new_genome.fitness = genome.fitness
    
    return new_genome

def create_population_from_winner(winner_genome, config, pop_size=100):
    new_population = {}
    
    # Create exact copies first
    for i in range(pop_size):
        new_population[i] = copy_genome(winner_genome, i)
    
    # # Then mutate all except the first one
    # for i in range(1, pop_size):    
    #     new_population[i].mutate(config.genome_config)
    
    return new_population

def run(config_path, winner_path=None):
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path
    )
    
    if winner_path:
        # Load the winner genome
        with open(winner_path, 'rb') as f:
            winner_genome = pickle.load(f)
        
        # Verify the winner genome's structure
        print(f"Winner genome nodes: {len(winner_genome.nodes)}")
        print(f"Winner genome connections: {len(winner_genome.connections)}")
        
        # Create initial population from winner
        initial_population = create_population_from_winner(winner_genome, config)
        
        # Verify the copied genome's structure
        first_copy = initial_population[0]
        print(f"First copy nodes: {len(first_copy.nodes)}")
        print(f"First copy connections: {len(first_copy.connections)}")
        
        # Create a new population
        population = neat.Population(config)
        
        # Replace its population with our initial population
        population.population = initial_population
        
        # Force immediate speciation of the population
        population.species.speciate(config, population.population, 0)
    else:
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

    winner = population.run(eval_genomes_wrapper, 200)
    print(winner)
    visualize_net(winner, config)
    with open('winner.pkl', 'wb') as f:
        pickle.dump(winner, f)
    pygame.quit()

    return winner, stats

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    winner_path = os.path.join(local_dir, "winner.pkl")
    run(config_path, winner_path)
    # main()