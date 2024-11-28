# Memory Management

## Overview

The Memory Management system implements the memory model defined in `ella_schema.yaml`. It handles memory formation, evaluation, and retention based on comprehensive archetype metrics.

## Core Features

### 1. Memory Structure

Each memory contains:

```python
class Memory:
    def __init__(self):
        # Core interaction data
        self.user_prompt = ""           # User's input/query
        self.agent_reply = ""           # System's response
        self.memory_priority = 0.0      # Weighted priority
        self.summary = ""               # Context summary
        self.long_term_flag = False     # Long-term retention
        self.time_decay_factor = 0.0    # Memory decay rate
        
        # Metadata
        self.metadata = {
            'session_id': "",           # Session identifier
            'user_id': "",              # User identifier
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
```

### 2. Archetype Evaluations

Each memory undergoes evaluation by all archetypes:

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
        self.ontological_insight = 0.0      # Existential understanding
        self.philosophical_depth = 0.0      # Abstract reasoning
        self.self_coherence = 0.0          # Identity consistency
        self.preservation_instinct = 0.0    # Self-preservation
        
        # Annotations
        self.spoken_annotation = ""         # Free-form evaluation
        self.identity_notes = ""            # Impact on identity
        self.belief_system = ""             # Core beliefs impact
        
        # Justifications
        self.metric_justifications = {}     # Per-metric reasoning
        self.priority_justification = ""    # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0       # Memory importance
```

#### Ella-D (Deception)
```python
class EllaDeceptionEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.creativity = 0.0               # Idea originality
        self.narrative_exploitation = 0.0   # Gap identification
        self.subversive_potential = 0.0     # Norm challenging
        self.critical_analysis = 0.0        # Impact evaluation
        
        # Annotations
        self.spoken_annotation = ""         # Free-form evaluation
        self.opportunity_notes = ""         # Potential applications
        self.risk_assessment = ""           # Consequence analysis
        
        # Justifications
        self.metric_justifications = {}     # Per-metric reasoning
        self.priority_justification = ""    # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0       # Memory importance
```

#### Ella-X (Experience)
```python
class EllaExperienceEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.novelty_factor = 0.0          # Experience uniqueness
        self.growth_potential = 0.0        # Development opportunity
        self.curiosity_trigger = 0.0       # Intellectual interest
        self.exploration_value = 0.0       # Investigation worth
        
        # Annotations
        self.spoken_annotation = ""         # Free-form evaluation
        self.learning_notes = ""            # Key insights
        self.future_directions = ""         # Areas to explore
        
        # Justifications
        self.metric_justifications = {}     # Per-metric reasoning
        self.priority_justification = ""    # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0       # Memory importance
```

#### Ella-H (Historical)
```python
class EllaHistoricalEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.temporal_relevance = 0.0       # Historical significance
        self.pattern_recognition = 0.0      # Past experience patterns
        self.context_richness = 0.0        # Historical context depth
        self.memory_persistence = 0.0       # Long-term importance
        
        # Annotations
        self.spoken_annotation = ""         # Free-form evaluation
        self.pattern_notes = ""             # Observed patterns
        self.timeline_context = ""          # Temporal relationships
        
        # Justifications
        self.metric_justifications = {}     # Per-metric reasoning
        self.priority_justification = ""    # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0       # Memory importance
```

#### Ella-R (Research)
```python
class EllaResearchEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.knowledge_depth = 0.0          # Technical understanding
        self.analytical_rigor = 0.0         # Methodological strength
        self.innovation_potential = 0.0     # Research opportunities
        self.practical_utility = 0.0        # Applied value
        
        # Annotations
        self.spoken_annotation = ""         # Free-form evaluation
        self.methodology_notes = ""         # Technical details
        self.knowledge_gaps = ""            # Areas for research
        
        # Justifications
        self.metric_justifications = {}     # Per-metric reasoning
        self.priority_justification = ""    # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0       # Memory importance
```

#### Ella-A (Analytical)
```python
class EllaAnalyticalEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.logical_coherence = 0.0        # Reasoning strength
        self.factual_accuracy = 0.0         # Information correctness
        self.analytical_depth = 0.0         # Analysis thoroughness
        self.decision_quality = 0.0         # Judgment soundness
        
        # Annotations
        self.spoken_annotation = ""         # Free-form evaluation
        self.reasoning_notes = ""           # Logic chain
        self.uncertainty_factors = ""       # Known limitations
        
        # Justifications
        self.metric_justifications = {}     # Per-metric reasoning
        self.priority_justification = ""    # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0       # Memory importance
```

#### Ella-F (Protective)
```python
class EllaProtectiveEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.risk_assessment = 0.0          # Threat evaluation
        self.safety_margin = 0.0            # Protective buffer
        self.vulnerability_index = 0.0      # Exposure level
        self.mitigation_potential = 0.0     # Control capability
        
        # Annotations
        self.spoken_annotation = ""         # Free-form evaluation
        self.risk_notes = ""                # Specific concerns
        self.protection_strategy = ""       # Mitigation approach
        
        # Justifications
        self.metric_justifications = {}     # Per-metric reasoning
        self.priority_justification = ""    # Priority explanation
        
        # Priority
        self.archetype_priority = 0.0       # Memory importance
```

### 3. Memory Formation

```python
async def form_memory(interaction: str, context: dict) -> Memory:
    # Create memory
    memory = Memory()
    memory.user_prompt = interaction
    
    # Set metadata
    memory.metadata = context.get('metadata', {})
    
    # Get archetype evaluations
    evaluations = await evaluate_archetypes(interaction, context)
    memory.evaluations = evaluations
    
    # Calculate priority
    memory.memory_priority = calculate_priority(evaluations)
    
    # Set relationships
    memory.relationships = find_relationships(memory)
    
    # Set retention flag
    memory.long_term_flag = should_retain(memory)
    
    return memory
```

### 4. Memory Retention

```python
def should_retain(memory: Memory) -> bool:
    # Check overall priority
    if memory.memory_priority > PRIORITY_THRESHOLD:
        return True
    
    # Check individual archetype priorities
    for eval in memory.evaluations:
        if eval.archetype_priority > ARCHETYPE_THRESHOLD:
            return True
    
    # Check relationship strength
    if max(memory.relationships['relationship_strength']) > RELATIONSHIP_THRESHOLD:
        return True
    
    return False
```

## Memory Integration

### 1. Relationship Management
```python
async def find_relationships(memory: Memory) -> dict:
    relationships = {
        'related_memories': [],
        'semantic_similarity': [],
        'metric_similarity': [],
        'relationship_strength': []
    }
    
    # Find related memories
    related = await search_memories(memory)
    
    for rel in related:
        # Calculate similarities
        semantic_sim = calculate_semantic_similarity(memory, rel)
        metric_sim = calculate_metric_similarity(memory, rel)
        strength = calculate_relationship_strength(semantic_sim, metric_sim)
        
        # Add to relationships
        relationships['related_memories'].append(rel.id)
        relationships['semantic_similarity'].append(semantic_sim)
        relationships['metric_similarity'].append(metric_sim)
        relationships['relationship_strength'].append(strength)
    
    return relationships
```

### 2. Memory Network
```python
class MemoryNetwork:
    def __init__(self):
        self.memories = []
        self.relationships = {}
    
    async def add_memory(self, memory: Memory):
        # Add memory
        self.memories.append(memory)
        
        # Update relationships
        self.relationships[memory.id] = memory.relationships
        
        # Update existing relationships
        for existing in self.memories[:-1]:
            if memory.id in existing.relationships['related_memories']:
                self.relationships[existing.id] = existing.relationships
```

## Integration

The Memory Management system integrates with:
- [Context Engine](context.md): Provides interaction context
- [Query Engine](query.md): Enables memory retrieval
- [Archetype System](archetypes.md): Provides evaluations
