import random
import uuid
from typing import List

from snackTraveler.utils.data_models import TravelerGenome, SourceBias
from snackTraveler.executor.traveler import Traveler
from snackTraveler.map_elites.elite_map import EliteMap
from snackTraveler.bandit.thompson_sampling import BanditAllocator
from snackTraveler.services.handlers import (
    evaluation_and_map_management_handler,
    generation_scheduler_handler,
    bandit_allocator_handler
)
from snackTraveler.evaluation.fitness import non_dominated_sort, calculate_crowding_distance


# --- Simulation Parameters ---
INITIAL_POPULATION_SIZE = 20
NUM_GENERATIONS = 10
NUM_OFFSPRING_PER_GENERATION = 10
MAP_RESOLUTION = 10
NUM_BANDIT_RUNS = 5


def create_random_genome() -> TravelerGenome:
    """Helper function to create a single random genome."""
    return TravelerGenome(
        genome_id=str(uuid.uuid4()),
        query_diversity=random.random(),
        query_template_id=random.choice([
            "template_v1_broad", "template_v2_specific", 
            "template_v3_questioning", "template_v4_news_focused"
        ]),
        language_mix=random.random(),
        source_bias=SourceBias(
            academic=random.uniform(-1, 1),
            news=random.uniform(-1, 1),
            official=random.uniform(-1, 1),
            blogs=random.uniform(-1, 1),
        ),
        search_depth=random.choice([1, 2]),
        novelty_weight=random.random()
    )

def main():
    """Main simulation script."""
    print("--- Initializing Simulation ---")
    elite_map = EliteMap(resolution=MAP_RESOLUTION)
    bandit_allocator = BanditAllocator(resolution=MAP_RESOLUTION)
    
    # 1. Create initial population
    population: List[TravelerGenome] = [create_random_genome() for _ in range(INITIAL_POPULATION_SIZE)]
    print(f"Initialized with {len(population)} random travelers.")

    # --- Main Evolutionary Loop (Exploration) ---
    print("\n--- Starting Evolutionary Loop (Exploration Phase) ---")
    for gen in range(NUM_GENERATIONS):
        evaluated_population = []
        for i, genome in enumerate(population):
            # Execute
            traveler = Traveler(genome)
            result = traveler.execute()
            
            # Evaluate (but don't add to map yet)
            evaluated_traveler = evaluation_and_map_management_handler(result, elite_map)
            evaluated_traveler.genome = genome # Replace placeholder with actual genome
            evaluated_population.append(evaluated_traveler)

        # Perform sorting and crowding distance calculation on the whole evaluated population
        fronts = non_dominated_sort(evaluated_population)
        for front in fronts:
            calculate_crowding_distance(front)
            
        # Now, add all evaluated individuals to the map
        updates = 0
        for ind in evaluated_population:
            if elite_map.add_individual(ind):
                updates +=1
        
        print(f"Generation {gen+1}/{NUM_GENERATIONS}: Pop Size={len(population)}, Elite Map Size={len(elite_map)}, Updates={updates}")

        # Create new population for the next generation
        population = generation_scheduler_handler(elite_map, NUM_OFFSPRING_PER_GENERATION)

    print("\n--- Evolutionary Loop Finished ---")
    print(f"Final Elite Map contains {len(elite_map.all_elites)} elites.")

    # --- Bandit-driven Loop (Exploitation) ---
    print("\n--- Starting Bandit Loop (Exploitation Phase) ---")
    for i in range(NUM_BANDIT_RUNS):
        print(f"Bandit Run {i+1}/{NUM_BANDIT_RUNS}")
        
        # 1. Bandit selects a traveler
        genome_to_run = bandit_allocator_handler(bandit_allocator, elite_map)
        print(f"  - Bandit selected genome from niche: {genome_to_run.model_dump(exclude={'genome_id'})}")
        
        # 2. Execute the selected traveler
        traveler = Traveler(genome_to_run)
        result = traveler.execute()
        
        # 3. Evaluate and update map & bandit
        evaluated_traveler = evaluation_and_map_management_handler(
            result, 
            elite_map, 
            bandit_allocator, 
            is_bandit_run=True
        )
        evaluated_traveler.genome = genome_to_run
        
        # Re-apply sorting/crowding to the single individual before adding to map
        evaluated_traveler.rank = 0 
        evaluated_traveler.crowding_distance = float('inf')
        
        if elite_map.add_individual(evaluated_traveler):
             print(f"  - Elite map was updated by bandit run.")
        else:
             print(f"  - Elite map was not updated.")

    print("\n--- Simulation Complete ---")
    
    # Final state
    print(f"\nFinal state of Bandit Allocator arms:")
    for coords, params in bandit_allocator.arms.items():
        print(f"  - Niche {coords}: alpha={params['alpha']}, beta={params['beta']}")

if __name__ == "__main__":
    main()
