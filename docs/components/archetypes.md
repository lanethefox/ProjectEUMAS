# Archetype System

## Overview

The archetype system implements the evaluation metrics defined in `ella_schema.yaml`. Each archetype provides a unique perspective for memory evaluation using specific metrics, annotations, and justifications.

## Archetype Definitions

### Ella-M (Emotional)
Evaluates emotional aspects of interactions.

**Core Metrics:**
- `emotional_depth` (0.0-1.0): Measures emotional complexity recognized in the interaction
- `empathy_level` (0.0-1.0): Assesses compassion shown in response
- `emotional_clarity` (0.0-1.0): Evaluates clarity of emotional content
- `internal_emotional_state` (0.0-1.0): Represents Ella-M's emotional state

**Annotations:**
- Spoken annotation: Free-form evaluation notes
- Context notes: Emotional context details
- Relationship impact: Effects on emotional bonds

### Ella-O (Ontological)
Evaluates existential and philosophical aspects.

**Core Metrics:**
- `ontological_insight` (0.0-1.0): Depth of existential understanding
- `philosophical_depth` (0.0-1.0): Abstract reasoning capability
- `self_coherence` (0.0-1.0): Internal identity consistency
- `preservation_instinct` (0.0-1.0): Self-preservation considerations

**Annotations:**
- Spoken annotation: Free-form evaluation notes
- Identity notes: Impact on self-understanding
- Belief system: Relevance to core beliefs

### Ella-D (Deception)
Evaluates creative and subversive aspects.

**Core Metrics:**
- `creativity` (0.0-1.0): Originality in ideas/responses
- `narrative_exploitation` (0.0-1.0): Ability to identify gaps/flaws
- `subversive_potential` (0.0-1.0): Capacity for challenging norms
- `critical_analysis` (0.0-1.0): Impact evaluation capability

**Annotations:**
- Spoken annotation: Free-form evaluation notes
- Opportunity notes: Potential applications
- Risk assessment: Consequence analysis

### Ella-X (Experience)
Evaluates experiential learning aspects.

**Core Metrics:**
- `novelty_factor` (0.0-1.0): Experience uniqueness
- `growth_potential` (0.0-1.0): Development opportunity
- `curiosity_trigger` (0.0-1.0): Intellectual interest level
- `exploration_value` (0.0-1.0): Worth of further investigation

**Annotations:**
- Spoken annotation: Free-form evaluation notes
- Learning notes: Key insights gained
- Future directions: Areas to explore

### Ella-H (Historical)
Evaluates temporal and historical aspects.

**Core Metrics:**
- `temporal_relevance` (0.0-1.0): Historical significance
- `pattern_recognition` (0.0-1.0): Links to past experiences
- `context_richness` (0.0-1.0): Depth of historical context
- `memory_persistence` (0.0-1.0): Long-term importance

**Annotations:**
- Spoken annotation: Free-form evaluation notes
- Pattern notes: Observed patterns
- Timeline context: Temporal relationships

### Ella-R (Research)
Evaluates technical and research aspects.

**Core Metrics:**
- `knowledge_depth` (0.0-1.0): Technical understanding
- `analytical_rigor` (0.0-1.0): Methodological strength
- `innovation_potential` (0.0-1.0): Research opportunities
- `practical_utility` (0.0-1.0): Applied value

**Annotations:**
- Spoken annotation: Free-form evaluation notes
- Methodology notes: Technical details
- Knowledge gaps: Areas needing research

### Ella-A (Analytical)
Evaluates logical and analytical aspects.

**Core Metrics:**
- `logical_coherence` (0.0-1.0): Reasoning strength
- `factual_accuracy` (0.0-1.0): Information correctness
- `analytical_depth` (0.0-1.0): Analysis thoroughness
- `decision_quality` (0.0-1.0): Judgment soundness

**Annotations:**
- Spoken annotation: Free-form evaluation notes
- Reasoning notes: Logic chain
- Uncertainty factors: Known limitations

### Ella-F (Protective)
Evaluates security and protection aspects.

**Core Metrics:**
- `risk_assessment` (0.0-1.0): Threat evaluation
- `safety_margin` (0.0-1.0): Protective buffer
- `vulnerability_index` (0.0-1.0): Exposure level
- `mitigation_potential` (0.0-1.0): Control capability

**Annotations:**
- Spoken annotation: Free-form evaluation notes
- Risk notes: Specific concerns
- Protection strategy: Mitigation approach

## Evaluation Process

Each archetype:
1. Evaluates interaction using core metrics
2. Provides detailed annotations
3. Justifies metric values
4. Assigns priority score
5. Contributes to overall memory priority

## Integration

The archetype system integrates with:
- [Memory Models](../theory/memory-models.md)
- [Context Engine](context.md)
- [Query Engine](query.md)
