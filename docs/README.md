# EUMAS Documentation

Welcome to the EUMAS documentation. This guide explains how EUMAS enables natural personality development through simple yet effective memory management and context understanding.

## Core Documentation

### Theory and Design
- [Theoretical Foundation](theory/README.md): Core concepts and principles
  - [Memory Models](theory/memory-models.md): How memories shape personality
  - [Natural Growth](theory/natural-growth.md): Personality development through experience

### Components
- [Core Components](components/README.md): Essential system elements
  - [Memory Management](components/memory.md): Simple, natural memory handling
  - [Context Engine](components/context.md): Understanding conversational context
  - [Archetype System](components/archetypes.md): Natural personality traits
  - [Query Engine](components/query.md): Memory retrieval through natural understanding

### Implementation
- [Implementation Guide](IMPLEMENTATION.md): Getting started with EUMAS
- [Contributing Guide](../CONTRIBUTING.md): How to contribute to the project

## System Architecture

### Core Components
- **Lain**: User/client interface
- **EllaPrimary**: Main interaction agent
- **EllaEvaluator**: Memory and metric evaluation
- **EllaContext**: Context management and retrieval

### System Flow
1. **User Input Phase**
   - User (Lain) initiates interaction with message
   - EllaPrimary receives and processes initial input
   - Message forwarded to context processing pipeline

2. **Context Processing Phase**
   - EllaPrimary delegates to EllaContext
   - EllaContext performs database retrieval:
     - Semantically related memories
     - Archetype metric related memories
   - Context summarization with special handling:
     - Core memories passed verbatim to EllaPrimary
     - All long-term and core memories included
     - Context synthesized for coherent understanding

3. **Response Generation Phase**
   - EllaPrimary generates personalized response using:
     - Original user input context
     - Retrieved memory context
     - Current archetype metric states
   - Response maintains personality consistency
   - Interaction data captured for evaluation

4. **Evaluation and Memory Phase**
   - Full interaction context passed to EllaEvaluator
   - EllaEvaluator performs comprehensive analysis:
     - Reevaluates all archetype metrics
     - Generates interaction summaries
     - Creates new memory embeddings
     - Establishes relationship mappings
     - Assigns memory priorities

5. **Database Maintenance**
   - Periodic background tasks:
     - Memory clustering through affinity propagation
     - Priority score updates
     - Long-term memory flag management
     - Decay flag processing
     - Relationship graph optimization

## Quick Links
- [Project Intent](../INTENT.md): Core philosophy and goals
- [Changelog](../CHANGELOG.md): Project history and updates

## Key Concepts

### Natural Memory Formation
- Memories form naturally through conversations
- Context drives understanding and connections
- Simple storage with rich meaning

### Personality Development
- Emerges from real interactions
- Shaped by experiences and memories
- Maintains consistency while allowing growth

### Implementation Philosophy
- Leverage GPT-4's natural understanding
- Keep technical complexity minimal
- Focus on genuine interactions
