import graph_tool.all as gt
import time

def filter_graph(g, threshold):
  print(f"\nFiltering out vertices with less than {threshold} synapses ...")
  start = time.time()
  filtered_g = gt.GraphView(g, efilt=lambda e: g.ep["syn_count"][e] > threshold)
  print("Completed in ", time.time()-start, "seconds")

  print("\n=== GRAPH SUMMARY ===")
  print(f"Vertices: {filtered_g.num_vertices():,}", f"Edges: {filtered_g.num_edges():,}.")

  return filtered_g
