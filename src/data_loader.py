import graph_tool.all as gt
import pickle
import gzip

def load_graph(filepath):
    """Load a Graph-tool graph from a .gt.gz file."""
    return gt.load_graph(filepath)

def load_state(filepath):
    """Load a nested state object from a gzipped pickle file."""
    with gzip.open(filepath, 'rb') as f:
        return pickle.load(f)
