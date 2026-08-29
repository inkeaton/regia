import random
from typing import Dict
from .config import GeneratorConfig

def generate_import_graph(config: GeneratorConfig) -> Dict[str, str]:
    """
    Generates a Directed Acyclic Graph (DAG) of physical files.
    Returns a dictionary mapping filename -> source code.
    """
    n = config.n_import_nodes
    k = config.n_import_edges
    
    random.seed(config.seed)
    
    files: Dict[str, str] = {}
    
    for i in range(n):
        filename = f"file_{i}.regia"
        imports = []
        
        # To avoid cycles, a node can only import nodes with a higher index.
        available_targets = list(range(i + 1, n))
        
        # Number of edges is min(k, available_targets)
        num_edges = min(k, len(available_targets))
        
        if num_edges > 0:
            targets = random.sample(available_targets, num_edges)
            for t in targets:
                imports.append(f'IMPORT "file_{t}.regia".')
                
        # A file must have at least one PLOT to be valid Regia source.
        source = "\n".join(imports)
        source += f"""
EVENT e_{i}.
PLOT P_{i}.
    PHASE p INITIAL.
    ROLE r.
    DURING PLOT:
        WHEN e_{i}:
            END PLOT.
"""
        
        files[filename] = source
        
    return files
