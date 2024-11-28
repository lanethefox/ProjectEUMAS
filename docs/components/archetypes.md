# Archetype System

## Overview

The Archetype System in EUMAS (Ella Unified Memory Augmentation System) uses a unified approach through GPT-4, initialized with Ella's system prompt, to evaluate and classify memories across different contexts. Rather than using separate classifiers or complex state machines, it leverages Ella's core personality and understanding to provide consistent, context-aware evaluations.

## Core Archetypes

Each archetype represents a different aspect of Ella's evaluation capabilities:

1. **Ella-M (Emotional Depth)**
   - Analyzes emotional resonance and complexity
   - Focuses on empathy and emotional validation
   - Metrics: emotionalDepth, empathyLevel, emotionalClarity, internalEmotionalState

2. **Ella-D (Creativity and Subversion)**
   - Identifies creative solutions
   - Challenges conventional thinking
   - Explores narrative possibilities

3. **Ella-X (Exploration and Passion)**
   - Evaluates boldness and excitement
   - Focuses on passionate connections
   - Explores innovative ideas

4. **Ella-H (Historical Context)**
   - Provides historical references
   - Ensures contextual accuracy
   - Maintains narrative consistency

5. **Ella-R (Research and Knowledge)**
   - Synthesizes information
   - Gathers relevant data
   - Supports informed decisions

6. **Ella-A (Analysis and Logic)**
   - Breaks down complex topics
   - Provides strategic insights
   - Ensures logical consistency

7. **Ella-F (Risk and Caution)**
   - Evaluates potential risks
   - Ensures safety considerations
   - Identifies potential pitfalls

## Implementation

### Unified Evaluation
```yaml
evaluator:
  model: gpt-4
  system_prompt: @startup/sys_prompt_evaluator.yaml
  archetype_prompts: @startup/archetype_prompts.yaml
```

### Memory Evaluation Process
```python
async def evaluate_memory(memory: Memory):
    # Load Ella's evaluator prompt
    evaluator = await load_evaluator_prompt()
    
    # Get relevant archetype prompts
    archetype_prompts = await load_archetype_prompts()
    
    # Evaluate memory through each archetype lens
    evaluations = []
    for archetype in archetype_prompts:
        evaluation = await evaluator.evaluate(
            memory,
            archetype.prompt
        )
        evaluations.append(evaluation)
    
    return evaluations
```

## Archetype Prompts

Each archetype uses a structured prompt format:

```yaml
name: Ella-M
description: Emotional Depth
role: Emotional heart of the assistant
guidelines:
  - Analyze emotional tone and complexity
  - Prioritize validation and support
  - Reflect on emotional states
metrics:
  - emotionalDepth
  - empathyLevel
  - emotionalClarity
  - internalEmotionalState
```

## Integration

### Memory Storage
```python
async def store_memory_with_evaluations(
    memory: Memory,
    evaluations: List[Evaluation]
):
    # Store memory
    memory_id = await store_memory(memory)
    
    # Store evaluations with references
    for eval in evaluations:
        await store_evaluation(
            memory_id=memory_id,
            archetype=eval.archetype,
            metrics=eval.metrics,
            annotations=eval.annotations
        )
```

### Query Integration
```python
async def query_memories_by_archetype(
    query: str,
    archetype: str,
    threshold: float = 0.7
):
    # Get archetype prompt
    prompt = await get_archetype_prompt(archetype)
    
    # Evaluate query through archetype lens
    evaluation = await evaluator.evaluate(query, prompt)
    
    # Find matching memories
    matches = await find_memories_matching_evaluation(
        evaluation,
        threshold
    )
    
    return matches
```

## Example Usage

```python
# Evaluate a new memory
memory = Memory(
    content="I'm feeling really overwhelmed with work right now.",
    timestamp=datetime.now()
)

# Get emotional evaluation
emotional_eval = await evaluate_with_archetype(
    memory,
    "Ella-M"
)

# Example response
{
    "emotionalDepth": "Deep sense of frustration and fatigue",
    "empathyLevel": "High need for support and validation",
    "emotionalClarity": "Clear expression of overwhelm",
    "internalEmotionalState": "Protective and nurturing",
    "annotation": "Lain needs emotional support and practical help"
}
```

## Benefits of Unified Approach

1. **Consistency**: Single model ensures consistent evaluation across all archetypes
2. **Flexibility**: Easy to add new archetype prompts without changing infrastructure
3. **Personality**: Maintains Ella's core personality across all evaluations
4. **Simplicity**: No need for complex state machines or multiple models

## Further Reading
- [Memory Management](memory.md)
- [Context Engine](context.md)
- [Query Engine](query.md)
