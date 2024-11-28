# Graph Structure

## Overview

EUMAS uses a weighted, directed graph structure to represent relationships between memories. This document details the implementation and usage of the graph system.

## Graph Representation

### Memory Node Structure
```mermaid
classDiagram
    class MemoryNode {
        +UUID id
        +String user_prompt
        +String assistant_response
        +Vector embedding
        +JSON context
        +DateTime created_at
        +DateTime updated_at
        +List~Edge~ outgoing_edges
        +List~Edge~ incoming_edges
    }
    
    class Edge {
        +UUID id
        +UUID source_id
        +List~UUID~ target_ids
        +String relationship_type
        +List~Float~ strengths
        +JSON metadata
        +DateTime created_at
    }
    
    MemoryNode "1" --> "*" Edge : has
```

### Implementation

#### Memory Node
```python
@dataclass
class MemoryNode:
    id: UUID
    user_prompt: str
    assistant_response: str
    embedding: np.ndarray
    context: dict
    created_at: datetime
    updated_at: datetime
    
    def similarity_to(self, other: 'MemoryNode') -> float:
        return 1 - cosine(self.embedding, other.embedding)
    
    def context_overlap(self, other: 'MemoryNode') -> float:
        return calculate_context_similarity(self.context, other.context)
```

#### Memory Edge
```python
@dataclass
class MemoryEdge:
    id: UUID
    source_id: UUID
    target_ids: List[UUID]
    relationship_type: str
    strengths: List[float]
    metadata: dict
    created_at: datetime
    
    def get_strongest_target(self) -> Tuple[UUID, float]:
        max_idx = np.argmax(self.strengths)
        return self.target_ids[max_idx], self.strengths[max_idx]
```

## Graph Operations

### Traversal Algorithms

#### Depth-First Search
```python
def dfs_traverse(
    start_node: UUID,
    max_depth: int = 3,
    min_strength: float = 0.5
) -> List[UUID]:
    visited = set()
    path = []
    
    def dfs(node_id: UUID, depth: int):
        if depth > max_depth or node_id in visited:
            return
        
        visited.add(node_id)
        path.append(node_id)
        
        # Get outgoing edges
        edges = get_memory_edges(node_id)
        for edge in edges:
            # Filter by strength
            strong_targets = [
                (tid, s) for tid, s in zip(edge.target_ids, edge.strengths)
                if s >= min_strength
            ]
            
            # Traverse strong connections
            for target_id, strength in strong_targets:
                dfs(target_id, depth + 1)
    
    dfs(start_node, 0)
    return path
```

#### Breadth-First Search
```python
async def bfs_traverse(
    start_node: UUID,
    max_depth: int = 3
) -> Dict[int, List[UUID]]:
    queue = deque([(start_node, 0)])
    visited = {start_node}
    levels = defaultdict(list)
    
    while queue:
        node_id, depth = queue.popleft()
        if depth > max_depth:
            continue
            
        levels[depth].append(node_id)
        
        # Get and process edges asynchronously
        edges = await get_memory_edges_async(node_id)
        for edge in edges:
            for target_id in edge.target_ids:
                if target_id not in visited:
                    visited.add(target_id)
                    queue.append((target_id, depth + 1))
    
    return levels
```

### Path Finding

#### Dijkstra's Algorithm
```python
def find_strongest_path(
    start_node: UUID,
    end_node: UUID
) -> Tuple[List[UUID], float]:
    distances = {start_node: 0}
    previous = {start_node: None}
    pq = [(0, start_node)]
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_node == end_node:
            break
            
        edges = get_memory_edges(current_node)
        for edge in edges:
            for target_id, strength in zip(edge.target_ids, edge.strengths):
                distance = current_distance + (1 - strength)
                
                if target_id not in distances or distance < distances[target_id]:
                    distances[target_id] = distance
                    previous[target_id] = current_node
                    heapq.heappush(pq, (distance, target_id))
    
    # Reconstruct path
    path = []
    current = end_node
    while current:
        path.append(current)
        current = previous.get(current)
    
    return path[::-1], distances[end_node]
```

## Graph Analysis

### Clustering Coefficient
```python
def calculate_clustering_coefficient(node_id: UUID) -> float:
    """Calculate local clustering coefficient for a node."""
    edges = get_memory_edges(node_id)
    if not edges:
        return 0.0
    
    # Get neighbors
    neighbors = set()
    for edge in edges:
        neighbors.update(edge.target_ids)
    
    if len(neighbors) < 2:
        return 0.0
    
    # Count connections between neighbors
    connections = 0
    for neighbor in neighbors:
        neighbor_edges = get_memory_edges(neighbor)
        for edge in neighbor_edges:
            connections += len(set(edge.target_ids) & neighbors)
    
    max_connections = len(neighbors) * (len(neighbors) - 1)
    return connections / max_connections if max_connections > 0 else 0.0
```

### Centrality Measures

#### PageRank
```python
def calculate_pagerank(
    damping: float = 0.85,
    max_iterations: int = 100,
    tolerance: float = 1e-6
) -> Dict[UUID, float]:
    query = """
    WITH RECURSIVE pagerank AS (
        -- Initialize
        SELECT id, 1.0::float as rank
        FROM memories
        
        UNION ALL
        
        -- Iterate
        SELECT 
            m.id,
            (1 - :damping) + :damping * COALESCE(
                SUM(p.rank * l.strength),
                0
            )
        FROM memories m
        LEFT JOIN memory_temporal_links l 
            ON m.id = ANY(l.target_memory_ids)
        JOIN pagerank p 
            ON l.source_memory_id = p.id
        GROUP BY m.id
    )
    SELECT id, rank
    FROM pagerank;
    """
    
    return execute_query(
        query,
        {'damping': damping}
    )
```

## Visualization

### Memory Graph Visualization
```python
def generate_graph_visualization(
    center_node: UUID,
    depth: int = 2
) -> Dict:
    # Traverse graph to get nodes and edges
    nodes = []
    edges = []
    
    def traverse(node_id: UUID, current_depth: int):
        if current_depth > depth:
            return
            
        # Add node
        node_data = get_memory_node(node_id)
        nodes.append({
            'id': str(node_id),
            'label': truncate_text(node_data.user_prompt),
            'title': node_data.user_prompt,
            'value': len(get_memory_edges(node_id))
        })
        
        # Add edges
        for edge in get_memory_edges(node_id):
            for target_id, strength in zip(edge.target_ids, edge.strengths):
                edges.append({
                    'from': str(node_id),
                    'to': str(target_id),
                    'value': strength,
                    'title': f'Strength: {strength:.2f}'
                })
                traverse(target_id, current_depth + 1)
    
    traverse(center_node, 0)
    
    return {
        'nodes': nodes,
        'edges': edges
    }
```

## Performance Optimization

### Edge Caching
```python
class EdgeCache:
    def __init__(self, capacity: int = 1000):
        self.cache = LRUCache(capacity)
        self.lock = asyncio.Lock()
    
    async def get_edges(self, node_id: UUID) -> List[MemoryEdge]:
        async with self.lock:
            if node_id in self.cache:
                return self.cache[node_id]
            
            edges = await fetch_edges_from_db(node_id)
            self.cache[node_id] = edges
            return edges
```

### Batch Processing
```python
async def process_edge_batch(
    edges: List[Tuple[UUID, UUID, float]]
) -> None:
    """Process a batch of edges efficiently."""
    query = """
    INSERT INTO memory_temporal_links (
        source_memory_id,
        target_memory_ids,
        relationship_type,
        cluster_strength
    )
    SELECT 
        source_id,
        ARRAY_AGG(target_id),
        'batch_processed',
        ARRAY_AGG(strength)
    FROM UNNEST($1::uuid[], $2::uuid[], $3::float[])
        AS t(source_id, target_id, strength)
    GROUP BY source_id;
    """
    
    source_ids, target_ids, strengths = zip(*edges)
    await execute_query(
        query,
        [source_ids, target_ids, strengths]
    )
```
