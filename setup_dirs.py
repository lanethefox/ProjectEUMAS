import os

directories = [
    'src',
    'src/core',
    'src/database',
    'src/models',
    'src/archetypes',
    'src/utils',
    'tests'
]

for dir in directories:
    os.makedirs(os.path.join(os.getcwd(), dir), exist_ok=True)
