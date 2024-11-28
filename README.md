# EUMAS: Ella Unified Memory and Archetype System

## 1. Architecture Overview

### 1.1 Infrastructure Components
- **Supabase Backend**
  - PostgreSQL with pgvector extension
  - Edge Functions for compute-intensive operations
  - Realtime websockets for state synchronization
  - Row Level Security (RLS) policies
  - PostgREST API interface

- **Application Layer**
  - Python-based memory management system
  - OpenAI API integration for embeddings and evaluation
  - Asynchronous operation handlers
  - Caching system using Redis

- **Client Layer**
  - WebSocket connections for real-time updates
  - Batch operation handlers
  - Local state management
  - Error recovery mechanisms

### 1.2 Edge Functions Architecture
Edge Functions handle compute-intensive operations close to the data:

1. **Memory Clustering Service**
```typescript
// memory-cluster.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from '@supabase/supabase-js'
import { affinityPropagation } from './clustering'

serve(async (req) => {
  const { vectors, preferences } = await req.json()
  const clusters = await affinityPropagation(vectors, {
    damping: 0.9,
    maxIter: 200,
    convergence_iter: 15
  })
  
  return new Response(JSON.stringify({ clusters }), {
    headers: { 'Content-Type': 'application/json' }
  })
})
```

2. **Memory Decay Service**
```typescript
// memory-decay.ts
serve(async (req) => {
  const { memory_id, last_access, importance } = await req.json()
  const decay_factor = calculateDecay(last_access, importance)
  
  // Update memory priority
  await supabase
    .from('memories')
    .update({ priority_score: decay_factor })
    .match({ id: memory_id })
})
```

### 1.3 Realtime WebSocket Integration
```python
async def setup_realtime_handlers(client):
    channel = client.channel('memory_updates')
    
    # Subscribe to memory state changes
    channel.on('UPDATE', lambda payload: handle_memory_update(payload))
    channel.on('INSERT', lambda payload: handle_new_memory(payload))
    
    # Subscribe to archetype state changes
    channel.on('archetype_changes', lambda payload: update_archetype_state(payload))
```

## 2. Memory Schema Design

### 2.1 Core Tables

```sql
-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Memories table
CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content JSONB NOT NULL,
    embedding vector(1536) NOT NULL,  -- OpenAI embedding
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    priority_score FLOAT DEFAULT 1.0,
    decay_rate FLOAT DEFAULT 0.1,
    context JSONB,
    metadata JSONB
);

-- Memory evaluations
CREATE TABLE memory_evaluations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    memory_id UUID REFERENCES memories(id),
    archetype TEXT NOT NULL,
    metrics vector(16) NOT NULL,  -- Archetype-specific metrics
    evaluation JSONB NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    confidence_score FLOAT DEFAULT 1.0
);

-- Temporal links
CREATE TABLE memory_temporal_links (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_memory_id UUID REFERENCES memories(id),
    target_memory_id UUID REFERENCES memories(id),
    relationship_type TEXT NOT NULL,
    strength FLOAT DEFAULT 1.0,
    context JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Archetype states
CREATE TABLE archetype_states (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    archetype TEXT UNIQUE NOT NULL,
    current_state vector(32) NOT NULL,
    influence_score FLOAT DEFAULT 1.0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Create indexes
CREATE INDEX ON memories USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON memory_evaluations (memory_id);
CREATE INDEX ON memory_temporal_links (source_memory_id, target_memory_id);
```

### 2.2 Sample Memory Instance
```json
{
  "memory": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "content": {
      "type": "conversation",
      "text": "User expressed frustration about work-life balance",
      "timestamp": "2024-02-20T15:30:00Z",
      "tokens": ["work", "balance", "frustration", "stress"]
    },
    "embedding": "[0.123, 0.456, ...]",  -- 1536-dimensional vector
    "priority_score": 0.85,
    "decay_rate": 0.1,
    "context": {
      "emotional_state": "frustrated",
      "energy_level": "low",
      "time_of_day": "afternoon"
    }
  },
  "evaluations": [
    {
      "archetype": "Ella-M",
      "metrics": [0.9, 0.8, 0.7, ...],  -- 16-dimensional vector
      "evaluation": {
        "empathy_level": 0.9,
        "emotional_resonance": 0.85,
        "support_needed": 0.8,
        "care_response": "high"
      },
      "confidence_score": 0.95
    },
    {
      "archetype": "Ella-A",
      "metrics": [0.6, 0.7, 0.8, ...],
      "evaluation": {
        "problem_complexity": 0.7,
        "solution_clarity": 0.6,
        "action_needed": "time_management_strategy",
        "priority": "high"
      },
      "confidence_score": 0.85
    }
  ],
  "temporal_links": [
    {
      "target_memory_id": "550e8400-e29b-41d4-a716-446655440001",
      "relationship_type": "causal",
      "strength": 0.75,
      "context": {
        "link_type": "work_related",
        "temporal_distance": "1_day"
      }
    }
  ]
}
```

## 3. Memory Operations

### 3.1 Memory Retrieval Process
1. **Query Preparation**
```python
async def prepare_memory_query(input_text: str, context: dict):
    # Generate embedding for input
    embedding = await openai.embeddings.create(text=input_text)
    
    # Prepare context vector
    context_vector = process_context(context)
    
    return {
        'embedding': embedding,
        'context': context_vector,
        'timestamp': datetime.utcnow()
    }
```

2. **Similarity Search**
```sql
-- Supabase Edge Function
CREATE FUNCTION search_similar_memories(
    query_embedding vector(1536),
    similarity_threshold float,
    max_results int
) RETURNS TABLE (
    id uuid,
    content jsonb,
    similarity float
) AS $$
    SELECT id, content, 1 - (embedding <=> query_embedding) as similarity
    FROM memories
    WHERE 1 - (embedding <=> query_embedding) > similarity_threshold
    ORDER BY similarity DESC
    LIMIT max_results;
$$ LANGUAGE sql STABLE;
```

3. **Affinity Propagation Clustering**
```python
def cluster_memories(memories: List[dict], damping: float = 0.9):
    # Extract features (embedding + metrics)
    features = np.array([
        np.concatenate([
            m['embedding'],
            weighted_archetype_metrics(m['evaluations'])
        ]) for m in memories
    ])
    
    # Calculate similarity matrix
    S = -euclidean_distances(features, squared=True)
    
    # Run clustering
    clustering = AffinityPropagation(
        damping=damping,
        max_iter=200,
        convergence_iter=15,
        random_state=42
    ).fit(features)
    
    return clustering.labels_
```

### 3.2 Memory Decay
```python
def calculate_memory_decay(
    memory: dict,
    current_time: datetime,
    base_rate: float = 0.1
) -> float:
    time_diff = (current_time - memory['last_accessed']).total_seconds()
    importance = memory['priority_score']
    
    # Decay formula: exponential decay with importance scaling
    decay = math.exp(-base_rate * time_diff / (importance * 86400))
    
    return max(0.1, decay)  # Maintain minimum priority of 0.1
```

### 3.3 Memory Reinforcement
```python
async def reinforce_memory(memory_id: str, interaction_strength: float):
    # Update priority score
    await supabase.rpc('update_memory_priority', {
        'memory_id': memory_id,
        'strength': interaction_strength
    })
    
    # Update temporal links
    await supabase.rpc('strengthen_temporal_links', {
        'memory_id': memory_id,
        'factor': interaction_strength
    })
```

## 4. Archetype Integration

### 4.1 Archetype State Updates
```python
async def update_archetype_state(
    archetype: str,
    memory_evaluation: dict,
    current_state: np.ndarray
):
    # Calculate new state vector
    influence = memory_evaluation['confidence_score']
    new_state = (1 - influence) * current_state + influence * memory_evaluation['metrics']
    
    # Update state in database
    await supabase.from('archetype_states').upsert({
        'archetype': archetype,
        'current_state': new_state.tolist(),
        'influence_score': influence,
        'updated_at': datetime.utcnow()
    })
```

### 4.2 Memory Evaluation Pipeline
```python
async def evaluate_memory(content: str, context: dict):
    evaluations = []
    
    for archetype in ARCHETYPES:
        # Get archetype-specific evaluation
        evaluation = await openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": ARCHETYPE_PROMPTS[archetype]},
                {"role": "user", "content": f"Evaluate: {content}\nContext: {context}"}
            ]
        )
        
        # Process evaluation into metrics
        metrics = process_evaluation_metrics(evaluation.choices[0].message.content)
        evaluations.append({
            'archetype': archetype,
            'metrics': metrics,
            'evaluation': evaluation.choices[0].message.content,
            'confidence_score': calculate_confidence(metrics)
        })
    
    return evaluations
```

## 5. Performance Optimization

### 5.1 Caching Strategy
```python
class MemoryCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.ttl = 3600  # 1 hour default TTL
    
    async def cache_cluster(self, query_hash: str, clusters: List[dict]):
        await self.redis.setex(
            f"cluster:{query_hash}",
            self.ttl,
            json.dumps(clusters)
        )
    
    async def get_cached_cluster(self, query_hash: str):
        cached = await self.redis.get(f"cluster:{query_hash}")
        return json.loads(cached) if cached else None
```

### 5.2 Batch Processing
```python
async def batch_process_memories(memories: List[dict]):
    # Process in chunks of 50
    chunk_size = 50
    for i in range(0, len(memories), chunk_size):
        chunk = memories[i:i + chunk_size]
        
        # Parallel processing
        tasks = [
            process_memory(memory)
            for memory in chunk
        ]
        await asyncio.gather(*tasks)
```

## 6. Security Considerations

### 6.1 Row Level Security
```sql
-- Enable RLS
ALTER TABLE memories ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Memory access policy"
    ON memories
    FOR ALL
    USING (auth.uid() = owner_id);
```

### 6.2 API Security
```python
def setup_security_middleware(app):
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response
