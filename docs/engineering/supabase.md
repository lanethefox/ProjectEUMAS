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
  embedding vector(1536),
  metadata jsonb
);

-- Create vector index
create index on memories using ivfflat (embedding vector_cosine_ops);
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
