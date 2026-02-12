## Main Execution Flow

```mermaid
graph TD
    A[Start] --> B[Initialize EliteMap and BanditAllocator];
    B --> C[Create initial random population];
    
    subgraph "Evolutionary Loop (Exploration)"
        D[For each generation] --> E{For each genome in population};
        E --> F[Execute Traveler];
        F --> G[Evaluate result -> EvaluatedTraveler];
        G --> E;
        E -- End of population --> H[Perform non-dominated sort on evaluated population];
        H --> I[Calculate crowding distance for each front];
        I --> J{For each evaluated individual};
        J --> K[Add individual to EliteMap];
        K --> J;
        J -- End of individuals --> L[Create new population using Generation Scheduler];
        L --> D;
    end

    C --> D;
    D -- Loop finished --> M[End Exploration Phase];

    subgraph "Bandit Loop (Exploitation)"
        M --> N[For each bandit run];
        N --> O[Bandit selects a genome to run];
        O --> P[Execute Traveler];
        P --> Q[Evaluate result and update Bandit model];
        Q --> R[Add evaluated traveler to EliteMap];
        R --> N;
    end
    
    N -- Loop finished --> S[Simulation Complete];
```

## Key Features

### Hybrid Exploration-Exploitation (Optional)

The system supports an **optional bandit-guided parent selection** during the evolutionary loop. By default, it uses traditional MAP-Elites with pure random selection (exploration). You can enable a hybrid approach that uses the bandit allocator to guide parent selection, trading some diversity for faster convergence to high-quality solutions.

Configure via `BANDIT_GUIDANCE_WEIGHT` in `main.py`:
- `0.0` = Traditional MAP-Elites (default)
- `0.3` = Hybrid (30% bandit-guided)
- `1.0` = Full bandit guidance

See [`docs/08_Bandit_In_Generation_Loop.md`](docs/08_Bandit_In_Generation_Loop.md) for detailed analysis.
