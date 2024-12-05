# Memory Models

## Overview
Our memory model implements the canonical evaluation system defined in `ella_schema.yaml`, using precise archetype metrics to evaluate and form memories. Each memory undergoes evaluation across all archetype dimensions with specific metrics, annotations, and justifications.

## Memory System Flow

### 1. Memory Formation
- **Input Processing**: User interactions are captured through Lain interface
- **Context Retrieval**: EllaContext fetches relevant memories:
  - Semantically related memories
  - Archetype metric related memories
  - Core memories (passed verbatim)
  - Long-term memories (fully included)

### 2. Memory Evaluation
- **Comprehensive Analysis**: EllaEvaluator processes each interaction
- **Metric Assessment**: Each archetype evaluates based on specific metrics
- **Priority Assignment**: Memory priority calculated from archetype scores
- **Relationship Mapping**: New memory connections established

### 3. Memory Maintenance
- **Clustering**: Affinity propagation for memory organization
- **Priority Updates**: Dynamic score adjustments
- **Decay Management**: Time-based memory importance
- **Graph Optimization**: Relationship network maintenance

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

#### Ella-O (Ontological)
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

#### Ella-D (Deception)
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

#### Ella-X (Uncensored)
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

#### Ella-H (Historical)
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

#### Ella-R (Research)
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

#### Ella-A (Analytical)
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

#### Ella-F (Fear)
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
    memory.evaluations.ella_uncensored = await evaluate_uncensored(content, context)
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
