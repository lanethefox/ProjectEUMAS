# Context Engine

## Overview

The Context Engine analyzes and manages contextual information for memories, enabling more accurate memory retrieval and relationship building. It processes both explicit and implicit context signals to create a rich contextual understanding.

## Architecture

```mermaid
graph TD
    subgraph Context Engine
        CA[Context Analyzer]
        CP[Context Processor]
        CE[Context Extractor]
        CM[Context Manager]
    end

    subgraph Analysis Tools
        NLP[NLP Processor]
        TA[Temporal Analyzer]
        SA[Semantic Analyzer]
    end

    subgraph Storage
        CS[(Context Store)]
        MS[(Memory Store)]
    end

    CA --> NLP
    CA --> TA
    CA --> SA
    CP --> CA
    CE --> CP
    CM --> CE
    CM --> CS
    CM --> MS
```

## Context Structure

### Context Object
```typescript
interface Context {
    id: string;
    type: ContextType;
    value: string;
    metadata: {
        created_at: timestamp;
        updated_at: timestamp;
        confidence: number;
        source: string;
    };
    relationships: {
        memory_ids: string[];
        related_contexts: string[];
    };
    parameters: {
        temporal?: {
            start_time?: timestamp;
            end_time?: timestamp;
            duration?: number;
        };
        spatial?: {
            location?: string;
            coordinates?: [number, number];
        };
        semantic?: {
            topics: string[];
            entities: string[];
            sentiment: number;
        };
    };
}

enum ContextType {
    TEMPORAL,
    SPATIAL,
    SEMANTIC,
    EMOTIONAL,
    TASK,
    CUSTOM
}
```

## Core Operations

### Context Extraction
```python
async def extract_context(
    content: str,
    metadata: dict = None
) -> Context:
    # Extract temporal context
    temporal = await temporal_analyzer.analyze(content)
    
    # Extract semantic context
    semantic = await semantic_analyzer.analyze(content)
    
    # Extract emotional context
    emotional = await emotional_analyzer.analyze(content)
    
    # Combine contexts
    context = Context(
        type=determine_primary_context_type(
            temporal, semantic, emotional
        ),
        value=content,
        metadata={
            'confidence': calculate_confidence(
                temporal, semantic, emotional
            ),
            'source': metadata.get('source', 'auto')
        },
        parameters={
            'temporal': temporal,
            'semantic': semantic,
            'emotional': emotional
        }
    )
    
    return context
```

### Context Processing
```python
async def process_context(
    context: Context,
    memory_ids: List[str] = None
) -> ProcessedContext:
    # Enrich context with additional information
    enriched = await context_enricher.enrich(context)
    
    # Link to memories if provided
    if memory_ids:
        await link_context_to_memories(enriched, memory_ids)
    
    # Update context store
    await context_store.update(enriched)
    
    return enriched
```

## Analysis Components

### Temporal Analysis
```python
class TemporalAnalyzer:
    async def analyze(self, content: str) -> TemporalContext:
        # Extract temporal expressions
        temporal_expressions = self.extract_temporal_expressions(
            content
        )
        
        # Normalize to timestamps
        timestamps = self.normalize_timestamps(
            temporal_expressions
        )
        
        # Determine temporal relationships
        relationships = self.analyze_temporal_relationships(
            timestamps
        )
        
        return TemporalContext(
            timestamps=timestamps,
            relationships=relationships
        )
```

### Semantic Analysis
```python
class SemanticAnalyzer:
    async def analyze(self, content: str) -> SemanticContext:
        # Extract topics and entities
        topics = await self.extract_topics(content)
        entities = await self.extract_entities(content)
        
        # Perform sentiment analysis
        sentiment = await self.analyze_sentiment(content)
        
        # Generate semantic embedding
        embedding = await self.generate_embedding(content)
        
        return SemanticContext(
            topics=topics,
            entities=entities,
            sentiment=sentiment,
            embedding=embedding
        )
```

## Context Management

### Context Storage
```python
async def store_context(
    context: Context,
    batch: bool = False
) -> str:
    if batch:
        return await context_store.batch_insert([context])
    
    # Store context
    context_id = await context_store.insert(context)
    
    # Update indexes
    await update_context_indexes(context)
    
    # Notify subscribers
    await notify_context_change(context)
    
    return context_id
```

### Context Retrieval
```python
async def retrieve_context(
    query: str,
    context_type: ContextType = None,
    limit: int = 10
) -> List[Context]:
    # Generate query embedding
    query_embedding = await generate_embedding(query)
    
    # Search context store
    contexts = await context_store.search(
        embedding=query_embedding,
        context_type=context_type,
        limit=limit
    )
    
    # Rank and filter results
    ranked_contexts = await rank_contexts(contexts, query)
    
    return ranked_contexts
```

## Optimization

### Caching Strategy
```python
CONTEXT_CACHE_CONFIG = {
    'max_size': 1000,
    'ttl': 3600,
    'update_interval': 300
}

class ContextCache:
    async def get_or_compute(
        self,
        key: str,
        computer: Callable
    ) -> Context:
        # Check cache
        cached = await self.get(key)
        if cached:
            return cached
        
        # Compute if not found
        result = await computer()
        
        # Cache result
        await self.set(key, result)
        
        return result
```

### Batch Processing
```python
async def batch_process_contexts(
    contexts: List[Context],
    batch_size: int = 50
) -> List[ProcessedContext]:
    results = []
    for batch in chunks(contexts, batch_size):
        # Process batch in parallel
        processed = await asyncio.gather(*[
            process_context(context)
            for context in batch
        ])
        results.extend(processed)
    return results
```

## Error Handling

### Recovery Mechanisms
```python
class ContextError(Exception):
    pass

async def safe_context_operation(
    operation: Callable,
    *args,
    **kwargs
):
    try:
        return await operation(*args, **kwargs)
    except AnalysisError:
        # Handle analysis failures
        await fallback_analysis()
    except StorageError:
        # Handle storage failures
        await recover_context_store()
    except ProcessingError:
        # Handle processing failures
        await retry_processing()
    raise ContextError("Failed to complete context operation")
```

## Monitoring

### Key Metrics
```python
CONTEXT_METRICS = {
    'extraction_rate': 'contexts_extracted/second',
    'processing_latency': 'milliseconds',
    'storage_usage': 'bytes',
    'cache_hit_ratio': 'percentage'
}

async def monitor_context_system():
    return {
        'extraction': await monitor_extraction(),
        'processing': await monitor_processing(),
        'storage': await monitor_storage(),
        'cache': await monitor_cache()
    }
```

## Configuration

### Environment Variables
```bash
# Analysis Configuration
NLP_MODEL=gpt-4
SENTIMENT_MODEL=distilbert
ENTITY_MODEL=spacy

# Processing Limits
MAX_CONTEXT_SIZE=10000
BATCH_SIZE=50
CACHE_SIZE=1000

# Storage Configuration
CONTEXT_STORE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
```

## Integration

### Event System
```python
@context_events.on('context.created')
async def handle_context_created(context: Context):
    # Update indexes
    await update_context_indexes(context)
    
    # Notify subscribers
    await notify_context_subscribers(context)
    
    # Update analytics
    await update_context_metrics(context)
```

## Development Guidelines

### Best Practices
1. Always validate context before processing
2. Use batch operations for multiple contexts
3. Implement proper error handling
4. Monitor performance metrics
5. Use appropriate caching strategies

### Testing
```python
async def test_context_extraction():
    # Test basic extraction
    context = await extract_context(
        "Meeting with John at 2pm tomorrow"
    )
    assert context.type == ContextType.TEMPORAL
    
    # Test semantic extraction
    semantic = context.parameters['semantic']
    assert 'Meeting' in semantic.topics
    assert 'John' in semantic.entities
    
    # Test temporal extraction
    temporal = context.parameters['temporal']
    assert temporal.start_time is not None
```

## Further Reading
- [Memory Management](memory.md)
- [Archetype System](archetypes.md)
- [Query Engine](query.md)
- [Analytics](../analytics/README.md)
