import gzip
import pickle

def load_state(filepath):
    """Load a nested state object from a gzipped pickle file."""
    with gzip.open(filepath, 'rb') as f:
        return pickle.load(f)