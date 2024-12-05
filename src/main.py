import graph_tool.all as gt
import load_graph as lg
import filter_graph as fg
import utils as ut

def main():
  g = lg.load_graph(file_name="data/connections.gt.gz")
  vertex_betweenness, edge_betweenness = gt.betweenness(g)
  cpd = gt.central_point_dominance(g, vertex_betweenness)
  print(f"\nCentral Point Dominance: {cpd}")

  filtered_g = fg.filter_graph(g, threshold=100)
  f_vertex_betweenness, f_edge_betweenness = gt.betweenness(g)
  f_cpd = gt.central_point_dominance(filtered_g, f_vertex_betweenness)
  print(f"\nCentral Point Dominance: {cpd}")
  
if __name__ == "__main__":
  main()
