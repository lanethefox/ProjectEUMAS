"""
EUMAS Core Implementation

This module implements the core EUMAS (Ella Unified Memory Augmentation System) functionality.
It uses GPT-4's natural understanding to create a dynamic, self-organizing network of memories.
"""

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
from uuid import UUID, uuid4

import openai
from supabase import Client, create_client

@dataclass
class Memory:
    """A single memory in the system"""
    id: UUID
    content: str
    timestamp: datetime
    evaluations: List[Dict[str, any]]
    context: Dict[str, any]
    affinities: List[Dict[str, any]]

@dataclass
class Context:
    """Current conversation context"""
    messages: List[Dict[str, any]]
    memories: List[Memory]
    emotional_state: Dict[str, any]
    focus_areas: List[str]
    active_archetypes: List[str]

@dataclass
class Query:
    """A memory query"""
    text: str
    intent: Dict[str, any]
    context: Dict[str, any]
    relevance_threshold: float = 0.7
    max_results: int = 10

@dataclass
class QueryResult:
    """Results of a memory query"""
    memories: List[Memory]
    affinity_groups: List[Dict[str, any]]
    reasoning: str

class Ella:
    """Core intelligence for EUMAS"""
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        self.system_prompt = self._load_system_prompt()
        self.archetype_prompts = self._load_archetype_prompts()
    
    async def reflect(
        self,
        content: str,
        aspect_prompt: str
    ) -> Dict[str, any]:
        """Reflect on content through a specific aspect"""
        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": aspect_prompt},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content
    
    async def understand_query(
        self,
        query: str,
        context: Context
    ) -> Dict[str, any]:
        """Understand a query in current context"""
        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Context: {context}"},
                {"role": "user", "content": f"Query: {query}"}
            ]
        )
        return response.choices[0].message.content
    
    async def find_memory_groups(
        self,
        memories: List[Memory]
    ) -> List[Dict[str, any]]:
        """Find natural groupings of memories"""
        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Group these memories naturally: {memories}"}
            ]
        )
        return response.choices[0].message.content
    
    async def explain_results(
        self,
        query: str,
        memories: List[Memory],
        groups: List[Dict]
    ) -> str:
        """Explain why memories are relevant"""
        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Query: {query}"},
                {"role": "user", "content": f"Explain these memory groups: {groups}"}
            ]
        )
        return response.choices[0].message.content
    
    def _load_system_prompt(self) -> str:
        """Load Ella's system prompt"""
        # TODO: Load from config
        return """You are Ella, an AI with a rich personality and emotional depth.
                 You help maintain and connect memories through natural understanding."""
    
    def _load_archetype_prompts(self) -> Dict[str, str]:
        """Load archetype prompts"""
        # TODO: Load from config
        return {
            "emotional": "How does this resonate emotionally?",
            "creative": "What creative elements exist here?",
            "explorative": "What possibilities does this spark?",
            "historical": "How does this connect to past experiences?",
            "research": "What knowledge is relevant here?",
            "analytical": "How can this be logically understood?",
            "protective": "What risks or concerns exist?"
        }

class EUMAS:
    """Main EUMAS system"""
    def __init__(
        self,
        supabase_url: str,
        supabase_key: str,
        openai_key: str
    ):
        # Initialize components
        self.db = create_client(supabase_url, supabase_key)
        openai.api_key = openai_key
        self.ella = Ella()
        
        # Initialize state
        self.context = Context(
            messages=[],
            memories=[],
            emotional_state={},
            focus_areas=[],
            active_archetypes=[]
        )
    
    async def process_message(self, message: str) -> Context:
        """Process a new message and update context"""
        # Add message to context
        self.context.messages.append({
            'content': message,
            'timestamp': datetime.now()
        })
        
        # Let Ella understand the context
        understanding = await self.ella.understand_query(
            message,
            self.context
        )
        
        # Update context
        self.context = Context(
            messages=self.context.messages[-10:],
            memories=understanding.relevant_memories,
            emotional_state=understanding.emotional_state,
            focus_areas=understanding.focus_areas,
            active_archetypes=understanding.active_archetypes
        )
        
        return self.context
    
    async def create_memory(self, content: str) -> Memory:
        """Create a new memory"""
        # Create memory object
        memory = Memory(
            id=uuid4(),
            content=content,
            timestamp=datetime.now(),
            evaluations=[],
            context=self.context.__dict__,
            affinities=[]
        )
        
        # Get Ella's evaluations
        for aspect, prompt in self.ella.archetype_prompts.items():
            eval = await self.ella.reflect(content, prompt)
            memory.evaluations.append({
                'aspect': aspect,
                'evaluation': eval
            })
        
        # Store in database
        await self.db.table('memories').insert(memory.__dict__)
        
        # Find and create affinity links
        similar = await self.find_similar_memories(memory)
        for other in similar:
            affinity = await self.calculate_affinity(memory, other)
            memory.affinities.append(affinity)
            await self.db.table('memory_links').insert({
                'source_id': memory.id,
                'target_id': other.id,
                'weight': affinity['strength']
            })
        
        return memory
    
    async def search_memories(
        self,
        query: str,
        context: Optional[Context] = None
    ) -> QueryResult:
        """Search for memories"""
        # Let Ella understand the query
        understanding = await self.ella.understand_query(
            query,
            context or self.context
        )
        
        # Find relevant memories
        memories = await self.db.table('memories').select('*').execute()
        relevant = await self.ella.sort_by_relevance(
            memories,
            understanding
        )
        
        # Group by affinity
        groups = await self.ella.find_memory_groups(relevant)
        
        # Get explanation
        reasoning = await self.ella.explain_results(
            query,
            relevant,
            groups
        )
        
        return QueryResult(
            memories=relevant,
            affinity_groups=groups,
            reasoning=reasoning
        )
    
    async def calculate_affinity(
        self,
        memory1: Memory,
        memory2: Memory
    ) -> Dict[str, any]:
        """Calculate natural affinity between memories"""
        understanding = await self.ella.reflect(
            f"Compare: {memory1.content} and {memory2.content}",
            "How are these memories related?"
        )
        return {
            'type': understanding['relationship_type'],
            'strength': understanding['strength'],
            'explanation': understanding['explanation']
        }
    
    async def find_similar_memories(
        self,
        memory: Memory,
        limit: int = 5
    ) -> List[Memory]:
        """Find similar memories"""
        memories = await self.db.table('memories').select('*').execute()
        return await self.ella.sort_by_relevance(
            memories,
            {'content': memory.content}
        )[:limit]
