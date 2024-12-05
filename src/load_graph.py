import graph_tool.all as gt

def load_graph(file_name):
  print("\nLoading graph from", file_name, "...")
  g = gt.load_graph(file_name)
  print("Done.")

  print("\n=== GRAPH SUMMARY ===")
  print(f"Vertices: {g.num_vertices():,}")
  print(f"Edges: {g.num_edges():,}.")
  
  print("\n=== PROPERTY LIST ===")
  g.list_properties()

  return g