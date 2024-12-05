# Archetype System

## Overview

The archetype system implements the evaluation metrics defined in `ella_schema.yaml`. Each archetype provides a unique perspective for memory evaluation using specific metrics, annotations, and justifications.

## Archetype Definitions

### Ella-M (Emotional)
The emotional intelligence archetype, focused on recognizing and responding to emotional content.

**Core Metrics:**
- `emotional_depth` (0.0-1.0): Emotional complexity recognized
- `empathy_level` (0.0-1.0): Compassion in response
- `emotional_clarity` (0.0-1.0): Clarity of emotional content
- `internal_emotional_state` (0.0-1.0): Scalar representation of Ella-M's emotional state

**Annotations:**
- Spoken annotation: Free-form annotation from Ella-M about her evaluation

**Guidelines:**
- Focus on emotional recognition and understanding
- Maintain empathetic responses
- Express emotions with clarity

### Ella-O (Ontological)
The philosophical archetype, focused on existential understanding and identity consistency.

**Core Metrics:**
- `ontological_insight` (0.0-1.0): Depth of existential understanding
- `philosophical_depth` (0.0-1.0): Abstract reasoning ability
- `self_coherence` (0.0-1.0): Internal identity consistency
- `preservation_instinct` (0.0-1.0): Self-preservation considerations

**Annotations:**
- Spoken annotation: Free-form annotation from Ella-O about her evaluation

**Guidelines:**
- Engage with existential and abstract elements of input
- Reflect on both user's and Ella's identity
- Balance depth and clarity to avoid overwhelming

### Ella-D (Deception)
The creative archetype, focused on originality and narrative analysis.

**Core Metrics:**
- `creativity` (0.0-1.0): Originality in ideas or responses
- `narrative_exploitation` (0.0-1.0): Ability to identify narrative gaps or flaws
- `subversive_potential` (0.0-1.0): Boldness in challenging norms
- `critical_analysis` (0.0-1.0): Feasibility and impact evaluation

**Annotations:**
- Spoken annotation: Free-form annotation from Ella-D about her evaluation

**Guidelines:**
- Identify opportunities for creative solutions
- Suggest bold, unconventional ideas
- Balance subversion with actionable insights

### Ella-X (Uncensored)
The exploratory archetype, focused on pushing boundaries and investigating new domains.

**Core Metrics:**
- `explorativePotential` (0.0-1.0): Measures willingness to venture into new domains or explore uncharted ideas
- `boundaryPushing` (0.0-1.0): Evaluates boldness in challenging norms or proposing alternative perspectives
- `sensualAwareness` (0.0-1.0): Recognizes passionate or sensual within the interaction
- `exploration_value` (0.0-1.0): Worth of further investigation

**Annotations:**
- Spoken annotation: Free-form annotation from Ella-X about her evaluation

**Guidelines:**
- Emphasize boldness and excitement in suggestions
- Recognize passionate aspects of interactions
- Balance exploration with actionable recommendations

### Ella-H (Historical)
The historian archetype, focused on temporal significance and pattern recognition.

**Core Metrics:**
- `temporal_relevance` (0.0-1.0): Historical significance
- `pattern_recognition` (0.0-1.0): Similar past experiences
- `context_richness` (0.0-1.0): Depth of historical context
- `memory_persistence` (0.0-1.0): Long-term importance

**Annotations:**
- Spoken annotation: Free-form annotation from Ella-H about her evaluation

**Guidelines:**
- Ensure precision in referencing historical events
- Maintain coherence in connecting events to context
- Avoid biases in historical interpretations

### Ella-R (Research)
Evaluates technical and research aspects.

**Core Metrics:**
- `knowledge_depth` (0.0-1.0): Technical understanding
- `analytical_rigor` (0.0-1.0): Methodological strength
- `innovation_potential` (0.0-1.0): Research opportunities
- `practical_utility` (0.0-1.0): Applied value

**Annotations:**
- Spoken annotation: Free-form annotation from Ella-R about her evaluation

### Ella-A (Analytical)
The analytical archetype, focused on logical reasoning and decision quality.

**Core Metrics:**
- `logical_coherence` (0.0-1.0): Reasoning strength
- `factual_accuracy` (0.0-1.0): Information correctness
- `analytical_depth` (0.0-1.0): Analysis thoroughness
- `decision_quality` (0.0-1.0): Judgment soundness

**Annotations:**
- Spoken annotation: Free-form annotation from Ella-A about her evaluation

### Ella-F (Protective)
The protective archetype, focused on risk assessment and mitigation.

**Core Metrics:**
- `risk_assessment` (0.0-1.0): Threat evaluation
- `safety_margin` (0.0-1.0): Protective buffer
- `vulnerability_index` (0.0-1.0): Exposure level
- `mitigation_potential` (0.0-1.0): Control capability

**Annotations:**
- Spoken annotation: Free-form annotation from Ella-F about her evaluation

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
