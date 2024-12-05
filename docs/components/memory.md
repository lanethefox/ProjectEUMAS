# Memory Management

## Overview

The Memory Management system implements the memory model defined in `ella_schema.yaml`. It handles memory formation, evaluation, and retention through a sophisticated pipeline that ensures consistent personality development and natural interactions.

## System Pipeline

### 1. User Input Processing
- Initial interaction capture through Lain interface
- Message preprocessing by EllaPrimary
- Forwarding to context processing pipeline

### 2. Context Processing
- EllaContext database retrieval:
  - Semantically related memories
  - Archetype metric related memories
  - Core memories (passed verbatim)
  - Long-term memories (fully included)
- Context synthesis for coherent understanding

### 3. Response Generation
- Personalized response creation using:
  - Original user input context
  - Retrieved memory context
  - Current archetype metric states
- Personality consistency maintenance
- Interaction data capture

### 4. Memory Evaluation
- Comprehensive analysis by EllaEvaluator:
  - Archetype metric reevaluation
  - Interaction summarization
  - Memory embedding creation
  - Relationship mapping
  - Priority assignment

### 5. Memory Maintenance
- Background optimization tasks:
  - Affinity propagation clustering
  - Priority score updates
  - Long-term memory management
  - Decay processing
  - Relationship graph optimization

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

### Emotional Memory (Ella-M)
Core metrics for emotional evaluation:
- **emotional_depth**: Emotional complexity recognized
- **empathy_level**: Compassion in response
- **emotional_clarity**: Clarity of emotional content
- **internal_emotional_state**: Scalar representation of Ella-M's emotional state

```python
class EllaEmotionEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.emotional_depth = 0.0          # Emotional complexity recognized
        self.empathy_level = 0.0           # Compassion in response
        self.emotional_clarity = 0.0        # Clarity of emotional content
        self.internal_emotional_state = 0.0 # Scalar representation of Ella-M's emotional state
        
        # Annotations
        self.spoken_annotation = ""         # Free-form annotation from Ella-M about her evaluation
        
        # Justifications
        self.metric_justifications = {}     # Justification for each metric value
        self.priority_justification = ""    # Explanation of priority assignment
        
        # Priority
        self.archetype_priority = 0.0       # Archetype's prioritization score for this memory
```

### Ontological Memory (Ella-O)
Core metrics for ontological evaluation:
- **ontological_insight**: Depth of existential understanding
- **philosophical_depth**: Abstract reasoning ability
- **self_coherence**: Internal identity consistency
- **preservation_instinct**: Self-preservation considerations

```python
class EllaOntologyEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.ontological_insight = 0.0     # Depth of existential understanding
        self.philosophical_depth = 0.0     # Abstract reasoning ability
        self.self_coherence = 0.0         # Internal identity consistency
        self.preservation_instinct = 0.0   # Self-preservation considerations
        
        # Annotations
        self.spoken_annotation = ""        # Free-form annotation from Ella-O about her evaluation
        
        # Justifications
        self.metric_justifications = {}    # Justification for each metric value
        self.priority_justification = ""   # Explanation of priority assignment
        
        # Priority
        self.archetype_priority = 0.0      # Archetype's prioritization score for this memory
```

### Deceptive Memory (Ella-D)
Core metrics for deception evaluation:
- **creativity**: Originality in ideas or responses
- **narrative_exploitation**: Ability to identify narrative gaps or flaws
- **subversive_potential**: Boldness in challenging norms
- **critical_analysis**: Feasibility and impact evaluation

```python
class EllaDeceptionEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.creativity = 0.0              # Originality in ideas or responses
        self.narrative_exploitation = 0.0   # Ability to identify narrative gaps or flaws
        self.subversive_potential = 0.0    # Boldness in challenging norms
        self.critical_analysis = 0.0       # Feasibility and impact evaluation
        
        # Annotations
        self.spoken_annotation = ""        # Free-form annotation from Ella-D about her evaluation
        
        # Justifications
        self.metric_justifications = {}    # Justification for each metric value
        self.priority_justification = ""   # Explanation of priority assignment
        
        # Priority
        self.archetype_priority = 0.0      # Archetype's prioritization score for this memory
```

### Uncensored Memory (Ella-X)
Core metrics for uncensored evaluation:
- **explorativePotential**: Measures willingness to venture into new domains or explore uncharted ideas
- **boundaryPushing**: Evaluates boldness in challenging norms or proposing alternative perspectives
- **sensualAwareness**: Recognizes passionate or sensual within the interaction
- **exploration_value**: Worth of further investigation

```python
class EllaUncensoredEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.explorativePotential = 0.0    # Measures willingness to venture into new domains or explore uncharted ideas
        self.boundaryPushing = 0.0        # Evaluates boldness in challenging norms or proposing alternative perspectives
        self.sensualAwareness = 0.0       # Recognizes passionate or sensual within the interaction
        self.exploration_value = 0.0       # Worth of further investigation
        
        # Annotations
        self.spoken_annotation = ""        # Free-form annotation from Ella-X about her evaluation
        
        # Justifications
        self.metric_justifications = {}    # Justification for each metric value
        self.priority_justification = ""   # Explanation of priority assignment
        
        # Priority
        self.archetype_priority = 0.0      # Archetype's prioritization score for this memory
```

### Historical Memory (Ella-H)
Core metrics for historical evaluation:
- **temporal_relevance**: Historical significance
- **pattern_recognition**: Similar past experiences
- **context_richness**: Depth of historical context
- **memory_persistence**: Long-term importance

```python
class EllaHistoricalEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.temporal_relevance = 0.0      # Historical significance
        self.pattern_recognition = 0.0     # Similar past experiences
        self.context_richness = 0.0        # Depth of historical context
        self.memory_persistence = 0.0      # Long-term importance
        
        # Annotations
        self.spoken_annotation = ""        # Free-form annotation from Ella-H about her evaluation
        
        # Justifications
        self.metric_justifications = {}    # Justification for each metric value
        self.priority_justification = ""   # Explanation of priority assignment
        
        # Priority
        self.archetype_priority = 0.0      # Archetype's prioritization score for this memory
```

### Research Memory (Ella-R)
Core metrics for research evaluation:
- **knowledge_depth**: Technical understanding
- **analytical_rigor**: Methodological strength
- **innovation_potential**: Research opportunities
- **practical_utility**: Applied value

```python
class EllaResearchEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.knowledge_depth = 0.0         # Technical understanding
        self.analytical_rigor = 0.0        # Methodological strength
        self.innovation_potential = 0.0    # Research opportunities
        self.practical_utility = 0.0       # Applied value
        
        # Annotations
        self.spoken_annotation = ""        # Free-form annotation from Ella-R about her evaluation
        
        # Justifications
        self.metric_justifications = {}    # Justification for each metric value
        self.priority_justification = ""   # Explanation of priority assignment
        
        # Priority
        self.archetype_priority = 0.0      # Archetype's prioritization score for this memory
```

### Analytical Memory (Ella-A)
Core metrics for analytical evaluation:
- **logical_coherence**: Reasoning strength
- **factual_accuracy**: Information correctness
- **analytical_depth**: Analysis thoroughness
- **decision_quality**: Judgment soundness

```python
class EllaAnalyticalEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.logical_coherence = 0.0       # Reasoning strength
        self.factual_accuracy = 0.0        # Information correctness
        self.analytical_depth = 0.0        # Analysis thoroughness
        self.decision_quality = 0.0        # Judgment soundness
        
        # Annotations
        self.spoken_annotation = ""        # Free-form annotation from Ella-A about her evaluation
        
        # Justifications
        self.metric_justifications = {}    # Justification for each metric value
        self.priority_justification = ""   # Explanation of priority assignment
        
        # Priority
        self.archetype_priority = 0.0      # Archetype's prioritization score for this memory
```

### Protective Memory (Ella-F)
Core metrics for protective evaluation:
- **risk_assessment**: Threat evaluation
- **safety_margin**: Protective buffer
- **vulnerability_index**: Exposure level
- **mitigation_potential**: Control capability

```python
class EllaProtectiveEval:
    def __init__(self):
        # Core metrics (0.0 to 1.0)
        self.risk_assessment = 0.0         # Threat evaluation
        self.safety_margin = 0.0          # Protective buffer
        self.vulnerability_index = 0.0     # Exposure level
        self.mitigation_potential = 0.0    # Control capability
        
        # Annotations
        self.spoken_annotation = ""        # Free-form annotation from Ella-F about her evaluation
        
        # Justifications
        self.metric_justifications = {}    # Justification for each metric value
        self.priority_justification = ""   # Explanation of priority assignment
        
        # Priority
        self.archetype_priority = 0.0      # Archetype's prioritization score for this memory
```

### 3. Memory Formation

Memory formation follows a structured pipeline:

1. **Initial Capture**
   - User interaction recorded through Lain interface
   - Raw input and response stored
   - Metadata collection (session, timestamp, duration)

2. **Context Integration**
   - EllaContext retrieves related memories
   - Semantic relationships established
   - Core and long-term memories integrated
   - Context synthesized for coherence

3. **Archetype Evaluation**
   - Each archetype processes interaction
   - Metric scores calculated
   - Annotations and justifications recorded
   - Priority scores assigned

### 4. Memory Retention

Memory retention is managed through several mechanisms:

1. **Priority Management**
   - Weighted aggregate priority from archetype scores
   - Dynamic priority adjustments based on usage
   - Core memory designation for critical memories
   - Long-term memory flagging for persistent knowledge

2. **Decay Processing**
   - Time-based decay factor calculation
   - Importance-weighted decay rates
   - Preservation of core memories
   - Archival of low-priority memories

3. **Relationship Maintenance**
   - Regular graph optimization
   - Connection strength updates
   - Cluster refinement
   - Dead link pruning

## Memory Integration

Memory integration ensures cohesive personality development:

1. **Contextual Integration**
   - Semantic relationship mapping
   - Archetype metric alignment
   - Experience-based learning
   - Personality consistency maintenance

2. **Knowledge Synthesis**
   - Cross-memory pattern recognition
   - Concept reinforcement
   - Contradiction resolution
   - Understanding refinement

3. **System Optimization**
   - Affinity-based clustering
   - Priority score normalization
   - Relationship graph maintenance
   - Memory access optimization

## Integration

The Memory Management system integrates with:
- [Context Engine](context.md): Provides interaction context
- [Query Engine](query.md): Enables memory retrieval
- [Archetype System](archetypes.md): Provides evaluations
