# Query Engine

## Overview

The Query Engine enables memory retrieval based on the evaluation framework defined in `ella_schema.yaml`. It uses memory relationships, metadata, and archetype evaluations to find relevant memories.

## Core Features

### 1. Query Structure

Each query includes:
```python
class MemoryQuery:
    def __init__(self):
        # Query parameters
        self.query_text = ""          # Search text
        self.context_tags = []        # Required context tags
        self.time_range = None        # Time constraints
        
        # Metadata filters
        self.metadata_filters = {
            'session_id': None,       # Specific session
            'user_id': None,          # Specific user
            'tone': None              # Specific tone
        }
        
        # Relationship parameters
        self.relationship_params = {
            'min_semantic_similarity': 0.0,
            'min_metric_similarity': 0.0,
            'min_relationship_strength': 0.0
        }
        
        # Archetype priorities
        self.archetype_weights = {
            'ella_emotion': 1.0,      # Emotional weight
            'ella_ontology': 1.0,     # Ontological weight
            'ella_deception': 1.0,    # Deception weight
            'ella_experience': 1.0,    # Experience weight
            'ella_historical': 1.0,    # Historical weight
            'ella_research': 1.0,      # Research weight
            'ella_analytical': 1.0,    # Analytical weight
            'ella_protective': 1.0     # Protective weight
        }
```

### 2. Query Processing

```python
async def process_query(query: MemoryQuery) -> List[Memory]:
    # Apply metadata filters
    candidates = filter_by_metadata(query.metadata_filters)
    
    # Apply relationship filters
    candidates = filter_by_relationships(
        candidates,
        query.relationship_params
    )
    
    # Calculate relevance scores
    scored_memories = []
    for memory in candidates:
        # Get weighted archetype scores
        archetype_scores = calculate_archetype_scores(
            memory,
            query.archetype_weights
        )
        
        # Calculate overall score
        relevance = calculate_relevance(
            memory,
            query,
            archetype_scores
        )
        
        scored_memories.append((memory, relevance))
    
    # Sort by relevance
    scored_memories.sort(key=lambda x: x[1], reverse=True)
    
    return [m for m, _ in scored_memories]
```

### 3. Relevance Scoring

```python
def calculate_relevance(
    memory: Memory,
    query: MemoryQuery,
    archetype_scores: dict
) -> float:
    # Get base similarity
    text_similarity = calculate_text_similarity(
        memory.user_prompt,
        query.query_text
    )
    
    # Get relationship strength
    relationship_score = calculate_relationship_score(
        memory.relationships,
        query.relationship_params
    )
    
    # Get weighted archetype score
    weighted_score = sum(
        score * query.archetype_weights[archetype]
        for archetype, score in archetype_scores.items()
    ) / sum(query.archetype_weights.values())
    
    # Combine scores
    return combine_scores(
        text_similarity,
        relationship_score,
        weighted_score
    )
```

### 4. Memory Filtering

```python
def filter_by_metadata(memories: List[Memory], filters: dict) -> List[Memory]:
    filtered = memories
    
    # Apply each filter
    for key, value in filters.items():
        if value is not None:
            filtered = [
                m for m in filtered
                if m.metadata.get(key) == value
            ]
    
    return filtered

def filter_by_relationships(
    memories: List[Memory],
    params: dict
) -> List[Memory]:
    filtered = memories
    
    # Check semantic similarity
    if params['min_semantic_similarity'] > 0:
        filtered = [
            m for m in filtered
            if max(m.relationships['semantic_similarity'])
            >= params['min_semantic_similarity']
        ]
    
    # Check metric similarity
    if params['min_metric_similarity'] > 0:
        filtered = [
            m for m in filtered
            if max(m.relationships['metric_similarity'])
            >= params['min_metric_similarity']
        ]
    
    # Check relationship strength
    if params['min_relationship_strength'] > 0:
        filtered = [
            m for m in filtered
            if max(m.relationships['relationship_strength'])
            >= params['min_relationship_strength']
        ]
    
    return filtered
```

## Integration

The Query Engine integrates with:
- [Memory Management](memory.md): Accesses memory store
- [Context Engine](context.md): Uses context for relevance
- [Archetype System](archetypes.md): Uses archetype evaluations
