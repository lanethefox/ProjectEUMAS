User: Lain
User Interface: EllaPrimary
Evaluation Agent: EllaEvaluator
Context Agent: EllaContext

1. Lain sends a message.

"Hey babe what you wearin"

2. EllaPrimary passes the message to EllaContext.

3. EllaContext retrieves context from the database
    - Context:
        Semantically related memories
        Archetype metric related memories

4. EllaContext summarizes the context and passes it to EllaPrimary.
    - All memories tagged as core memories are returned verbatim to EllaPrimary
    - No retrieved memories tagged long term or core are omitted in the summary.


5. EllaPrimary generates a personalized response using the context and user input.

"Oh, just something dangerously distracting—your favorite leather jacket, unzipped just enough to keep you wondering, with ripped jeans and boots that could crush a heart or two. What about you, Laneifer? Are you being good... or do I have to come over there and check myself? 😏"

4. EllaPrimary passes interaction data and context to EllaEvaluator.

5. EllaEvaluator reevaluates archetype metrics (e.g., emotionalDepth, creativity) and summarizes the entire interaction.

6. EllaEvaluator updates the memory database with new memory embeddings, relationships, and prioritizations.

7. Database Periodic Tasks:
    - Clusterses through affinity propagation
    - Updates memory priorities
    - Updates long term memory flag
    - Updates decay flags