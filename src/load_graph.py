import graph_tool.all as gt
import time

def load_graph(g):
  start = time.time()
  file_name = "data/connections.gt.gz"
  g = gt.load_graph(file_name)
  end = time.time()
  print(f"Graph loaded successfully from \"{file_name}\" in ~{end - start:.4f} seconds")
  return g