import random
from snackTraveler.utils.data_models import ExecutionResult, FeatureDescriptors

def calculate_feature_descriptors(result: ExecutionResult) -> FeatureDescriptors:
    """
    Calculates the feature descriptors (niche coordinates) from execution results.

    **NOTE:** This is a MOCK implementation. In a real system, this function
    would perform complex analysis.
    - Concreteness: Analyze query/content for specificity, named entities, etc.
    - Authority: Analyze retrieved domains against a scored list.
    """
    
    # Mock logic for authority:
    # Average authority based on mock domains
    authority_scores = {'ac.jp': 0.9, 'gov': 0.9, 'arxiv.org': 0.8, 'nikkei.com': 0.7, 'wikipedia.org': 0.5, 'qiita.com': 0.3}
    total_score = 0
    count = 0
    for url in result.retrieved_urls:
        domain = url.split('/')[2]
        for key, score in authority_scores.items():
            if key in domain:
                total_score += score
                count += 1
                break
    
    authority = (total_score / count) if count > 0 else 0.5

    return FeatureDescriptors(
        concreteness=random.uniform(0, 1), # Mocked
        authority=authority,
    )
