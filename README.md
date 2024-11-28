# EUMAS (Ella Unified Memory Augmentation System)

## Overview
EUMAS is a biologically-inspired memory system that combines graph-based memory storage with neural architectures to create a flexible, context-aware memory retrieval system. The system draws inspiration from both computer science principles of graph databases and neuroscientific understanding of human memory formation and recall.

## Infrastructure

### Core Components
- **PostgreSQL + pgvector**: Primary storage with vector similarity search
- **Python Backend**: Handles memory processing and graph operations
- **OpenAI API**: Generates embeddings and assists in memory evaluation
- **Edge Functions**: Manages compute-intensive operations
- **Realtime WebSockets**: Enables state synchronization
- **Row Level Security**: Ensures data privacy and access control

## Memory System Design

### Graph-Based Architecture
- **Nodes**: Individual memories with vector embeddings
- **Edges**: Weighted relationships between memories
- **Clusters**: Groups of semantically or contextually related memories
- **Traversal**: Path-finding through memory space based on relevance

### Context Management
- Multi-dimensional context storage
- Dynamic context updating
- Context-aware memory retrieval
- Temporal relationship tracking

### Archetype System
- Predefined evaluation metrics
- Memory classification
- Performance monitoring
- Quality assessment

## Theoretical Foundation

### Computer Science Concepts
- **Graph Theory**: Memory relationships and traversal
- **Vector Spaces**: Semantic similarity measurement
- **Clustering Algorithms**: Memory organization
- **Information Retrieval**: Context-aware search

### Neuroscience Principles
- **Hippocampal Indexing**: Memory relationship mapping
- **Hebbian Learning**: Connection strength adjustment
- **State-Dependent Memory**: Context influence on recall
- **Neural Pattern Completion**: Memory reconstruction

## Implementation Details

### Memory Operations
```python
# Example: Memory Creation and Linking
memory = create_memory(prompt, response, context)
similar_memories = find_similar_memories(memory)
create_memory_links(memory, similar_memories)

# Example: Context-Aware Retrieval
relevant_memories = find_memories(
    query=query,
    context=current_context,
    archetype=selected_archetype
)
```

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for detailed implementation guide.

## Data Dictionary

### Core Tables
- **memories**: Stores individual memory nodes
- **memory_temporal_links**: Manages memory relationships
- **memory_evaluations**: Tracks archetype-based evaluations
- **archetype_metrics**: Defines evaluation criteria
- **archetype_states**: Monitors system performance

### Key Fields
- **embedding**: Vector representation of memory content
- **context**: JSONB field storing contextual information
- **cluster_strength**: Relationship weight arrays
- **target_memory_ids**: Related memory references

## Query Examples

### Graph Traversal
```sql
-- Find related memories with context filtering
WITH RECURSIVE memory_graph AS (
    -- Base case
    SELECT source_memory_id, target_memory_ids
    FROM memory_temporal_links
    WHERE source_memory_id = :start_id
    
    UNION ALL
    
    -- Recursive case
    SELECT l.source_memory_id, l.target_memory_ids
    FROM memory_temporal_links l
    JOIN memory_graph g ON l.source_memory_id = ANY(g.target_memory_ids)
)
SELECT * FROM memory_graph;
```

### Analytics
```sql
-- Memory cluster analysis
SELECT 
    relationship_type,
    avg(array_length(target_memory_ids, 1)) as avg_cluster_size,
    avg(array_length(cluster_strength, 1)) as avg_connections
FROM memory_temporal_links
GROUP BY relationship_type;
```

## Getting Started

### Prerequisites
- PostgreSQL 14+ with pgvector
- Python 3.9+
- OpenAI API access

### Quick Start
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables
4. Initialize database: `python scripts/init_db.py`
5. Run tests: `python -m pytest tests/`

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License
MIT License - see [LICENSE](LICENSE) file.

## Acknowledgments
- OpenAI for embedding technology
- PostgreSQL and pgvector teams
- Neuroscience research community
