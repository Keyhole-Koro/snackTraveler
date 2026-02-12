import random
from typing import List, Dict
from operator import attrgetter

from snackTraveler.utils.data_models import (
    ExecutionResult,
    Fitness,
    EvaluatedTraveler,
)

def calculate_fitness(result: ExecutionResult) -> Fitness:
    """
    Calculates the multi-objective fitness scores from execution results.

    """
    # Real metrics approximation
    
    # 1. Cost: Actual execution time + API calls
    # Normalize: expect ~10s execution and ~5 calls?
    cost = (result.execution_time / 60.0) + (result.api_calls / 20.0)
    cost = min(1.0, cost)

    # 2. Coverage: Ratio of unique domains found
    from urllib.parse import urlparse
    unique_domains = set()
    for url in result.retrieved_urls:
        try:
            unique_domains.add(urlparse(url).netloc)
        except:
            pass
    # Expecting up to 10 unique domains for high coverage in this short task
    coverage = min(1.0, len(unique_domains) / 10.0)

    # 3. Reliability: (Reusing simple domain scoring for now, similar to features)
    authority_scores = {'ac.jp': 0.9, 'gov': 0.9, 'go.jp': 0.9, 'nikkei.com': 0.8, 'reuters.com': 0.8}
    rel_score = 0
    for d in unique_domains:
        val = 0.5
        for k, v in authority_scores.items():
            if k in d:
                val = v
                break
        rel_score += val
    reliability = (rel_score / len(unique_domains)) if unique_domains else 0.5

    # 4. Novelty: Heuristic - more potential for novelty if we went deep?
    # Or if we found domains NOT in the top authority list?
    novel_domains = 0
    for d in unique_domains:
        is_common = False
        for k in authority_scores.keys():
            if k in d:
                is_common = True
                break
        if not is_common:
            novel_domains += 1
    novelty = min(1.0, novel_domains / 5.0)

    # 5. Downstream Value: Random (simulating user feedback placeholder)
    downstream_value = random.uniform(0.3, 0.9)

    return Fitness(
        novelty=novelty,
        coverage=coverage,
        reliability=reliability,
        cost=cost, 
        downstream_value=downstream_value,
    )


def non_dominated_sort(population: List[EvaluatedTraveler]) -> List[List[EvaluatedTraveler]]:
    """
    Performs non-dominated sorting on a population (NSGA-II algorithm).

    Returns a list of fronts, where each front is a list of individuals.
    Front 0 is the best (non-dominated) front.
    """
    fronts = [[]]
    for individual in population:
        individual.domination_count = 0
        individual.dominated_solutions = []
        for other_individual in population:
            if individual.dominates(other_individual):
                individual.dominated_solutions.append(other_individual)
            elif other_individual.dominates(individual):
                individual.domination_count += 1
        
        if individual.domination_count == 0:
            individual.rank = 0
            fronts[0].append(individual)

    i = 0
    while len(fronts[i]) > 0:
        next_front = []
        for individual in fronts[i]:
            for other_individual in individual.dominated_solutions:
                other_individual.domination_count -= 1
                if other_individual.domination_count == 0:
                    other_individual.rank = i + 1
                    next_front.append(other_individual)
        i += 1
        if next_front:
            fronts.append(next_front)
        else:
            break
            
    # Clean up temporary attributes
    for ind in population:
        del ind.domination_count
        del ind.dominated_solutions

    return fronts


def calculate_crowding_distance(front: List[EvaluatedTraveler]):
    """
    Calculates the crowding distance for each individual in a front (NSGA-II).
    """
    if not front:
        return

    num_objectives = len(Fitness.model_fields)
    front_size = len(front)
    
    for ind in front:
        ind.crowding_distance = 0

    # Note: This assumes all objectives are in the Fitness model.
    # 'cost' is a minimization objective, others are maximization.
    objective_names = list(Fitness.model_fields.keys())

    for name in objective_names:
        # Sort by the current objective
        # For minimization objectives (like 'cost'), we sort ascending.
        # For maximization, we sort descending to use the same logic, or handle it explicitly.
        # Here, we sort ascending and use absolute differences.
        reverse_sort = name != 'cost'
        front.sort(key=lambda x: attrgetter(f"fitness.{name}")(x), reverse=reverse_sort)
        
        # Set boundary points to infinity
        front[0].crowding_distance = float('inf')
        front[-1].crowding_distance = float('inf')

        if front_size > 2:
            min_val = attrgetter(f"fitness.{name}")(front[-1])
            max_val = attrgetter(f"fitness.{name}")(front[0])
            val_range = max_val - min_val
            if val_range == 0:
                continue

            # Add distance from neighbors
            for i in range(1, front_size - 1):
                prev_val = attrgetter(f"fitness.{name}")(front[i+1])
                next_val = attrgetter(f"fitness.{name}")(front[i-1])
                front[i].crowding_distance += (next_val - prev_val) / val_range
