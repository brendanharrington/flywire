import graph_tool.all as gt
import load_graph as lg
import filter_graph as fg
import utils as ut
import time

def main():
  g = lg.load_graph(file_name="data/connections.gt.gz")

  print("\nCalculating betweenness for graph ...")
  start = time.time()
  vertex_betweenness, edge_betweenness = gt.betweenness(g)
  print("Completed in ", time.time()-start, "seconds")

  print("\nCalculating Central Point Dominance for the Graph ...")
  cpd = gt.central_point_dominance(g, vertex_betweenness)
  print("Completed in ", time.time()-start, "seconds")

  print(f"\nCentral Point Dominance: {cpd}")

  filtered_g = fg.filter_graph(g, threshold=100)
  
  print("\nCalculating betweenness for filtered graph ...")
  start = time.time()
  f_vertex_betweenness, f_edge_betweenness = gt.betweenness(g)
  print("Completed in ", time.time()-start, "seconds")

  print("\nCalculating Central Point Dominance for the Graph ...")
  f_cpd = gt.central_point_dominance(filtered_g, f_vertex_betweenness)
  print(f"\nCentral Point Dominance: {f_cpd}")
  
if __name__ == "__main__":
  main()
