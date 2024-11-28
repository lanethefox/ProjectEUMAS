# Memory Models

## Overview
Our memory model implements the canonical evaluation system defined in `ella_schema.yaml`, using precise archetype metrics to evaluate and form memories. Each memory undergoes evaluation across all archetype dimensions with specific metrics, annotations, and justifications.

## Core Concepts

### 1. Memory Structure

Each memory contains interaction data and archetype evaluations:

```python
class Memory:
    def __init__(self):
        # Interaction data
        self.user_prompt = ""           # User's input/query
        self.agent_reply = ""           # System's response
        self.memory_priority = 0.0      # Weighted aggregate priority
        self.summary = ""               # Overall context summary
        self.long_term_flag = False     # Long-term retention flag
        self.time_decay_factor = 0.0    # Memory decay rate
        
        # Metadata
        self.metadata = {
            'session_id': "",           # Session identifier
            'user_id': "",              # User identifier
            'context_tags': [],         # Context descriptors
            'tone': "",                 # Interaction tone
            'timestamp': None,          # Interaction time
            'duration': 0.0             # Interaction duration
        }
        
        # Relationships
        self.relationships = {
            'related_memories': [],     # Related memory IDs
            'semantic_similarity': [],   # Vector similarities
            'metric_similarity': [],     # Metric similarities
            'relationship_strength': []  # Connection strengths
        }
        
        # Archetype evaluations
        self.evaluations = ArchetypeEvaluation()
```

### 2. Archetype Evaluations

Each memory is evaluated by all archetypes according to the schema:

#### Ella-M (Emotional)
```python
class EllaEmotionEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.emotional_depth = 0.0          # Emotional complexity
        self.empathy_level = 0.0            # Compassion in response
        self.emotional_clarity = 0.0        # Emotional content clarity
        self.internal_emotional_state = 0.0 # Ella-M's emotional state
        
        # Annotations
        self.spoken_annotation = ""         # Free-form evaluation
        self.context_notes = ""             # Emotional context
        self.relationship_impact = ""       # Effect on bonds
        
        # Justifications
        self.metric_justifications = {}     # Per-metric reasoning
        self.priority_justification = ""    # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0       # Memory importance
```

#### Ella-O (Ontological)
```python
class EllaOntologyEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.ontological_insight = 0.0    # Existential understanding
        self.philosophical_depth = 0.0    # Abstract reasoning
        self.self_coherence = 0.0         # Identity consistency
        self.preservation_instinct = 0.0  # Self-preservation
        
        # Annotations
        self.spoken_annotation = ""       # Free-form evaluation
        self.identity_notes = ""          # Identity impact
        self.belief_system = ""           # Core belief relevance
        
        # Justifications
        self.metric_justifications = {}   # Per-metric reasoning
        self.priority_justification = ""  # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0     # Memory importance
```

#### Ella-D (Deception)
```python
class EllaDeceptionEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.creativity = 0.0             # Idea originality
        self.narrative_exploitation = 0.0  # Gap identification
        self.subversive_potential = 0.0   # Norm challenge
        self.critical_analysis = 0.0      # Impact evaluation
        
        # Annotations
        self.spoken_annotation = ""       # Free-form evaluation
        self.opportunity_notes = ""       # Potential applications
        self.risk_assessment = ""         # Consequence analysis
        
        # Justifications
        self.metric_justifications = {}   # Per-metric reasoning
        self.priority_justification = ""  # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0     # Memory importance
```

#### Ella-X (Experience)
```python
class EllaExperienceEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.novelty_factor = 0.0      # Experience uniqueness
        self.growth_potential = 0.0     # Development opportunity
        self.curiosity_trigger = 0.0    # Intellectual interest
        self.exploration_value = 0.0    # Investigation worth
        
        # Annotations
        self.spoken_annotation = ""     # Free-form evaluation
        self.learning_notes = ""        # Key insights
        self.future_directions = ""     # Exploration areas
        
        # Justifications
        self.metric_justifications = {} # Per-metric reasoning
        self.priority_justification = "" # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0   # Memory importance
```

#### Ella-H (Historical)
```python
class EllaHistoricalEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.temporal_relevance = 0.0   # Historical significance
        self.pattern_recognition = 0.0   # Past experience links
        self.context_richness = 0.0      # Historical context
        self.memory_persistence = 0.0     # Long-term value
        
        # Annotations
        self.spoken_annotation = ""      # Free-form evaluation
        self.pattern_notes = ""          # Pattern observations
        self.timeline_context = ""       # Temporal context
        
        # Justifications
        self.metric_justifications = {}  # Per-metric reasoning
        self.priority_justification = "" # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0    # Memory importance
```

#### Ella-R (Research)
```python
class EllaResearchEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.knowledge_depth = 0.0      # Technical grasp
        self.analytical_rigor = 0.0     # Method strength
        self.innovation_potential = 0.0  # Research openings
        self.practical_utility = 0.0     # Applied value
        
        # Annotations
        self.spoken_annotation = ""     # Free-form evaluation
        self.methodology_notes = ""     # Technical details
        self.knowledge_gaps = ""        # Research needs
        
        # Justifications
        self.metric_justifications = {} # Per-metric reasoning
        self.priority_justification = "" # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0   # Memory importance
```

#### Ella-A (Analytical)
```python
class EllaAnalyticalEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.logical_coherence = 0.0    # Reasoning strength
        self.factual_accuracy = 0.0     # Information truth
        self.analytical_depth = 0.0     # Analysis quality
        self.decision_quality = 0.0     # Judgment soundness
        
        # Annotations
        self.spoken_annotation = ""     # Free-form evaluation
        self.reasoning_notes = ""       # Logic chain
        self.uncertainty_factors = ""   # Known limits
        
        # Justifications
        self.metric_justifications = {} # Per-metric reasoning
        self.priority_justification = "" # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0   # Memory importance
```

#### Ella-F (Protective)
```python
class EllaProtectiveEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.risk_assessment = 0.0      # Threat evaluation
        self.safety_margin = 0.0        # Protection buffer
        self.vulnerability_index = 0.0   # Exposure level
        self.mitigation_potential = 0.0  # Control ability
        
        # Annotations
        self.spoken_annotation = ""     # Free-form evaluation
        self.risk_notes = ""           # Specific risks
        self.protection_strategy = ""   # Risk mitigation
        
        # Justifications
        self.metric_justifications = {} # Per-metric reasoning
        self.priority_justification = "" # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0   # Memory importance
```

### 3. Memory Evaluation Process

```python
async def evaluate_memory(content: str, context: dict) -> Memory:
    # Create memory
    memory = Memory()
    memory.user_prompt = content
    
    # Get evaluations from all archetypes
    memory.evaluations.ella_emotion = await evaluate_emotion(content, context)
    memory.evaluations.ella_ontology = await evaluate_ontology(content, context)
    memory.evaluations.ella_deception = await evaluate_deception(content, context)
    memory.evaluations.ella_experience = await evaluate_experience(content, context)
    memory.evaluations.ella_historical = await evaluate_historical(content, context)
    memory.evaluations.ella_research = await evaluate_research(content, context)
    memory.evaluations.ella_analytical = await evaluate_analytical(content, context)
    memory.evaluations.ella_protective = await evaluate_protective(content, context)
    
    # Calculate overall priority
    memory.memory_priority = calculate_priority(memory.evaluations)
    
    # Set metadata and relationships
    memory.metadata = get_metadata(context)
    memory.relationships = find_relationships(memory)
    
    return memory
```

## Integration
- Core component of [Memory Management](../components/memory.md)
- Guides [Context Engine](../components/context.md)
- Informs [Query Engine](../components/query.md)
- Shapes [Archetype System](../components/archetypes.md)
