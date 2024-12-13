import graph_tool.all as gt
import matplotlib.pyplot as plt
import numpy as np

import functions as fnc

def main():
    version = '783'
    file_name = 'data/connections-v' + version + '.gt.gz'

    g= gt.load_graph(file_name=file_name)
    
    fnc.print_summmary_statistics(g, version)

if __name__ == "__main__":
    main()