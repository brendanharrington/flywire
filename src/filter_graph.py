import graph_tool.all as gt
import time

def filter_graph(g, threshold):
  # Create a filtered graph view based on synapse count
  filtered_g = gt.GraphView(g, efilt=lambda e: g.ep["syn_count"][e] > threshold)

  # Use the filtered graph as a normal graph
  print("Filtered graph:")
  print(f"Number of vertices: {filtered_g.num_vertices()}")
  print(f"Number of edges: {filtered_g.num_edges()}")

  # Visualize or analyze the filtered graph
  for e in list(filtered_g.edges())[:5]:
      print(e, g.ep["syn_count"][e])  # Use g.ep to access edge properties

  return filtered_g
