import graph_tool.all as gt
import time

def load_graph(file_name):
  print("\nLoading graph from", file_name, "...")
  start = time.time()
  g = gt.load_graph(file_name)
  print("Completed in ", time.time()-start, "seconds")

  print("\n=== GRAPH SUMMARY ===")
  print(f"Vertices: {g.num_vertices():,}")
  print(f"Edges: {g.num_edges():,}.")
  
  print("\n=== PROPERTY LIST ===")
  g.list_properties()

  return g