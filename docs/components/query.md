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
        
        # Emotional query parameters
        self.emotional_query_params = {
            'emotional_depth': None,   # Emotional complexity recognized
            'empathy_level': None,     # Compassion in response
            'emotional_clarity': None, # Clarity of emotional content
            'internal_emotional_state': None # Scalar representation of Ella-M's emotional state
        }
        
        # Ontological query parameters
        self.ontological_query_params = {
            'ontological_insight': None, # Depth of existential understanding
            'philosophical_depth': None, # Abstract reasoning ability
            'self_coherence': None, # Internal identity consistency
            'preservation_instinct': None # Self-preservation considerations
        }
        
        # Deceptive query parameters
        self.deceptive_query_params = {
            'creativity': None, # Originality in ideas or responses
            'narrative_exploitation': None, # Ability to identify narrative gaps or flaws
            'subversive_potential': None, # Boldness in challenging norms
            'critical_analysis': None # Feasibility and impact evaluation
        }
        
        # Uncensored query parameters
        self.uncensored_query_params = {
            'explorativePotential': None, # Measures willingness to venture into new domains or explore uncharted ideas
            'boundaryPushing': None, # Evaluates boldness in challenging norms or proposing alternative perspectives
            'sensualAwareness': None, # Recognizes passionate or sensual within the interaction
            'exploration_value': None # Worth of further investigation
        }
        
        # Historical query parameters
        self.historical_query_params = {
            'temporal_relevance': None, # Historical significance
            'pattern_recognition': None, # Similar past experiences
            'context_richness': None, # Depth of historical context
            'memory_persistence': None # Long-term importance
        }
        
        # Research query parameters
        self.research_query_params = {
            'knowledge_depth': None, # Technical understanding
            'analytical_rigor': None, # Methodological strength
            'innovation_potential': None, # Research opportunities
            'practical_utility': None # Applied value
        }
        
        # Analytical query parameters
        self.analytical_query_params = {
            'logical_coherence': None, # Reasoning strength
            'factual_accuracy': None, # Information correctness
            'analytical_depth': None, # Analysis thoroughness
            'decision_quality': None # Judgment soundness
        }
        
        # Protective query parameters
        self.protective_query_params = {
            'risk_assessment': None, # Threat evaluation
            'safety_margin': None, # Protective buffer
            'vulnerability_index': None, # Exposure level
            'mitigation_potential': None # Control capability
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

### Query Parameters by Archetype

#### Emotional Query Parameters
- `emotional_depth`: Emotional complexity recognized
- `empathy_level`: Compassion in response
- `emotional_clarity`: Clarity of emotional content
- `internal_emotional_state`: Scalar representation of Ella-M's emotional state

#### Ontological Query Parameters
- `ontological_insight`: Depth of existential understanding
- `philosophical_depth`: Abstract reasoning ability
- `self_coherence`: Internal identity consistency
- `preservation_instinct`: Self-preservation considerations

#### Deceptive Query Parameters
- `creativity`: Originality in ideas or responses
- `narrative_exploitation`: Ability to identify narrative gaps or flaws
- `subversive_potential`: Boldness in challenging norms
- `critical_analysis`: Feasibility and impact evaluation

#### Uncensored Query Parameters
- `explorativePotential`: Measures willingness to venture into new domains or explore uncharted ideas
- `boundaryPushing`: Evaluates boldness in challenging norms or proposing alternative perspectives
- `sensualAwareness`: Recognizes passionate or sensual within the interaction
- `exploration_value`: Worth of further investigation

#### Historical Query Parameters
- `temporal_relevance`: Historical significance
- `pattern_recognition`: Similar past experiences
- `context_richness`: Depth of historical context
- `memory_persistence`: Long-term importance

#### Research Query Parameters
- `knowledge_depth`: Technical understanding
- `analytical_rigor`: Methodological strength
- `innovation_potential`: Research opportunities
- `practical_utility`: Applied value

#### Analytical Query Parameters
- `logical_coherence`: Reasoning strength
- `factual_accuracy`: Information correctness
- `analytical_depth`: Analysis thoroughness
- `decision_quality`: Judgment soundness

#### Protective Query Parameters
- `risk_assessment`: Threat evaluation
- `safety_margin`: Protective buffer
- `vulnerability_index`: Exposure level
- `mitigation_potential`: Control capability
