# EUMAS Schema Documentation

## Core Tables

### memories
Stores the base memory entries with their raw interaction data and metadata.

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| id | UUID | Unique identifier for the memory | PRIMARY KEY, DEFAULT uuid_generate_v4() |
| user_prompt | TEXT | Original user input/prompt | NOT NULL |
| assistant_response | TEXT | Complete response from the assistant | NOT NULL |
| embedding | vector(1536) | OpenAI embedding of combined prompt and response | NOT NULL |
| created_at | TIMESTAMPTZ | Creation timestamp | DEFAULT CURRENT_TIMESTAMP |
| last_accessed | TIMESTAMPTZ | Last retrieval timestamp | DEFAULT CURRENT_TIMESTAMP |
| priority_score | FLOAT | Current importance score | DEFAULT 1.0 |
| decay_rate | FLOAT | Rate at which memory importance decays | DEFAULT 0.1 |
| context | JSONB | Contextual information (emotional state, time, environment, etc.) | |

### archetype_metrics
Defines the available metrics for each archetype, providing a structured approach to evaluation.

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| id | UUID | Unique identifier | PRIMARY KEY, DEFAULT uuid_generate_v4() |
| archetype | TEXT | Archetype identifier (e.g., 'Ella-M') | NOT NULL |
| metric_name | TEXT | Name of the metric | NOT NULL |
| description | TEXT | Detailed description of what the metric measures | NOT NULL |
| value_type | TEXT | Type of value (numeric, categorical, boolean) | NOT NULL |
| value_range | JSONB | Valid range or set of values | NOT NULL |
| weight | FLOAT | Importance weight in archetype calculations | DEFAULT 1.0 |
| created_at | TIMESTAMPTZ | When the metric was defined | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMPTZ | Last modification timestamp | DEFAULT CURRENT_TIMESTAMP |

### memory_evaluations
Stores metric evaluations for each memory-archetype combination.

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| id | UUID | Unique identifier | PRIMARY KEY, DEFAULT uuid_generate_v4() |
| memory_id | UUID | Reference to memories table | FOREIGN KEY |
| archetype_metric_id | UUID | Reference to archetype_metrics | FOREIGN KEY |
| value | TEXT | Metric value (converted to appropriate type based on metric definition) | NOT NULL |
| evaluation_text | TEXT | Textual explanation of the evaluation | NOT NULL |
| created_at | TIMESTAMPTZ | Evaluation timestamp | DEFAULT CURRENT_TIMESTAMP |

### memory_temporal_links
Tracks relationships between memories, allowing one memory to be associated with multiple related memories based on clustering.

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| id | UUID | Unique identifier | PRIMARY KEY, DEFAULT uuid_generate_v4() |
| source_memory_id | UUID | Source memory reference | FOREIGN KEY |
| target_memory_ids | UUID[] | Array of related memory references | NOT NULL |
| relationship_type | TEXT | Type of relationship (semantic, temporal, contextual, etc.) | NOT NULL |
| cluster_strength | FLOAT[] | Array of relationship strengths corresponding to target_memory_ids | NOT NULL |
| cluster_metadata | JSONB | Clustering details (algorithm parameters, similarity thresholds, etc.) | |
| created_at | TIMESTAMPTZ | Link creation timestamp | DEFAULT CURRENT_TIMESTAMP |

### archetype_states
Tracks the current state of each archetype based on memory evaluations.

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| id | UUID | Unique identifier | PRIMARY KEY, DEFAULT uuid_generate_v4() |
| archetype | TEXT | Archetype identifier | UNIQUE, NOT NULL |
| state_vector | vector(32) | Current state embedding | NOT NULL |
| influence_score | FLOAT | Current influence level | DEFAULT 1.0 |
| active_metrics | TEXT[] | Currently active metrics | NOT NULL |
| updated_at | TIMESTAMPTZ | Last state update | DEFAULT CURRENT_TIMESTAMP |
| metadata | JSONB | Additional state metadata | |

## Sample Memory Context Structure
```json
{
  "emotional": {
    "user_state": "frustrated",
    "conversation_tone": "supportive",
    "intensity": 0.8
  },
  "temporal": {
    "time_of_day": "evening",
    "day_of_week": "monday",
    "season": "winter"
  },
  "environmental": {
    "location": "home",
    "activity": "working",
    "platform": "desktop"
  },
  "behavioral": {
    "interaction_pattern": "seeking_advice",
    "response_preference": "detailed",
    "engagement_level": "high"
  }
}
```

## Sample Archetype Metrics

### Ella-M (Maternal)
| Metric Name | Description | Type | Range |
|-------------|-------------|------|-------|
| empathy_level | Degree of emotional understanding | numeric | 0.0 - 1.0 |
| care_intensity | Level of nurturing response | numeric | 0.0 - 1.0 |
| emotional_resonance | Alignment with user's emotional state | numeric | 0.0 - 1.0 |
| support_type | Type of support provided | categorical | ['emotional', 'practical', 'motivational'] |
| protection_level | Degree of protective response | numeric | 0.0 - 1.0 |

### Ella-A (Analytical)
| Metric Name | Description | Type | Range |
|-------------|-------------|------|-------|
| logical_coherence | Clarity of logical structure | numeric | 0.0 - 1.0 |
| problem_complexity | Assessed complexity level | numeric | 0.0 - 1.0 |
| solution_clarity | Clarity of proposed solutions | numeric | 0.0 - 1.0 |
| analysis_depth | Depth of analytical thinking | numeric | 0.0 - 1.0 |
| evidence_based | Degree of evidence support | boolean | true/false |

### Ella-R (Researcher)
| Metric Name | Description | Type | Range |
|-------------|-------------|------|-------|
| curiosity_level | Degree of intellectual curiosity | numeric | 0.0 - 1.0 |
| knowledge_depth | Depth of domain knowledge | numeric | 0.0 - 1.0 |
| investigation_quality | Quality of research approach | numeric | 0.0 - 1.0 |
| learning_potential | Potential for new insights | numeric | 0.0 - 1.0 |
| source_reliability | Reliability of information sources | numeric | 0.0 - 1.0 |

## Schema Initialization
```sql
-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Create tables
CREATE TABLE memories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_prompt TEXT NOT NULL,
    assistant_response TEXT NOT NULL,
    embedding vector(1536) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    last_accessed TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    priority_score FLOAT DEFAULT 1.0,
    decay_rate FLOAT DEFAULT 0.1,
    context JSONB
);

CREATE TABLE archetype_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    archetype TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    description TEXT NOT NULL,
    value_type TEXT NOT NULL,
    value_range JSONB NOT NULL,
    weight FLOAT DEFAULT 1.0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE memory_evaluations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    memory_id UUID REFERENCES memories(id),
    archetype_metric_id UUID REFERENCES archetype_metrics(id),
    value TEXT NOT NULL,
    evaluation_text TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE memory_temporal_links (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_memory_id UUID REFERENCES memories(id),
    target_memory_ids UUID[] NOT NULL,
    relationship_type TEXT NOT NULL,
    cluster_strength FLOAT[] NOT NULL,
    cluster_metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT target_strength_match CHECK (array_length(target_memory_ids, 1) = array_length(cluster_strength, 1))
);

CREATE TABLE archetype_states (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    archetype TEXT UNIQUE NOT NULL,
    state_vector vector(32) NOT NULL,
    influence_score FLOAT DEFAULT 1.0,
    active_metrics TEXT[] NOT NULL,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Create indexes
CREATE INDEX ON memories USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON memory_evaluations (memory_id, archetype_metric_id);
CREATE INDEX ON memory_temporal_links (source_memory_id);
CREATE INDEX ON memory_temporal_links USING gin(target_memory_ids);
CREATE INDEX ON archetype_metrics (archetype, metric_name);

## Graph Traversal Examples

### Recursive Memory Cluster Navigation
```sql
WITH RECURSIVE memory_graph AS (
    -- Base case: Start with a specific memory and its direct connections
    SELECT 
        source_memory_id,
        unnest(target_memory_ids) as target_id,
        unnest(cluster_strength) as strength,
        relationship_type,
        1 as depth,
        ARRAY[source_memory_id] as path
    FROM memory_temporal_links
    WHERE source_memory_id = '123e4567-e89b-12d3-a456-426614174000'  -- Starting memory

    UNION ALL

    -- Recursive case: Follow connections to specified depth
    SELECT 
        l.source_memory_id,
        unnest(l.target_memory_ids) as target_id,
        unnest(l.cluster_strength) as strength,
        l.relationship_type,
        g.depth + 1,
        g.path || l.source_memory_id
    FROM memory_temporal_links l
    INNER JOIN memory_graph g ON l.source_memory_id = g.target_id
    WHERE 
        g.depth < 3  -- Limit depth to prevent infinite recursion
        AND NOT l.source_memory_id = ANY(g.path)  -- Prevent cycles
)
SELECT DISTINCT
    m.id,
    m.user_prompt,
    me.value as archetype_evaluation,
    mg.depth,
    mg.strength,
    mg.relationship_type
FROM memory_graph mg
JOIN memories m ON mg.target_id = m.id
LEFT JOIN memory_evaluations me ON m.id = me.memory_id
JOIN archetype_metrics am ON me.archetype_metric_id = am.id
WHERE 
    am.archetype = 'specific_archetype'  -- Filter by archetype
    AND mg.strength >= 0.8  -- Filter by relationship strength
ORDER BY mg.depth, mg.strength DESC;
```

This query demonstrates:
1. **Graph Structure**: Each memory can connect to multiple related memories through `target_memory_ids`
2. **Archetype Association**: We can filter memories by their archetype evaluations
3. **Strength-based Filtering**: Connections can be filtered by `cluster_strength`
4. **Cycle Prevention**: The path tracking prevents infinite loops
5. **Depth Control**: We can limit how far we traverse from the starting memory

### Sample Query for Finding Related Memories by Context
```sql
-- Find memories in the same cluster with similar context
SELECT 
    m.id,
    m.user_prompt,
    m.context,
    unnest(mtl.target_memory_ids) as related_memory_id,
    unnest(mtl.cluster_strength) as relationship_strength
FROM memories m
JOIN memory_temporal_links mtl ON m.id = mtl.source_memory_id
WHERE 
    m.context->>'topic' = 'specific_topic'
    AND mtl.relationship_type = 'semantic_cluster'
    AND mtl.cluster_metadata->>'algorithm' = 'affinity_propagation'
ORDER BY relationship_strength DESC;
```

This structure allows us to:
- Traverse the memory space based on semantic relationships
- Filter by context, archetype, or relationship strength
- Follow chains of related memories
- Analyze clusters of memories with similar characteristics

## Sample Memory Link Structure
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "source_memory_id": "123e4567-e89b-12d3-a456-426614174000",
  "target_memory_ids": [
    "223e4567-e89b-12d3-a456-426614174001",
    "323e4567-e89b-12d3-a456-426614174002",
    "423e4567-e89b-12d3-a456-426614174003"
  ],
  "relationship_type": "semantic_cluster",
  "cluster_strength": [0.92, 0.87, 0.85],
  "cluster_metadata": {
    "algorithm": "affinity_propagation",
    "parameters": {
      "damping": 0.9,
      "preference": -50,
      "convergence_iter": 15
    },
    "similarity_metrics": {
      "embedding_weight": 0.7,
      "context_weight": 0.3
    },
    "cluster_timestamp": "2024-02-20T15:30:00Z",
    "cluster_size": 3,
    "cluster_coherence": 0.88
  }
}
