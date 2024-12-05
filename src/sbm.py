import graph_tool.all as gt
import pickle
import gzip
import time

start = time.time()

print("\nLoading connections.gt.gz ...")
g = gt.load_graph("data/connections.gt.gz")
print("Successfully loaded connections.gt.gz!")

print("\nCreating a BlockState object for the graph ...")
state = gt.minimize_blockmodel_dl(g)
print("Successfully created BlockState!")

print("\nBlockState Statistics:")
blocks = state.get_blocks()

num_nodes = state.get_N()
print(f'Total number of nodes: {num_nodes}')

num_edges = state.get_E()
print(f'Total number of edges: {num_edges}')

num_blocks = state.get_B()
print(f'Total number of blocks: {num_blocks}')

eff_num_blocks = state.get_Be()
print(f'Effective number of blocks: {eff_num_blocks}')

# Calculate entropy of the model
entropy = state.entropy()
print(f"Model entropy: {entropy}")

# Calculate the description length (DL)
dl = state.entropy(dl=True)
print(f"Model description length: {dl}") 

end = time.time()
print(f"\nExecution time: {end - start} seconds")