def analyze_hierarchy(state):
    """Analyze the hierarchy of block states in a nested state."""
    nested_blocks = state.get_levels()
    print(f"\nNumber of levels: {len(nested_blocks)}")
    for level, block_state in enumerate(nested_blocks):
        num_blocks = len(set(block_state.get_blocks()))
        print(f"Level {level}: {num_blocks} blocks")

# def visualize_state(state, output_file):
#     """Visualize the graph with its nested state hierarchy."""
#     state.draw(output=output_file)
