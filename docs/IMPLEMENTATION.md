# Simplified EUMAS Implementation Guide

## Overview
EUMAS leverages GPT-4's natural intelligence for memory formation, contextual understanding, and personality development. This guide explains how to implement the core components using Supabase for real-time data management and edge functions for GPT-4 evaluations.

## Core Components

### 1. Memory System
```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
import openai
from supabase import create_client, Client

@dataclass
class Memory:
    content: str
    embedding: List[float]
    evaluation: Dict[str, any]
    affinities: Dict[str, List[str]]
    created_at: datetime
    updated_at: datetime

class MemorySystem:
    def __init__(self, supabase: Client, openai_client: openai.OpenAI):
        self.db = supabase
        self.openai = openai_client
    
    async def store_memory(self, content: str) -> Memory:
        # Get GPT-4 embedding
        embedding = await self.openai.embeddings.create(
            model="text-embedding-ada-002",
            input=content
        )
        
        # Create memory in Supabase
        memory = await self.db.table('memories').insert({
            'content': content,
            'embedding': embedding.data[0].embedding
        }).execute()
        
        # Trigger GPT-4 evaluation edge function
        evaluation = await self.db.functions.invoke(
            'memory-evaluation',
            {'content': content}
        )
        
        # Update memory with evaluation
        await self.db.table('memories').update({
            'evaluation': evaluation
        }).eq('id', memory.data[0]['id']).execute()
        
        # Discover natural affinities
        await self.db.functions.invoke(
            'affinity-discovery',
            {'memory_id': memory.data[0]['id']}
        )
        
        return memory.data[0]
```

### 2. Context Engine
```python
class ContextEngine:
    def __init__(self, supabase: Client, openai_client: openai.OpenAI):
        self.db = supabase
        self.openai = openai_client
    
    async def get_current_context(self) -> Dict:
        # Get current context state
        context = await self.db.table('contexts').select('*').order(
            'created_at', desc=True
        ).limit(1).execute()
        
        if not context.data:
            # Initialize new context if none exists
            state = await self.evaluate_initial_state()
            context = await self.db.table('contexts').insert({
                'state': state,
                'active_memories': []
            }).execute()
        
        return context.data[0]
    
    async def evaluate_initial_state(self) -> Dict:
        # Let GPT-4 evaluate initial state
        response = await self.openai.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "You are Ella, evaluating your initial state. Consider your current knowledge, mood, and goals."
            }]
        )
        return response.choices[0].message.content
```

### 3. Query Engine
```python
class QueryEngine:
    def __init__(self, supabase: Client, openai_client: openai.OpenAI):
        self.db = supabase
        self.openai = openai_client
    
    async def search_memories(self, query: str) -> List[Memory]:
        # Parallel retrieval through semantic and evaluation paths
        semantic_memories, evaluation_memories = await asyncio.gather(
            self._semantic_search(query),
            self._evaluation_based_search(query)
        )
        
        # Combine and deduplicate memories
        all_memories = {m['id']: m for m in semantic_memories + evaluation_memories}
        
        # Let GPT-4 evaluate final relevance and ordering
        response = await self.openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are Ella, evaluating which memories are most relevant to the query. Consider both semantic similarity and emotional/thematic connections."
                },
                {
                    "role": "user",
                    "content": f"Query: {query}\nMemories: {list(all_memories.values())}"
                }
            ]
        )
        
        return self.sort_by_relevance(list(all_memories.values()), response.choices[0].message.content)
    
    async def _semantic_search(self, query: str) -> List[Memory]:
        # Get query embedding
        embedding = await self.openai.embeddings.create(
            model="text-embedding-ada-002",
            input=query
        )
        
        # Find semantically similar memories
        memories = await self.db.rpc(
            'search_similar_memories',
            {
                'query_embedding': embedding.data[0].embedding,
                'similarity_threshold': 0.7,
                'match_count': 10
            }
        ).execute()
        
        return memories.data
    
    async def _evaluation_based_search(self, query: str) -> List[Memory]:
        # Get GPT-4's evaluation of the query
        evaluation = await self.openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are Ella, evaluating a query. Consider its emotional aspects, themes, and deeper meaning."
                },
                {
                    "role": "user",
                    "content": query
                }
            ]
        )
        
        # Use affinity discovery to find resonant memories
        affinity_results = await self.db.functions.invoke(
            'affinity-discovery',
            {
                'evaluation': evaluation.choices[0].message.content,
                'mode': 'query'  # Special mode for query-based affinity discovery
            }
        )
        
        return affinity_results.data
```

## Setup and Deployment

1. **Initialize Supabase Project**
   ```bash
   # Install Supabase CLI
   npm install -g supabase-cli
   
   # Login to Supabase
   supabase login
   
   # Initialize project
   supabase init
   ```

2. **Deploy Edge Functions**
   ```bash
   # Deploy memory evaluation function
   supabase functions deploy memory-evaluation
   
   # Deploy affinity discovery function
   supabase functions deploy affinity-discovery
   ```

3. **Configure Environment**
   ```bash
   # Set required environment variables
   export OPENAI_API_KEY="your-key"
   export SUPABASE_URL="your-project-url"
   export SUPABASE_KEY="your-anon-key"
   ```

4. **Run Application**
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Start the application
   python main.py
   ```

## Testing

```python
async def test_memory_creation():
    content = "I love watching sunsets by the beach!"
    memory = await memory_system.store_memory(content)
    
    assert memory['content'] == content
    assert memory['embedding'] is not None
    assert memory['evaluation'] is not None
    
    # Wait for affinity discovery
    await asyncio.sleep(2)
    affinities = await memory_system.db.table('memories').select(
        'affinities'
    ).eq('id', memory['id']).execute()
    
    assert affinities.data[0]['affinities'] is not None

async def test_context_flow():
    context = await context_engine.get_current_context()
    assert context['state'] is not None
    
    # Subscribe to context changes
    channel = memory_system.db.channel('context_flow')
    channel.on('postgres_changes', {
        'event': 'UPDATE',
        'schema': 'public',
        'table': 'contexts'
    }, lambda payload: print(f"Context updated: {payload}"))
    
    await channel.subscribe()
```

For more detailed information about the Supabase implementation, see [Supabase Integration](./engineering/supabase.md).
