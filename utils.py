from settings import *
from bridge import Bridge
from ladder import Ladder
import graphviz
import matplotlib.pyplot as plt
import csv

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

def visualize_net(genome, config, filename="network"):
    dot = graphviz.Digraph(format="png", engine="dot")
    dot.attr(rankdir='TB', size='30,30', ratio='fill')
    
    for node_key in genome.nodes:
        if node_key in config.genome_config.input_keys:
            dot.node(str(node_key), label=str(node_key), color="green", 
                     width="1.5", height="1.5", fontsize="52") 
        elif node_key in config.genome_config.output_keys:
            dot.node(str(node_key), label=str(node_key), color="red", 
                     width="1.5", height="1.5", fontsize="52")
        else:
            dot.node(str(node_key), label=str(node_key), color="blue", 
                     width="1.5", height="1.5", fontsize="52")

    for cg in genome.connections.values():
        if cg.enabled:
            dot.edge(str(cg.key[0]), str(cg.key[1]), label=f"{cg.weight:.2f}")

    dot.attr(dpi='300') 
    dot.render(filename, cleanup=True)
    
    if os.path.exists(f"{filename}.png"):
        print(f"{filename}.png was successfully created.")
    else:
        print(f"Failed to create {filename}.png.")        
        
def log_generation(generation, best_fitness, avg_fitness, species_count):
    log_file = "training_log.csv"
    file_exists = os.path.isfile(log_file)
    
    with open(log_file, 'a', newline='') as csvfile:
        fieldnames = ['Generation', 'Best Fitness', 'Average Fitness', 'Species Count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'Generation': generation,
            'Best Fitness': best_fitness,
            'Average Fitness': avg_fitness,
            'Species Count': species_count
        })
