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

    **NOTE:** This is a MOCK implementation. In a real system, this function
    would perform complex analysis of the execution results.
    - Novelty: Compare content embeddings to a historical archive.
    - Coverage: Check for newly covered topics/entities against a knowledge base.
    - Reliability: Score domains against a predefined authority list.
    - Cost: Use actual API calls and execution time from the result.
    - Downstream Value: This would likely be updated asynchronously after
      user interaction, but is mocked here for simulation.
    """
    return Fitness(
        novelty=random.uniform(0, 1),
        coverage=random.uniform(0, 1),
        reliability=random.uniform(0, 1),
        cost=result.api_calls + result.execution_time / 10.0, # Example cost function
        downstream_value=random.uniform(0, 1),
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
