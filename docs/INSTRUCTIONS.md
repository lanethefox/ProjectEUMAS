# Implementation Instructions

This guide provides step-by-step instructions for each task in the implementation plan. Each section corresponds to tasks in `IMPLEMENTATION.md`.

## Project Setup Instructions

### Create virtual environment and install basic dependencies
1. Open terminal in project root directory
2. Run `python -m venv venv`
3. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Run `pip install --upgrade pip`

### Set up project structure
1. Create the following directories in project root:
```
eumas/
├── memory/
├── context/
├── evaluator/
├── database/
├── api/
└── tests/
```
2. Add `__init__.py` to each directory
3. Create placeholder `README.md` in each directory explaining its purpose

### Initialize git repository
1. Run `git init`
2. Create `.gitignore` with common Python patterns:
```
venv/
__pycache__/
*.pyc
.env
.pytest_cache/
*.egg-info/
dist/
build/
```

### Create requirements.txt
1. Add core dependencies:
```
fastapi>=0.68.0
uvicorn>=0.15.0
sqlalchemy>=1.4.23
alembic>=1.7.1
pytest>=6.2.5
python-dotenv>=0.19.0
pydantic>=1.8.2
```
2. Run `pip install -r requirements.txt`

### Set up pytest structure
1. Create `tests/conftest.py`
2. Add basic fixture:
```python
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def test_client():
    from your_app.main import app
    return TestClient(app)
```

## Database Implementation Instructions

### Create SQLAlchemy models
1. Create `database/models.py`
2. Define base model:
```python
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
```
3. Create Memory model:
```python
class Memory(Base):
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    priority = Column(Float, default=0.0)
    # Add other fields
```

### Implement CRUD operations
1. Create `database/crud.py`
2. Implement basic operations:
```python
def create_memory(db: Session, memory: MemoryCreate):
    db_memory = Memory(**memory.dict())
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return db_memory

def get_memory(db: Session, memory_id: int):
    return db.query(Memory).filter(Memory.id == memory_id).first()
```

### Create vector store integration
1. Install required packages:
```bash
pip install sentence-transformers faiss-cpu
```
2. Create `database/vector_store.py`:
```python
from sentence_transformers import SentenceTransformer
import faiss

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
```

## Memory System Instructions

### Implement Memory class
1. Create `memory/memory.py`
2. Define base class:
```python
class Memory:
    def __init__(self):
        self.content = ""
        self.created_at = datetime.utcnow()
        self.priority = 0.0
        self.relationships = []
        self.metadata = {}
```

### Create memory formation pipeline
1. Create `memory/pipeline.py`
2. Implement pipeline stages:
```python
class MemoryPipeline:
    def process(self, content: str):
        # 1. Clean and validate input
        cleaned = self.clean_content(content)
        
        # 2. Create memory object
        memory = Memory(content=cleaned)
        
        # 3. Calculate initial priority
        memory.priority = self.calculate_priority(memory)
        
        return memory
```

## Context Engine Instructions

### Create base Context class
1. Create `context/context.py`
2. Implement base class:
```python
class Context:
    def __init__(self):
        self.memories = []
        self.metadata = {}
        self.summary = ""
```

### Implement context retrieval
1. Create `context/retrieval.py`
2. Add retrieval methods:
```python
class ContextRetrieval:
    def get_relevant_memories(self, query: str, limit: int = 5):
        # 1. Convert query to embedding
        embedding = self.encode_query(query)
        
        # 2. Search vector store
        similar_memories = self.vector_store.search(embedding, limit)
        
        return similar_memories
```

## Evaluation System Instructions

### Create base Evaluator class
1. Create `evaluator/base.py`
2. Implement evaluator:
```python
class BaseEvaluator:
    def evaluate(self, content: str) -> Dict[str, float]:
        raise NotImplementedError
```

### Implement core metrics
1. Create `evaluator/metrics.py`
2. Add metric calculations:
```python
def calculate_emotional_depth(text: str) -> float:
    # Implement emotion detection
    pass

def calculate_creativity(text: str) -> float:
    # Implement creativity scoring
    pass
```

## API Layer Instructions

### Create FastAPI application
1. Create `api/main.py`
2. Set up basic app:
```python
from fastapi import FastAPI

app = FastAPI(title="EUMAS API")

@app.get("/")
async def root():
    return {"message": "Welcome to EUMAS API"}
```

### Implement core endpoints
1. Create `api/routers/`
2. Add memory endpoints:
```python
@router.post("/memories/")
async def create_memory(memory: MemoryCreate):
    return memory_service.create(memory)

@router.get("/memories/{memory_id}")
async def get_memory(memory_id: int):
    return memory_service.get(memory_id)
```

## Testing Instructions

### Write unit tests
1. Create test files for each component
2. Example memory test:
```python
def test_memory_creation():
    memory = Memory(content="Test content")
    assert memory.content == "Test content"
    assert memory.priority == 0.0
```

### Add integration tests
1. Create `tests/integration/`
2. Test full pipeline:
```python
def test_memory_pipeline():
    content = "Test memory"
    pipeline = MemoryPipeline()
    memory = pipeline.process(content)
    assert memory in db.query(Memory).all()
```

## Deployment Instructions

### Create Docker configuration
1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Create `docker-compose.yml`:
```yaml
version: '3'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/eumas
  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=eumas
```

## Tips for Success
- Always create a new branch for each task
- Write tests before implementing features (TDD)
- Document your code as you write it
- Ask for help if you're stuck for more than 30 minutes
- Make small, frequent commits
- Run tests before pushing code

## Common Debugging Steps
1. Check logs using `logging` module
2. Use `pdb` for Python debugging
3. Verify database connections
4. Check API responses using Swagger UI
5. Validate environment variables

Remember to:
- Keep code clean and well-documented
- Follow PEP 8 style guidelines
- Update requirements.txt when adding dependencies
- Run tests frequently
- Ask questions when unclear
