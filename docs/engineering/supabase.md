# Supabase Integration

## Overview
EUMAS leverages Supabase's powerful features for real-time data synchronization, edge computing, and vector operations. This document details how we utilize each Supabase component.

## Database Features

### pgvector Integration
We use Supabase's native pgvector support for memory embeddings:

```sql
-- Enable pgvector extension
create extension vector;

-- Create hypertable for memory embeddings
create table memories (
  id uuid primary key default uuid_generate_v4(),
  content text not null,
  embedding vector(1536),
  metrics jsonb not null default '{}'::jsonb,
  justifications jsonb not null default '{}'::jsonb,
  annotations jsonb not null default '{}'::jsonb,
  affinities jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Trigger for automatic timestamp updates
create trigger handle_updated_at before update on memories
  for each row execute procedure moddatetime (updated_at);

-- Enable full-text search
alter table memories add column fts tsvector
  generated always as (to_tsvector('english', content)) stored;

create index memories_fts_idx on memories using gin(fts);

-- Create vector index for similarity search
create index on memories using ivfflat (embedding vector_cosine_ops);

-- Create indices for metric-based search
create index memories_metrics_idx on memories using gin (metrics);
create index memories_justifications_idx on memories using gin (justifications);
```

### Context Table Structure
```sql
create table contexts (
  id uuid primary key default uuid_generate_v4(),
  state jsonb not null,
  active_memories jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
```

Reference: [Supabase Vector Support](https://supabase.com/docs/guides/database/extensions/pgvector)

## Edge Functions

### Memory Clustering Service
```typescript
// /functions/memory-clustering/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from '@supabase/supabase-js'

serve(async (req) => {
  const { memories } = await req.json()
  const clusters = await performClustering(memories)
  
  return new Response(
    JSON.stringify({ clusters }),
    { headers: { 'Content-Type': 'application/json' } }
  )
})
```

Deployment command:
```bash
supabase functions deploy memory-clustering
```

Reference: [Edge Functions Guide](https://supabase.com/docs/guides/functions)

### Memory Evaluation Service
```typescript
// /functions/memory-evaluation/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { Configuration, OpenAIApi } from 'https://esm.sh/openai@3.2.1'

serve(async (req) => {
  const { content, context } = await req.json()
  
  const openai = new OpenAIApi(new Configuration({
    apiKey: Deno.env.get('OPENAI_API_KEY')
  }))

  // Get GPT-4's evaluation with metrics
  const evaluation = await openai.createChatCompletion({
    model: "gpt-4",
    messages: [
      {
        role: "system",
        content: `You are Ella, evaluating a new memory. For each metric, provide:
1. A scalar value (0.0-1.0)
2. A semantic justification
3. A contextual annotation

Consider these aspects:
- Emotional Depth
- Empathy Level
- Emotional Clarity
- Internal State
- Other relevant metrics`
      },
      {
        role: "user",
        content: `Memory: ${content}\nContext: ${context}`
      }
    ]
  })

  // Parse evaluation into structured format
  const parsed = parseMetricEvaluation(evaluation.data.choices[0].message?.content)

  return new Response(
    JSON.stringify(parsed),
    { headers: { 'Content-Type': 'application/json' } }
  )
})

function parseMetricEvaluation(text: string): {
  metrics: Record<string, number>,
  justifications: Record<string, string>,
  annotations: Record<string, string>
} {
  // TODO: Implement parsing logic
  return {
    metrics: {},
    justifications: {},
    annotations: {}
  }
}
```

Deployment command:
```bash
supabase functions deploy memory-evaluation
```

### Natural Affinity Discovery
```typescript
// /functions/affinity-discovery/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from '@supabase/supabase-js'
import { Configuration, OpenAIApi } from 'https://esm.sh/openai@3.2.1'

serve(async (req) => {
  const { memory_id } = await req.json()
  
  // Get related memories using vector similarity
  const { data: similarMemories } = await supabase
    .rpc('search_similar_memories', {
      query_embedding: memory.embedding,
      similarity_threshold: 0.8,
      match_count: 5
    })

  // Use GPT-4 to discover natural affinities
  const openai = new OpenAIApi(new Configuration({
    apiKey: Deno.env.get('OPENAI_API_KEY')
  }))

  const affinities = await openai.createChatCompletion({
    model: "gpt-4",
    messages: [
      {
        role: "system",
        content: "You are Ella, discovering natural connections between memories. Consider thematic, emotional, and contextual relationships."
      },
      {
        role: "user",
        content: `Discover affinities between these memories: ${JSON.stringify(similarMemories)}`
      }
    ]
  })

  return new Response(
    JSON.stringify({ affinities: affinities.data.choices[0].message }),
    { headers: { 'Content-Type': 'application/json' } }
  )
})
```

Deployment command:
```bash
supabase functions deploy affinity-discovery
```

Reference: [Edge Functions Guide](https://supabase.com/docs/guides/functions)

### Real-time Memory Updates

```typescript
// Subscribe to memory changes
const channel = supabase
  .channel('memory_changes')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'memories'
    },
    (payload) => {
      console.log('Change received!', payload)
    }
  )
  .subscribe()
```

Reference: [Realtime Guide](https://supabase.com/docs/guides/realtime)

## Database Functions

### Similarity Search
```sql
create function search_similar_memories(
  query_embedding vector(1536),
  similarity_threshold float,
  match_count int
)
returns table (
  id uuid,
  content jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    id,
    content,
    1 - (memories.embedding <=> query_embedding) as similarity
  from memories
  where 1 - (memories.embedding <=> query_embedding) > similarity_threshold
  order by memories.embedding <=> query_embedding
  limit match_count;
end;
$$;
```

### Search Memories with Metrics
```sql
create or replace function search_memories_with_metrics(
  query_embedding vector(1536),
  metric_filters jsonb,
  similarity_threshold float,
  match_count int
)
returns table (
  id uuid,
  content text,
  metrics jsonb,
  justifications jsonb,
  annotations jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    id,
    content,
    metrics,
    justifications,
    annotations,
    1 - (memories.embedding <=> query_embedding) as similarity
  from memories
  where 1 - (memories.embedding <=> query_embedding) > similarity_threshold
    and case
      when metric_filters is not null
      then metrics @> metric_filters
      else true
    end
  order by
    case
      when metric_filters is not null
      then jsonb_array_length(metrics)
      else 0
    end desc,
    memories.embedding <=> query_embedding
  limit match_count;
end;
$$;
```

Reference: [Database Functions](https://supabase.com/docs/guides/database/functions)

## Row Level Security (RLS)

```sql
-- Enable RLS
alter table memories enable row level security;

-- Create policies
create policy "Users can view their own memories"
  on memories for select
  using ( auth.uid() = user_id );

create policy "Users can insert their own memories"
  on memories for insert
  with check ( auth.uid() = user_id );
```

Reference: [Row Level Security](https://supabase.com/docs/guides/auth/row-level-security)

## Streaming Replication

We use Supabase's streaming replication for real-time memory updates:

```typescript
// Set up change listener
const subscription = supabase
  .channel('schema-db-changes')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
    },
    (payload) => {
      handleDatabaseChange(payload)
    }
  )
  .subscribe()
```

Reference: [Database Streaming](https://supabase.com/docs/guides/realtime/postgres-changes)

## Real-time Features

### Memory State Synchronization
```typescript
// Subscribe to memory evaluations and affinity updates
const channel = supabase
  .channel('memory_evaluations')
  .on(
    'postgres_changes',
    {
      event: 'UPDATE',
      schema: 'public',
      table: 'memories',
      filter: 'evaluation IS NOT NULL'
    },
    (payload) => {
      updateMemoryState(payload)
    }
  )
  .subscribe()
```

### Context Flow Management
```typescript
// Subscribe to context state changes
const contextChannel = supabase
  .channel('context_flow')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'contexts'
    },
    (payload) => {
      updateContextFlow(payload)
    }
  )
  .subscribe()
```

Reference: [Realtime Guide](https://supabase.com/docs/guides/realtime)

## Performance Optimization

### Connection Pooling
```sql
-- Configure connection pool
alter system set max_connections = '100';
alter system set superuser_reserved_connections = '3';
```

Reference: [Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pool)

## Monitoring and Debugging

### Real-time Inspector
Use Supabase's real-time inspector for debugging:
- Monitor real-time events
- Track subscription status
- Debug payload delivery

Reference: [Real-time Inspector](https://supabase.com/docs/guides/realtime/inspector)

## Security Considerations

### API Security
```typescript
// Secure client initialization
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY,
  {
    auth: {
      persistSession: true
    }
  }
)
```

Reference: [Security Guide](https://supabase.com/docs/guides/auth/overview#security)
