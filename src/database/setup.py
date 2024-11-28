from supabase import create_client
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def setup_database():
    """Set up the database schema and extensions"""
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Enable pgvector extension
        supabase.rpc('enable_pgvector').execute()
        
        # Create tables
        create_tables(supabase)
        
        logger.info("Database setup completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error setting up database: {str(e)}")
        return False

def create_tables(supabase):
    """Create all necessary tables"""
    
    # Create interactions table
    supabase.table('interactions').create({
        'id': 'uuid default uuid_generate_v4() primary key',
        'user_prompt': 'text not null',
        'agent_reply': 'text not null',
        'memory_priority': 'float not null',
        'summary': 'text not null',
        'long_term_flag': 'boolean default false',
        'time_decay_factor': 'float default 1.0',
        'embedding': 'vector(1536)',  # OpenAI's embedding dimension
        'created_at': 'timestamp with time zone default timezone(\'utc\'::text, now())'
    }).execute()
    
    # Create interaction_metadata table
    supabase.table('interaction_metadata').create({
        'id': 'uuid default uuid_generate_v4() primary key',
        'interaction_id': 'uuid references interactions(id)',
        'session_id': 'uuid not null',
        'user_id': 'text',
        'context_tags': 'text[]',
        'tone': 'text',
        'duration': 'float',
        'created_at': 'timestamp with time zone default timezone(\'utc\'::text, now())'
    }).execute()
    
    # Create archetype_evaluations table
    supabase.table('archetype_evaluations').create({
        'id': 'uuid default uuid_generate_v4() primary key',
        'interaction_id': 'uuid references interactions(id)',
        'archetype': 'text not null',
        'metrics': 'jsonb not null',  # Stores archetype-specific metrics
        'spoken_annotation': 'text not null',
        'archetype_priority': 'float not null',
        'created_at': 'timestamp with time zone default timezone(\'utc\'::text, now())'
    }).execute()
    
    # Create memory_relationships table
    supabase.table('memory_relationships').create({
        'id': 'uuid default uuid_generate_v4() primary key',
        'source_memory_id': 'uuid references interactions(id)',
        'related_memory_id': 'uuid references interactions(id)',
        'relationship_strength': 'float not null',
        'created_at': 'timestamp with time zone default timezone(\'utc\'::text, now())'
    }).execute()
    
    # Create indexes
    create_indexes(supabase)

def create_indexes(supabase):
    """Create necessary indexes for performance"""
    
    # Create GiST index for vector similarity search
    supabase.rpc('create_vector_index', {
        'table_name': 'interactions',
        'column_name': 'embedding'
    }).execute()
    
    # Create indexes for foreign keys and frequently queried columns
    supabase.rpc('create_index', {
        'table_name': 'interaction_metadata',
        'column_name': 'interaction_id'
    }).execute()
    
    supabase.rpc('create_index', {
        'table_name': 'interaction_metadata',
        'column_name': 'session_id'
    }).execute()
    
    supabase.rpc('create_index', {
        'table_name': 'archetype_evaluations',
        'column_name': 'interaction_id'
    }).execute()
    
    supabase.rpc('create_index', {
        'table_name': 'memory_relationships',
        'column_names': ['source_memory_id', 'related_memory_id']
    }).execute()

if __name__ == "__main__":
    setup_database()
