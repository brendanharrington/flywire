import graph_tool.all as gt
import load_graph
import filter_graph

def main():
  file_name = "data/connections.gt.gz"
  
  # Define a threshold number of synapses, to filter out low-degree nodes
  threshold = 100
  
  g = load_graph(file_name)
  filtered_g = filter_graph(g, threshold)

if __name__ == "__main__":
  main()
