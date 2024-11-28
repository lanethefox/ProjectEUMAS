# Memory Management

## Overview

The Memory Management system is responsible for creating, storing, retrieving, and maintaining memories within EUMAS. It implements efficient storage strategies and optimizes memory access patterns.

## Architecture

```mermaid
graph TD
    subgraph Memory Manager
        MC[Memory Creator]
        MS[Memory Store]
        MR[Memory Retriever]
        MI[Memory Indexer]
    end

    subgraph Storage Layer
        VDB[(Vector Store)]
        GDB[(Graph Store)]
        RDB[(Relational Store)]
    end

    MC --> MS
    MS --> VDB
    MS --> GDB
    MS --> RDB
    MR --> VDB
    MR --> GDB
    MR --> RDB
    MI --> VDB
    MI --> GDB
    MI --> RDB
```

## Memory Structure

### Memory Object
```typescript
interface Memory {
    id: string;
    content: string;
    embedding: number[];
    metadata: {
        created_at: timestamp;
        updated_at: timestamp;
        source: string;
        context: string;
        archetype: string;
    };
    relationships: {
        parent_id?: string;
        child_ids: string[];
        related_ids: string[];
    };
    metrics: {
        importance: number;
        relevance: number;
        recency: number;
    };
}
```

## Core Operations

### Memory Creation
```python
async def create_memory(
    content: str,
    context: str,
    source: str,
    relationships: dict = None
) -> Memory:
    # Generate embedding
    embedding = await vector_engine.generate_embedding(content)
    
    # Create memory object
    memory = Memory(
        content=content,
        embedding=embedding,
        metadata={
            'context': context,
            'source': source,
            'created_at': datetime.now()
        },
        relationships=relationships or {}
    )
    
    # Store in databases
    await store_memory(memory)
    
    return memory
```

### Memory Retrieval
```python
async def retrieve_memories(
    query: str,
    context: str = None,
    limit: int = 10,
    threshold: float = 0.7
) -> List[Memory]:
    # Generate query embedding
    query_embedding = await vector_engine.generate_embedding(query)
    
    # Search vector store
    similar_memories = await vector_store.similarity_search(
        query_embedding,
        limit=limit,
        threshold=threshold
    )
    
    # Apply context filter if provided
    if context:
        similar_memories = [
            m for m in similar_memories
            if context_engine.matches_context(m, context)
        ]
    
    return similar_memories
```

## Storage Strategy

### Vector Store
- Uses pgvector for embedding storage
- Implements HNSW index for fast similarity search
- Optimizes for high-dimensional vector operations

### Graph Store
- Stores memory relationships
- Enables efficient traversal
- Supports relationship types and weights

### Relational Store
- Stores metadata and metrics
- Handles ACID transactions
- Provides SQL query capabilities

## Memory Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Active
    Active --> Archived
    Active --> Deleted
    Archived --> Active
    Archived --> Deleted
    Deleted --> [*]
```

### States
1. **Created**: Initial memory creation
2. **Active**: Regular access and updates
3. **Archived**: Reduced priority, compressed storage
4. **Deleted**: Marked for removal

## Optimization

### Caching Strategy
```python
CACHE_CONFIG = {
    'memory_cache_size': 1000,
    'vector_cache_size': 100,
    'cache_ttl': 3600,
    'prefetch_threshold': 0.8
}
```

### Batch Operations
```python
async def batch_create_memories(
    memories: List[Dict],
    batch_size: int = 50
) -> List[Memory]:
    results = []
    for batch in chunks(memories, batch_size):
        # Generate embeddings in parallel
        embeddings = await vector_engine.batch_generate_embeddings(
            [m['content'] for m in batch]
        )
        
        # Create memory objects
        memory_objects = [
            Memory(content=m['content'],
                  embedding=e,
                  metadata=m['metadata'])
            for m, e in zip(batch, embeddings)
        ]
        
        # Batch store
        await store_memories(memory_objects)
        results.extend(memory_objects)
    
    return results
```

## Error Handling

### Recovery Mechanisms
```python
class MemoryOperationError(Exception):
    pass

async def safe_memory_operation(operation: Callable, *args, **kwargs):
    try:
        return await operation(*args, **kwargs)
    except VectorStoreError:
        # Handle vector store failures
        await failover_to_backup_store()
    except GraphStoreError:
        # Handle graph store failures
        await rebuild_relationships()
    except DatabaseError:
        # Handle database failures
        await initiate_recovery()
    raise MemoryOperationError("Failed to complete memory operation")
```

## Monitoring

### Key Metrics
- Creation rate
- Retrieval latency
- Storage utilization
- Cache hit ratio

### Health Checks
```python
async def check_memory_system_health():
    return {
        'vector_store': await check_vector_store(),
        'graph_store': await check_graph_store(),
        'relational_store': await check_relational_store(),
        'cache': await check_cache_status()
    }
```

## Configuration

### Environment Variables
```bash
# Storage Configuration
VECTOR_STORE_URL=postgresql://user:pass@host:5432/db
GRAPH_STORE_URL=neo4j://user:pass@host:7687
REDIS_URL=redis://host:6379

# Operation Limits
MAX_BATCH_SIZE=100
MAX_VECTOR_DIMENSION=1536
CACHE_TTL=3600

# Performance Tuning
PREFETCH_SIZE=50
INDEX_REFRESH_INTERVAL=300
```

## Integration

### Event System
```python
@memory_events.on('memory.created')
async def handle_memory_created(memory: Memory):
    # Update indexes
    await memory_indexer.index_memory(memory)
    
    # Notify subscribers
    await notify_memory_subscribers(memory)
    
    # Update analytics
    await update_memory_metrics(memory)
```

## Development Guidelines

### Best Practices
1. Always use batch operations for multiple memories
2. Implement proper error handling and recovery
3. Monitor performance metrics
4. Use appropriate indexes
5. Implement caching strategies

### Testing
```python
async def test_memory_creation():
    # Test basic creation
    memory = await create_memory(
        content="Test memory",
        context="test",
        source="unit_test"
    )
    assert memory.id is not None
    
    # Test relationships
    related_memory = await create_memory(
        content="Related memory",
        context="test",
        source="unit_test",
        relationships={'related_ids': [memory.id]}
    )
    assert memory.id in related_memory.relationships['related_ids']
```

## Further Reading
- [Vector Operations](../data/vectors.md)
- [Graph Operations](../data/graph.md)
- [Performance Tuning](../optimization/README.md)
- [Error Handling](../troubleshooting/README.md)
