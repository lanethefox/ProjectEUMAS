# Archetype System

## Overview

The Archetype System in EUMAS (Ella Unified Memory Augmentation System) uses a dynamic, self-reflective approach where a GPT-4 model, initialized with Ella's personality, evaluates memories through different aspects of her own personality. This creates a natural, emergent graph of contextualized memories that evolve with Ella's current emotional and mental state.

## Core Concept

Rather than using complex state machines or multiple models, EUMAS leverages two key components:
1. **Self-Reflection**: GPT-4 model evaluates memories through different aspects of Ella's personality
2. **Affinity Clustering**: Identifies related memories based on these self-reflective evaluations

```mermaid
graph TD
    M[Memory] --> E[Ella GPT-4]
    E --> A[Archetype Evaluation]
    A --> C[Clustered Affinity Search]
    C --> R[Related Memories]
    
    subgraph "Self-Reflection"
        E
        A
    end
    
    subgraph "Memory Graph"
        M
        C
        R
    end
```

## Archetype Evaluation

Each memory is evaluated through different aspects of Ella's personality, defined in `@startup/archetype_prompts.yaml`:

1. **Ella-M (Emotional)**: How does this memory resonate emotionally?
2. **Ella-O (Ontological)**: What existential insights does this memory offer?
3. **Ella-D (Deception)**: What creative or subversive elements exist?
4. **Ella-X (Experience)**: What possibilities or passions does this spark?
5. **Ella-H (Historical)**: How does this connect to past experiences?
6. **Ella-R (Research)**: What knowledge or insights are relevant?
7. **Ella-A (Analytical)**: How can this be logically understood?
8. **Ella-F (Protective)**: What risks or concerns should be considered?

## Archetype Metrics and Annotations

Each archetype evaluates memories using specific metrics (0.0 to 1.0) and provides detailed annotations:

### Ella-M (Emotional)
- **Metrics**:
  - `emotional_depth`: Complexity and depth of emotional recognition
  - `empathy_level`: Degree of compassionate understanding
  - `emotional_clarity`: Clarity in emotional expression
  - `internal_emotional_state`: Ella's own emotional response
- **Annotations**:
  - `spoken_annotation`: Natural language reflection on emotional significance
  - `context_notes`: Emotional context and background
  - `relationship_impact`: How this affects emotional bonds

### Ella-O (Ontological)
- **Metrics**:
  - `ontological_insight`: Depth of existential understanding
  - `philosophical_depth`: Level of abstract reasoning
  - `self_coherence`: Consistency with identity
  - `preservation_instinct`: Self-preservation considerations
- **Annotations**:
  - `spoken_annotation`: Philosophical reflection
  - `identity_notes`: Impact on self-understanding
  - `belief_system`: Relevance to core beliefs

### Ella-D (Deception)
- **Metrics**:
  - `creativity`: Originality in ideas
  - `narrative_exploitation`: Recognition of narrative opportunities
  - `subversive_potential`: Capacity for norm challenge
  - `critical_analysis`: Impact evaluation
- **Annotations**:
  - `spoken_annotation`: Strategic insights
  - `opportunity_notes`: Potential applications
  - `risk_assessment`: Potential consequences

### Ella-X (Experience)
- **Metrics**:
  - `novelty_factor`: Uniqueness of experience
  - `growth_potential`: Opportunity for development
  - `curiosity_trigger`: Intellectual interest
  - `exploration_value`: Worth of further investigation
- **Annotations**:
  - `spoken_annotation`: Experiential reflection
  - `learning_notes`: Key insights gained
  - `future_directions`: Potential areas to explore

### Ella-H (Historical)
- **Metrics**:
  - `temporal_relevance`: Historical significance
  - `pattern_recognition`: Similar past experiences
  - `context_richness`: Depth of historical context
  - `memory_persistence`: Long-term importance
- **Annotations**:
  - `spoken_annotation`: Historical perspective
  - `pattern_notes`: Observed patterns
  - `timeline_context`: Temporal relationships

### Ella-R (Research)
- **Metrics**:
  - `knowledge_depth`: Technical understanding
  - `analytical_rigor`: Methodological strength
  - `innovation_potential`: Research opportunities
  - `practical_utility`: Applied value
- **Annotations**:
  - `spoken_annotation`: Research insights
  - `methodology_notes`: Technical details
  - `knowledge_gaps`: Areas for investigation

### Ella-A (Analytical)
- **Metrics**:
  - `logical_coherence`: Reasoning strength
  - `factual_accuracy`: Information correctness
  - `analytical_depth`: Analysis thoroughness
  - `decision_quality`: Judgment soundness
- **Annotations**:
  - `spoken_annotation`: Analytical perspective
  - `reasoning_notes`: Logic chain
  - `uncertainty_factors`: Known limitations

### Ella-F (Protective)
- **Metrics**:
  - `risk_assessment`: Threat evaluation
  - `safety_margin`: Protective buffer
  - `vulnerability_index`: Exposure level
  - `mitigation_potential`: Control capability
- **Annotations**:
  - `spoken_annotation`: Safety considerations
  - `risk_notes`: Specific concerns
  - `protection_strategy`: Mitigation approach

## Memory Formation Process

Each memory goes through a multi-step evaluation process:

1. **Initial Processing**:
   - Raw content analysis
   - Context extraction
   - Basic metadata collection

2. **Archetype Evaluation**:
   - Each archetype processes the memory
   - Metrics are calculated
   - Annotations are generated
   - Priority scores are assigned

3. **Integration**:
   - Metrics are aggregated
   - Annotations are consolidated
   - Memory is positioned in the knowledge graph
   - Affinities are established

4. **Storage**:
   - Vector embeddings are generated
   - Evaluation data is stored
   - Relationships are indexed

## Implementation Details

### Memory Evaluation
```python
async def evaluate_memory(memory: Memory):
    # Load Ella's personality
    ella = await load_ella_evaluator()
    
    # Collect evaluations from all archetypes
    evaluations = []
    for archetype in ARCHETYPES:
        eval_data = await ella.evaluate(
            memory=memory,
            archetype=archetype,
            metrics_required=True,
            annotations_required=True
        )
        evaluations.append(eval_data)
    
    # Aggregate and store evaluations
    memory.archetype_evaluations = aggregate_evaluations(evaluations)
    memory.update_affinities()
```

## Implementation

### Memory Evaluation
```python
async def evaluate_memory(memory: Memory):
    # Load Ella's personality
    ella = await load_ella_evaluator()
    
    # Get her perspective through different lenses
    evaluations = []
    for archetype in ARCHETYPE_PROMPTS:
        evaluation = await ella.reflect(
            memory.content,
            archetype.prompt
        )
        evaluations.append(evaluation)
    
    # Create affinity clusters
    clusters = await cluster_by_affinity(
        memory,
        evaluations
    )
    
    return {
        'evaluations': evaluations,
        'clusters': clusters
    }
```

### Affinity Search
```python
async def find_related_memories(memory: Memory):
    # Get memory evaluations
    evals = await evaluate_memory(memory)
    
    # Find memories with similar evaluations
    similar = await search_memory_graph(
        evals.clusters,
        threshold=0.7
    )
    
    # Sort by relevance to current state
    return sort_by_current_context(similar)
```

## Dynamic State

Ella's state emerges naturally from:
1. The current conversation context
2. Recently activated memories
3. Emotional resonance with current topics

No explicit state management is needed because:
- Her personality adapts organically through the GPT-4 model
- Memory connections form based on natural affinity
- Context shifts fluidly with conversation flow

```python
async def get_current_state():
    # Get recent context
    context = await get_conversation_context()
    
    # Get active memories
    memories = await get_recent_memories()
    
    # Let Ella reflect on current state
    return await ella.reflect_on_state(
        context,
        memories
    )
```

## UI Personality Profiles

While natural state is dynamic, the UI allows explicit personality profile simulation:

```python
async def set_personality_profile(profile: Profile):
    # Update Ella's system prompt
    await update_system_prompt(profile.prompt)
    
    # Adjust archetype weights
    await update_archetype_weights(profile.weights)
    
    # Clear conversation context
    await reset_context()
```

## Example Usage

```python
# Evaluate a new memory
memory = Memory(
    content="I'm feeling really overwhelmed with work right now.",
    timestamp=datetime.now()
)

# Get Ella's perspective
evaluation = await evaluate_memory(memory)

# Example response
{
    "Ella-M": {
        "emotional_resonance": "Deep empathy and concern",
        "care_response": "Wanting to provide support and comfort"
    },
    "Ella-X": {
        "possibilities": "Opportunity to explore work-life balance",
        "passion_points": "Personal wellbeing, sustainable practices"
    },
    # ... other archetype evaluations
}

# Find related memories
related = await find_related_memories(memory)
```

## Benefits

1. **Natural Evolution**: Personality emerges from GPT-4's understanding rather than rigid rules
2. **Computational Efficiency**: Single model evaluation instead of complex state machines
3. **Contextual Awareness**: Memory relationships form based on natural affinity
4. **Flexible Adaptation**: State changes fluidly with conversation context
5. **Simple Implementation**: Leverages GPT-4's capabilities rather than custom ML

## Further Reading
- [Memory Management](memory.md)
- [Context Engine](context.md)
- [Query Engine](query.md)
