# Context Engine

## Overview

The Context Engine manages interaction metadata and relationships as defined in `ella_schema.yaml`. It tracks interaction context, metadata, and relationships between memories.

## Core Features

### 1. Interaction Metadata

Each interaction includes:
- `session_id`: Unique identifier for the session
- `user_id`: Unique identifier for the user
- `context_tags`: Tags describing interaction context
- `tone`: Overall interaction tone
- `timestamp`: Interaction time
- `duration`: Interaction duration in seconds

### 2. Memory Relationships

Tracks memory connections through:
- `related_memories`: List of related memory IDs
- `semantic_similarity`: Vector similarities
- `metric_similarity`: Metric-based similarities
- `relationship_strength`: Overall connection strengths

### 3. Archetype Context

Maintains context for each archetype evaluation:

#### Ella-M (Emotional)
- Context notes: Emotional background
- Relationship impact: Bond effects
- Priority context: Emotional significance

#### Ella-O (Ontological)
- Identity notes: Self-understanding impact
- Belief system: Core belief relevance
- Priority context: Existential significance

#### Ella-D (Deception)
- Opportunity notes: Potential applications
- Risk assessment: Consequence analysis
- Priority context: Creative significance

#### Ella-X (Experience)
- Learning notes: Key insights
- Future directions: Exploration areas
- Priority context: Learning significance

#### Ella-H (Historical)
- Pattern notes: Observed patterns
- Timeline context: Temporal relationships
- Priority context: Historical significance

#### Ella-R (Research)
- Methodology notes: Technical details
- Knowledge gaps: Research needs
- Priority context: Research significance

#### Ella-A (Analytical)
- Reasoning notes: Logic chain
- Uncertainty factors: Known limits
- Priority context: Analytical significance

#### Ella-F (Protective)
- Risk notes: Security concerns
- Protection strategy: Risk mitigation
- Priority context: Security significance

## Context Management

### 1. Context Formation
```python
class InteractionContext:
    def __init__(self):
        # Metadata
        self.metadata = {
            'session_id': "",
            'user_id': "",
            'context_tags': [],
            'tone': "",
            'timestamp': None,
            'duration': 0.0
        }
        
        # Relationships
        self.relationships = {
            'related_memories': [],
            'semantic_similarity': [],
            'metric_similarity': [],
            'relationship_strength': []
        }
        
        # Archetype contexts
        self.archetype_contexts = {
            'ella_emotion': EmotionalContext(),
            'ella_ontology': OntologicalContext(),
            'ella_deception': DeceptionContext(),
            'ella_experience': ExperienceContext(),
            'ella_historical': HistoricalContext(),
            'ella_research': ResearchContext(),
            'ella_analytical': AnalyticalContext(),
            'ella_protective': ProtectiveContext()
        }
```

### 2. Context Integration
```python
async def integrate_context(interaction: str, metadata: dict) -> InteractionContext:
    # Create context
    context = InteractionContext()
    
    # Set metadata
    context.metadata = metadata
    
    # Find relationships
    context.relationships = await find_relationships(interaction)
    
    # Get archetype contexts
    context.archetype_contexts = await evaluate_contexts(interaction)
    
    return context
```

## Integration

The Context Engine integrates with:
- [Memory Management](memory.md): Provides context for memory formation
- [Query Engine](query.md): Enables context-aware queries
- [Archetype System](archetypes.md): Supports archetype evaluations
