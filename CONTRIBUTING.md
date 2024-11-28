# Contributing to EUMAS

## Overview
EUMAS welcomes contributions that enhance Ella's memory system and personality development. This guide explains how to contribute effectively.

## Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/ProjectEUMAS.git
   cd ProjectEUMAS
   ```

2. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints for function parameters and returns
- Add docstrings to all functions and classes

### Testing
- Write tests for new features
- Run tests before submitting PR:
  ```bash
  python -m pytest tests/
  ```

### Documentation
- Update relevant documentation
- Add examples for new features
- Keep diagrams up to date

## Submitting Changes

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Write code
   - Add tests
   - Update docs

3. **Commit Changes**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

4. **Submit Pull Request**
   - Push to your fork
   - Create PR from GitHub
   - Describe changes in PR

## Areas of Focus

### Memory System
- Natural memory formation
- Affinity clustering
- Context management

### Personality Development
- Archetype evaluation
- State transitions
- Emotional understanding

### Infrastructure
- Supabase integration
- GPT-4 optimization
- Performance improvements

## Questions?
Open an issue for discussion or clarification.
