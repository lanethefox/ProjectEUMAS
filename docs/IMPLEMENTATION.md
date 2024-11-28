# Implementation Guide

## Overview

This guide explains how to implement the evaluation system defined in `ella_schema.yaml`. The system uses comprehensive archetype evaluations to form and manage memories.

## Core Components

### 1. Memory System

The memory system implements:
- Memory formation and retention
- Archetype evaluations
- Memory relationships
- Priority management

Key files:
- `memory/memory.py`: Memory class and formation
- `memory/evaluation.py`: Archetype evaluations
- `memory/relationships.py`: Memory relationships
- `memory/priority.py`: Priority calculations

### 2. Archetype System

Each archetype provides:
- Core metrics (0.0-1.0 scale)
- Annotations and notes
- Metric justifications
- Priority scores

Archetype implementations:
- `archetypes/ella_emotion.py`: Ella-M (Emotional)
- `archetypes/ella_ontology.py`: Ella-O (Ontological)
- `archetypes/ella_deception.py`: Ella-D (Deception)
- `archetypes/ella_experience.py`: Ella-X (Experience)
- `archetypes/ella_historical.py`: Ella-H (Historical)
- `archetypes/ella_research.py`: Ella-R (Research)
- `archetypes/ella_analytical.py`: Ella-A (Analytical)
- `archetypes/ella_protective.py`: Ella-F (Protective)

### 3. Context Engine

Manages:
- Interaction metadata
- Memory relationships
- Archetype contexts

Key files:
- `context/context.py`: Context management
- `context/metadata.py`: Metadata handling
- `context/relationships.py`: Relationship tracking

### 4. Query Engine

Implements:
- Memory retrieval
- Relevance scoring
- Result filtering

Key files:
- `query/query.py`: Query processing
- `query/relevance.py`: Scoring system
- `query/filters.py`: Memory filtering

## Implementation Steps

### 1. Setup Project

```bash
# Create project structure
mkdir -p eumas/{memory,archetypes,context,query}
touch eumas/__init__.py

# Create component directories
for dir in memory archetypes context query; do
    mkdir -p eumas/$dir
    touch eumas/$dir/__init__.py
done
```

### 2. Implement Memory System

```python
# memory/memory.py
class Memory:
    def __init__(self):
        # Core data
        self.user_prompt = ""
        self.agent_reply = ""
        self.memory_priority = 0.0
        self.summary = ""
        self.long_term_flag = False
        self.time_decay_factor = 0.0
        
        # Metadata
        self.metadata = {
            'session_id': "",
            'user_id': "",
            'context_tags': [],
            'tone': "",
            'timestamp': None,
            'duration': 0.0
        }
        
        # Relationships
        self.relationships = {
            'related_memories': [],
            'semantic_similarity': [],
            'metric_similarity': [],
            'relationship_strength': []
        }
```

### 3. Implement Archetypes

```python
# archetypes/base.py
class BaseArchetype:
    def __init__(self):
        self.metrics = {}
        self.annotations = {}
        self.justifications = {}
        self.priority = 0.0
    
    async def evaluate(self, content: str, context: dict):
        # Implement in subclasses
        raise NotImplementedError

# archetypes/ella_emotion.py
class EllaEmotion(BaseArchetype):
    def __init__(self):
        super().__init__()
        self.metrics = {
            'emotional_depth': 0.0,
            'empathy_level': 0.0,
            'emotional_clarity': 0.0,
            'internal_emotional_state': 0.0
        }
    
    async def evaluate(self, content: str, context: dict):
        # Implement emotional evaluation
        pass
```

### 4. Implement Context Engine

```python
# context/context.py
class InteractionContext:
    def __init__(self):
        # Metadata
        self.metadata = {
            'session_id': "",
            'user_id': "",
            'context_tags': [],
            'tone': "",
            'timestamp': None,
            'duration': 0.0
        }
        
        # Relationships
        self.relationships = {
            'related_memories': [],
            'semantic_similarity': [],
            'metric_similarity': [],
            'relationship_strength': []
        }
        
        # Archetype contexts
        self.archetype_contexts = {}
```

### 5. Implement Query Engine

```python
# query/query.py
class MemoryQuery:
    def __init__(self):
        # Query parameters
        self.query_text = ""
        self.context_tags = []
        self.time_range = None
        
        # Metadata filters
        self.metadata_filters = {}
        
        # Relationship parameters
        self.relationship_params = {
            'min_semantic_similarity': 0.0,
            'min_metric_similarity': 0.0,
            'min_relationship_strength': 0.0
        }
        
        # Archetype weights
        self.archetype_weights = {
            'ella_emotion': 1.0,
            'ella_ontology': 1.0,
            'ella_deception': 1.0,
            'ella_experience': 1.0,
            'ella_historical': 1.0,
            'ella_research': 1.0,
            'ella_analytical': 1.0,
            'ella_protective': 1.0
        }
```

## Testing

### 1. Unit Tests

Create tests for each component:
```python
# tests/test_memory.py
def test_memory_formation():
    memory = Memory()
    assert memory.user_prompt == ""
    assert memory.memory_priority == 0.0
    assert len(memory.relationships) == 4

# tests/test_archetypes.py
def test_emotional_evaluation():
    archetype = EllaEmotion()
    eval = await archetype.evaluate("I feel happy", {})
    assert 0 <= eval.metrics['emotional_depth'] <= 1.0
    assert 0 <= eval.metrics['empathy_level'] <= 1.0
```

### 2. Integration Tests

Test component interactions:
```python
# tests/test_integration.py
async def test_memory_formation_with_context():
    # Create context
    context = InteractionContext()
    context.metadata['session_id'] = "test_session"
    
    # Form memory
    memory = await form_memory("Test input", context)
    assert memory.metadata['session_id'] == "test_session"
    
    # Check evaluations
    assert len(memory.evaluations) == 8  # All archetypes
    for eval in memory.evaluations:
        assert 0 <= eval.archetype_priority <= 1.0
```

## Deployment

1. Package the project:
```bash
python setup.py sdist bdist_wheel
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
pytest tests/
```

4. Start the system:
```python
from eumas import create_app

app = create_app()
app.run()
```

## Integration

The system integrates with:
- Memory storage system
- Context management
- Query processing
- Archetype evaluations

For detailed documentation, see:
- [Memory Models](theory/memory-models.md)
- [Archetype System](components/archetypes.md)
- [Context Engine](components/context.md)
- [Query Engine](components/query.md)
