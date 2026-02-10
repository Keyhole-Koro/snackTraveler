## Genomes Component (Data Structure)

```mermaid
graph TD
    subgraph TravelerGenome
        A[genome_id: string]
        B[query_diversity: number (0-1)]
        C[query_template_id: string (enum)]
        D[language_mix: number (0-1)]
        E[search_depth: integer (1 or 2)]
        F[novelty_weight: number (0-1)]
        G[source_bias: object]
    end

    subgraph SourceBias
        H[academic: number (-1 to 1)]
        I[news: number (-1 to 1)]
        J[official: number (-1 to 1)]
        K[blogs: number (-1 to 1)]
    end

    TravelerGenome --> G
    G --> SourceBias
```
