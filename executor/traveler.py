import random
import time
from snackTraveler.utils.data_models import TravelerGenome, ExecutionResult

class Traveler:
    """
    A mock traveler executor.

    In a real system, this class would interact with LLMs, search APIs,
    and web pages. Here, it just simulates the execution and returns a
    mock result.
    """
    def __init__(self, genome: TravelerGenome):
        self.genome = genome

    def execute(self) -> ExecutionResult:
        """
        Simulates a web exploration task based on the genome.
        """
        start_time = time.time()

        # Simulate API calls based on search depth
        api_calls = 5 * self.genome.search_depth + random.randint(1, 5)

        # Simulate latency
        time.sleep(random.uniform(0.1, 0.5) * self.genome.search_depth)
        
        # Simulate generating URLs based on source bias
        retrieved_urls = self._simulate_url_generation()

        execution_time = time.time() - start_time

        return ExecutionResult(
            genome_id=self.genome.genome_id,
            retrieved_urls=retrieved_urls,
            generated_queries=[f"mock_query_{i}" for i in range(3)],
            log="Mock execution completed successfully.",
            api_calls=api_calls,
            execution_time=execution_time,
        )

    def _simulate_url_generation(self) -> list[str]:
        """Generates fake URLs based on the source_bias in the genome."""
        urls = []
        source_domains = {
            'academic': ['https://arxiv.org/abs/2305.12345', 'https://www.nature.com/articles/s41586-023-06122-2'],
            'news': ['https://www.nikkei.com/article/DGXZQOUC01001_R00C23A5000000/', 'https://www.bbc.com/news/technology-65506729'],
            'official': ['https://www.digital.go.jp/policies/ai/', 'https://openai.com/blog/function-calling-and-other-api-updates'],
            'blogs': ['https://qiita.com/advent-calendar/2023/llm', 'https://zenn.dev/articles/abc123def456']
        }
        
        # Weigh the choices based on bias
        choices = []
        for source, bias in self.genome.source_bias.model_dump().items():
            # Convert bias [-1, 1] to a weight [0, 2]
            weight = int((bias + 1) * 10)
            choices.extend([source] * weight)

        for _ in range(5 * self.genome.search_depth):
            if not choices: continue
            chosen_source = random.choice(choices)
            if source_domains.get(chosen_source):
                urls.append(random.choice(source_domains[chosen_source]))
        
        return list(set(urls))

    def __str__(self) -> str:
        return f"Traveler(genome_id={self.genome.genome_id})"

