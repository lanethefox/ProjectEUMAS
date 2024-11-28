from typing import List, Dict, Any, Optional
from supabase import create_client
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseInterface:
    def __init__(self):
        self.supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
    
    async def store_interaction(self, 
                              user_prompt: str,
                              agent_reply: str,
                              memory_priority: float,
                              summary: str,
                              embedding: List[float],
                              metadata: Dict[str, Any],
                              long_term_flag: bool = False) -> Optional[str]:
        """Store a new interaction and its metadata"""
        try:
            # Insert interaction
            result = self.supabase.table('interactions').insert({
                'user_prompt': user_prompt,
                'agent_reply': agent_reply,
                'memory_priority': memory_priority,
                'summary': summary,
                'embedding': embedding,
                'long_term_flag': long_term_flag
            }).execute()
            
            interaction_id = result.data[0]['id']
            
            # Insert metadata
            self.supabase.table('interaction_metadata').insert({
                'interaction_id': interaction_id,
                'session_id': metadata['session_id'],
                'user_id': metadata.get('user_id'),
                'context_tags': metadata.get('context_tags', []),
                'tone': metadata.get('tone'),
                'duration': metadata.get('duration')
            }).execute()
            
            return interaction_id
        except Exception as e:
            logger.error(f"Error storing interaction: {str(e)}")
            return None
    
    async def store_archetype_evaluation(self,
                                       interaction_id: str,
                                       archetype: str,
                                       metrics: Dict[str, float],
                                       spoken_annotation: str,
                                       archetype_priority: float) -> bool:
        """Store archetype evaluation for an interaction"""
        try:
            self.supabase.table('archetype_evaluations').insert({
                'interaction_id': interaction_id,
                'archetype': archetype,
                'metrics': metrics,
                'spoken_annotation': spoken_annotation,
                'archetype_priority': archetype_priority
            }).execute()
            return True
        except Exception as e:
            logger.error(f"Error storing archetype evaluation: {str(e)}")
            return False
    
    async def store_memory_relationship(self,
                                      source_memory_id: str,
                                      related_memory_id: str,
                                      relationship_strength: float) -> bool:
        """Store relationship between two memories"""
        try:
            self.supabase.table('memory_relationships').insert({
                'source_memory_id': source_memory_id,
                'related_memory_id': related_memory_id,
                'relationship_strength': relationship_strength
            }).execute()
            return True
        except Exception as e:
            logger.error(f"Error storing memory relationship: {str(e)}")
            return False
    
    async def find_similar_memories(self,
                                  embedding: List[float],
                                  limit: int = 5,
                                  threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Find similar memories using vector similarity search"""
        try:
            result = self.supabase.rpc(
                'match_memories',
                {
                    'query_embedding': embedding,
                    'match_threshold': threshold,
                    'match_count': limit
                }
            ).execute()
            
            return result.data
        except Exception as e:
            logger.error(f"Error finding similar memories: {str(e)}")
            return []
    
    async def get_memory_by_id(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific memory by ID"""
        try:
            result = self.supabase.table('interactions').select(
                '*',
                count='exact'
            ).eq('id', memory_id).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error retrieving memory: {str(e)}")
            return None
