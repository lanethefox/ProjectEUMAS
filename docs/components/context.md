# EllaContext

EllaContext is the core context management component of EUMAS, responsible for understanding, retrieving, and synthesizing contextual information from conversations and memories.

## Overview

EllaContext serves as the bridge between user interactions and memory systems, providing rich contextual understanding for natural personality development. It processes incoming messages, retrieves relevant memories, and synthesizes context for EllaPrimary's response generation.

## Core Functions

### Context Processing
- **Input Analysis**: Processes user messages for key themes and semantic meaning
- **Memory Retrieval**: Fetches relevant memories using semantic and metric-based search
- **Context Synthesis**: Combines current interaction with historical context
- **Core Memory Integration**: Special handling of high-priority memories

### Memory Types

1. **Core Memories**
   - Highest priority memories that define personality
   - Always included verbatim in context
   - Direct influence on response generation

2. **Long-term Memories**
   - Persistent, significant memories
   - Fully included in context synthesis
   - Strong influence on personality consistency

3. **Recent Memories**
   - Recent interactions and experiences
   - Weighted by recency and relevance
   - Important for conversation continuity

## Implementation Guide

### Context Schema

```yaml
ContextRequest:
  user_message: str          # Current user input
  session_id: str           # Unique session identifier
  user_id: str             # User identifier
  timestamp: datetime      # Current interaction time
  retrieval_params:
    semantic_threshold: float  # Minimum similarity threshold
    max_memories: int         # Maximum memories to retrieve
    include_core: bool        # Whether to include core memories
    time_window: int         # Time window for recent memories

ContextResponse:
  relevant_memories: List[Memory]  # Retrieved memories
  core_memories: List[Memory]      # Core personality memories
  context_summary: str            # Synthesized context
  archetype_states: Dict          # Current archetype states
  relationship_graph: Dict        # Memory relationship data
```

### Key Methods

1. **Context Retrieval**
```python
def retrieve_context(
    message: str,
    params: ContextParams
) -> ContextResponse:
    """
    Retrieve and synthesize context for the current interaction
    """
```

2. **Memory Search**
```python
def search_memories(
    query: str,
    search_type: str,  # 'semantic' or 'metric'
    threshold: float
) -> List[Memory]:
    """
    Search memory database for relevant memories
    """
```

3. **Context Synthesis**
```python
def synthesize_context(
    current_message: str,
    memories: List[Memory]
) -> str:
    """
    Create coherent context summary from memories
    """
```

4. **Core Memory Management**
```python
def process_core_memories(
    memories: List[Memory]
) -> List[Memory]:
    """
    Special handling for core personality memories
    """
```

## Usage Examples

### Basic Context Retrieval
```python
context = ella_context.retrieve_context(
    message="How are you feeling today?",
    params=ContextParams(
        semantic_threshold=0.7,
        max_memories=10,
        include_core=True
    )
)
```

### Memory Search
```python
related_memories = ella_context.search_memories(
    query="previous conversations about emotions",
    search_type="semantic",
    threshold=0.8
)
```

### Context Synthesis
```python
summary = ella_context.synthesize_context(
    current_message="Let's talk about your growth",
    memories=related_memories
)
```

## Best Practices

1. **Memory Retrieval**
   - Always include core memories for personality consistency
   - Balance between recent and historical context
   - Use appropriate semantic thresholds for relevance

2. **Context Synthesis**
   - Prioritize recent interactions for immediate context
   - Include emotional and factual context
   - Maintain personality consistency

3. **Performance Optimization**
   - Use efficient vector similarity search
   - Implement memory caching for frequent retrievals
   - Optimize relationship graph queries

## Integration Points

1. **With EllaPrimary**
   - Provides context for response generation
   - Maintains personality consistency
   - Enables natural conversation flow

2. **With EllaEvaluator**
   - Receives memory evaluations
   - Updates relationship graphs
   - Adjusts memory priorities

3. **With Memory System**
   - Manages memory retrieval
   - Updates memory relationships
   - Handles memory prioritization

## Error Handling

1. **Missing Context**
   - Fallback to core memories
   - Use default personality traits
   - Log context retrieval failures

2. **Invalid Memories**
   - Skip corrupted memory entries
   - Maintain minimal valid context
   - Report memory integrity issues

3. **Performance Issues**
   - Implement timeout mechanisms
   - Use cached results when necessary
   - Degrade gracefully under load