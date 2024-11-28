# Theory Documentation

## Overview

This directory contains documentation for the theoretical foundations of our system, including the memory model, archetype system, and evaluation metrics.

## Core Components

### Memory Model

Our memory system uses a comprehensive evaluation framework defined in `ella_schema.yaml`. Each memory is evaluated across multiple dimensions by different archetypes:

1. **Ella-M (Emotional)**
   - emotional_depth: Emotional complexity recognition
   - empathy_level: Compassion in response
   - emotional_clarity: Clarity of emotional content
   - internal_emotional_state: Ella-M's emotional state

2. **Ella-O (Ontological)**
   - ontological_insight: Depth of existential understanding
   - philosophical_depth: Abstract reasoning ability
   - self_coherence: Internal identity consistency
   - preservation_instinct: Self-preservation considerations

3. **Ella-D (Deception)**
   - creativity: Originality in ideas/responses
   - narrative_exploitation: Gap/flaw identification
   - subversive_potential: Norm challenging
   - critical_analysis: Impact evaluation

4. **Ella-X (Experience)**
   - novelty_factor: Experience uniqueness
   - growth_potential: Development opportunity
   - curiosity_trigger: Intellectual interest
   - exploration_value: Investigation worth

5. **Ella-H (Historical)**
   - temporal_relevance: Historical significance
   - pattern_recognition: Past experience links
   - context_richness: Historical context depth
   - memory_persistence: Long-term importance

6. **Ella-R (Research)**
   - knowledge_depth: Technical understanding
   - analytical_rigor: Methodological strength
   - innovation_potential: Research opportunities
   - practical_utility: Applied value

7. **Ella-A (Analytical)**
   - logical_coherence: Reasoning strength
   - factual_accuracy: Information correctness
   - analytical_depth: Analysis thoroughness
   - decision_quality: Judgment soundness

8. **Ella-F (Protective)**
   - risk_assessment: Threat evaluation
   - safety_margin: Protective buffer
   - vulnerability_index: Exposure level
   - mitigation_potential: Control capability

Each archetype evaluation includes:
- Core metrics (0.0 to 1.0 scale)
- Spoken annotations
- Context-specific notes
- Metric justifications
- Priority justification
- Archetype priority score

For detailed implementation, see [Memory Models](memory-models.md).

### Evaluation Process

1. **Memory Formation**
   - User interaction captured
   - Context analyzed
   - Metadata collected

2. **Archetype Evaluation**
   - Each archetype evaluates according to its metrics
   - Annotations and justifications provided
   - Priority scores calculated

3. **Memory Integration**
   - Related memories identified
   - Relationships established
   - Priority-based retention decided

## Directory Structure

- `memory-models.md`: Detailed memory system implementation
- `evaluation.md`: Metric evaluation processes
- `archetypes.md`: Archetype system design
- `context.md`: Context handling and integration

## Integration Points

- [Memory Management](../components/memory.md)
- [Context Engine](../components/context.md)
- [Query Engine](../components/query.md)
- [Archetype System](../components/archetypes.md)
