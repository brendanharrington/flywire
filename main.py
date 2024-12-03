import graph_tool.all as gt
import numpy as np
import src.utils as ut
import src.data_loader as dl
import src.community_detection as cd

def main():
  g = gt.Graph()
  g_loaded = False
  state_loaded = False

  while True:
    print("\n=== FlyWire Community Detection ===")
    print("1. Load and display graph statistics")
    print("2. Analyze community hierarchy")
    print("3. Refine blockmodel with merge-split MCMC")
    print("4. Print CCDF")
    print("5. Quit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
      if g_loaded:
        print("\nGraph already loaded!")
      else:
        g = dl.load_graph("data/connections.gt.gz")
        ut.print_graph_stats(g)
        g_loaded = True

    elif choice == "2":
      if state_loaded:
        print("\n State already loaded!")
      elif g_loaded:
        state = dl.load_state("data/state_nested.pkl.gz")
        print("\nSUMMARY OF STATE_NESTED.PKL.GZ")
        state.print_summary()
        state_loaded = True
      else:
        print("Graph not loaded yet!")
      
    elif choice == "3":
      if state_loaded:
        # S1 = state.entropy()

        # for i in range(1000): # this should be sufficiently large
        #     state.multiflip_mcmc_sweep(beta=np.inf, niter=10)

        # S2 = state.entropy()

        # print("Improvement:", S2 - S1)
      else:
        print("State not loaded yet!")

    elif choice == "4":
      ut.plot_ccdf(g)

    elif choice == "5":
      print("\nExiting...")
      break

    else:
      print("Invalid choice. Please try again.")

if __name__ == "__main__":
  main()
