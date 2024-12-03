from src.data_loader import load_graph, load_state
from src.community_detection import analyze_hierarchy, visualize_state
from src.utils import print_graph_stats, generate_timestamped_filename

# import src.utils as ut

# action c
# file_name = str(input("Please enter a filename: "))
# file_extension = str(input("Please enter a file extension: "))
# timestamp_file = ut.generate_timestamped_filename(file_name,file_extension)

# print(f"The unique filename is: {timestamp_file}")

def main():
  while True:
    print("\n=== FlyWire Community Detection ===")
    print("1. Load and display graph statistics")
    print("2. Analyze community hierarchy")
    print("3. Visualize nested state")
    print("4. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
      graph = load_graph("data/connections.gt.gz")
      print_graph_stats(graph)

    elif choice == "2":
      state = load_state("data/state_nested.pkl.gz")
      analyze_hierarchy(state)

    elif choice == "3":
      state = load_state("data/state_nested.pkl.gz")
      output_file = generate_timestamped_filename("nested_state", "svg")
      visualize_state(state, f"outputs/{output_file}")
      print(f"Visualization saved as outputs/{output_file}")

    elif choice == "4":
      print("Exiting...")
      break

    else:
      print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
