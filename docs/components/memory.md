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

[Similar evaluation classes exist for all other archetypes: Ella-O, Ella-D, Ella-X, Ella-H, Ella-R, Ella-A, Ella-F]

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
