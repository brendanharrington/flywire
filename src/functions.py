import graph_tool.all as gt
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import time
import pickle
import gzip
import datetime

""" 
LOOP
"""
def run_loop(g):
    while True:
        print('\n========= OPTIONS =========')
        print('[0]: Print graph')
        print('[1]: Print blockmodel graph')
        print('[q]: Quit')
        
        choice = input('\nEnter the number of what you\'d like to do: ')

        match choice:
            case '0':
                gt.graph_draw(g)
            case '1':
                state = gt.minimize_blockmodel_dl(g)
                state.draw()
            case 'q':
                print('\nQuitting...')
                break
            case _:
                print('\nInvalid entry, try again.')


""" 
PLOT
"""
def plot_PDFhist(kis):
    # input : a list of degrees, e.g., from a networkx graph G
    # output: a plot of the PDF of the degree distribution Pr(k) as a simple histogram for k>=1
    
    kmax = max(kis)

    # histogram and plot
    counts, bins = np.histogram(kis, bins=[i for i in range(kmax+2)], density=True)
    plt.bar(bins[1:-1], counts[1:], facecolor='r', alpha=0.5)    
    plt.xlabel('Degree, k')
    plt.ylabel('Pr(k)')
    plt.show()
    return

def plot_PDFsemi(kis):
    # input : a list of degrees, e.g., from a networkx graph G
    # output: a plot of the PDF of the degree distribution Pr(k) on semi-log axes for k>=1
    
    kmax = max(kis)

    # histogram and plot
    counts, bins = np.histogram(kis, bins=[i for i in range(kmax+2)], density=True)
    plt.semilogx(bins[1:-1], counts[1:], 'rs-', alpha=0.5)
    plt.xlabel('Degree, k')
    plt.ylabel('Pr(k)')
    plt.show()
    return

def plot_PDFloglog(kis):
    # input : a list of degrees, e.g., from a networkx graph G
    # output: a plot of the PDF of the degree distribution Pr(k) on log-log axes for k>=1
    
    kmax = max(kis)

    # histogram and plot
    counts, bins = np.histogram(kis, bins=[i for i in range(kmax+2)], density=True)
    plt.loglog(bins[1:-1], counts[1:], 'rs', alpha=0.5)
    plt.xlabel('Degree, k')
    plt.ylabel('Pr(k)')
    plt.show()
    return

def plot_CCDF(kis):
    # input : a list of degrees, e.g., from a networkx graph G
    # output: a plot of the CCDF of the degree distribution Pr(K>=k) for k>=1
    
    kmax = max(kis)

    # histogram and plot
    counts, bins = np.histogram(kis, bins=[i for i in range(kmax+2)], density=True)
    cumcounts = np.cumsum(counts)
    cumcounts = np.insert(cumcounts,0,0)
    plt.loglog(bins[1:-1], 1-cumcounts[1:-1], 'rs', alpha=0.5)
    plt.xlabel('Degree, k')
    plt.ylabel('Pr(K>=k)')
    plt.show()
    return

def plot_neuropil_connection_strength(g):
    all_regions, np_order, np_names, np_color = get_region_stats()

    # Filter edges with neuropil != "None"
    valid_edges = [e for e in g.edges() if g.ep.neuropil[e] != "None"]

    # Count and sum syn_count per neuropil
    neuropil_conn_cnt = {}
    neuropil_sizes = {}

    for e in valid_edges:
        neuropil = g.ep.neuropil[e]
        syn_count = g.ep.syn_count[e]
        
        if neuropil not in neuropil_conn_cnt:
            neuropil_conn_cnt[neuropil] = 0
            neuropil_sizes[neuropil] = 0
        
        neuropil_conn_cnt[neuropil] += 1  # Count connections
        neuropil_sizes[neuropil] += syn_count  # Sum synapse count

    # Sort by np_order
    np_conn_cnt = np.array([neuropil_conn_cnt.get(np, 0) for np in np_order])
    np_sizes = np.array([neuropil_sizes.get(np, 0) for np in np_order])

    # Calculate average connection strength
    np_strength = np_sizes / np_conn_cnt

    # Plot
    x_positions = np.arange(len(np_names))

    # Plot using matplotlib
    fig, ax = plt.subplots(1, 1, figsize=(20, 4))
    bars = ax.bar(x_positions, np_strength, color=np_color)

    # Format x-axis
    ax.set_xticks(x_positions)
    ax.set_xticklabels(np_names, rotation=90)
    for xtick, color in zip(ax.get_xticklabels(), np_color):
        xtick.set_color(color)

    # Set axis labels and formatting
    ax.tick_params(axis='y', labelsize=20)
    ax.set_ylabel("Average conn. strength", fontsize=24)
    ax.set_xlabel("Neuropils", fontsize=24)

    plt.show()


""" 
PRINT 
"""

def print_basic_statistics(g, flag):
    n = g.num_vertices()
    m = g.num_edges()
    k_ins_unweighted = plot_degree_distribution(g, degree_type='in', weighted=False) # add 'flag=1' as a parameter to plot a histogram
    k_ins_weighted = plot_degree_distribution(g, degree_type='in', weighted=True) # add 'flag=1' as a parameter to plot a histogram
    k_outs_unweighted = plot_degree_distribution(g, degree_type='out', weighted=False) # add 'flag=1' as a parameter to plot a histogram
    k_outs_weighted = plot_degree_distribution(g, degree_type='out', weighted=True) # add 'flag=1' as a parameter to plot a histogram

    print('\nNumber of nodes:', n, '\n',
          'Number of edges:', m, '\n',
          'Mean degree (unweighted):', np.mean(k_ins_unweighted), '\n',
          'Mean degree (weighted)', np.mean(k_ins_weighted), '\n')

    print('=== IN DEGREE ===', '\n',
          '=== UNWEIGHTED ===', '\n',
          'Maximum:', max(k_ins_unweighted), '\n',
          'Minimum:', min(k_ins_unweighted), '\n',
          '=== WEIGHTED ===', '\n',
          'Maximum:', max(k_ins_weighted), '\n',
          'Minimum:', min(k_ins_weighted), '\n')
    
    print('=== OUT DEGREE ===', '\n',
          '=== UNWEIGHTED ===', '\n',
          'Maximum:', max(k_outs_unweighted), '\n',
          'Minimum:', min(k_outs_unweighted), '\n',
          '=== WEIGHTED ===', '\n',
          'Maximum:', max(k_outs_weighted), '\n',
          'Minimum:', min(k_outs_weighted), '\n')
    
    
    print('=== TOTAL DEGREE ===', '\n',
          'UNWEIGHTED', '\n',
          'Mean:', np.mean(k_ins_unweighted), '\n',
          'Maximum:', max(k_ins_unweighted), '\n',
          'Minimum:', min(k_ins_unweighted), '\n',
          '\n',
          'WEIGHTED', '\n',
          'Mean:', np.mean(k_ins_weighted), '\n',
          'Maximum:', max(k_ins_weighted), '\n',
          'Minimum:', min(k_ins_weighted), '\n')

def print_summmary_statistics(g, version):
    n = g.num_vertices()
    m = g.num_edges()
    k_mean = m/n
    connection_probability = m / (n*(n-1))
    reciprocity = gt.edge_reciprocity(g)

    dist_unweighted, ends_unweighted = gt.pseudo_diameter(g)
    dist_weighted, ends_weighted =  gt.pseudo_diameter(g, weights=g.ep.syn_count)
    c, num_triangles, num_triples = gt.global_clustering(g, ret_counts=True)

    in_degrees = g.get_in_degrees(g.get_vertices())
    out_degrees = g.get_out_degrees(g.get_vertices())
    total_degrees = in_degrees + out_degrees
    
    print(f'\n=== v{version} ===')
    print('\nNumber of Nodes:', n)
    print('Number of Edges:', m)

    print(f'\nAverage Node Degree: {k_mean:4f}')
    print(f'\nAverage Node Degree: {k_mean:4f}')
    print('Maximum Node Degree:', max(total_degrees))
    print('Minimum Node Degree:', min(total_degrees))

    print(f'\nConnection Probability: {connection_probability:4f}')
    print(f'Reciprocity: {reciprocity:4f}\n')

    print('Pseudo-diameter:', dist_unweighted)
    print(f'Clustering coefficient: {c[0]:4f} with standard deviation {c[1]:4f}')
    print(f'Number of triangles: {num_triangles}')
    print(f'Number of triples: {num_triples}', '\n')

""" 
MISC
"""
def count_FFBL_motifs(g,flag=0):
    # input : a networkx digraph G and a binary-valued variabe flag
    # output: if flag=1, a print statement of the type {FFL,FBL} and its member edges for each found motif
    #         a list (FFL,FBL) of the counts of feed-forward and feed-back loops in G
    
    # YOUR CODE HERE
    FFL_count = 0
    FBL_count = 0

    for i in g.get_vertices():
        for j in g.get_out_neighbors(i):
            for k in g.get_out_neighbors(j):
                if k == i:
                    continue  
                
                if g.edge(i, k):
                    FFL_count += 1
                    if flag == 1:
                        print(f"FFL: ({i},{j}),({j},{k}),({i},{k})")
                
                if g.edge(k, i):
                    FBL_count += 1
                    if flag == 1:
                        print(f"FBL: ({i},{j}),({j},{k}),({k},{i})")
                        
    return FFL_count,FBL_count

def get_region_stats():

    all_regions = ["FB","EB","PB","NO","AMMC_L","AMMC_R","FLA_L","FLA_R",
               "CAN_L","CAN_R","PRW","SAD","GNG","AL_L","AL_R","LH_L","LH_R",
               "MB_CA_L","MB_CA_R","MB_PED_L","MB_PED_R","MB_VL_L","MB_VL_R","MB_ML_L",
               "MB_ML_R","BU_L","BU_R","GA_L","GA_R","LAL_L","LAL_R","SLP_L","SLP_R",
               "SIP_L","SIP_R","SMP_L","SMP_R","CRE_L","CRE_R","SCL_L","SCL_R","ICL_L","ICL_R",
               "IB_L","IB_R","ATL_L","ATL_R","VES_L","VES_R","EPA_L","EPA_R","GOR_L","GOR_R","SPS_L",
               "SPS_R","IPS_L","IPS_R","AOTU_L","AOTU_R","AVLP_L","AVLP_R","PVLP_L","PVLP_R","PLP_L","PLP_R",
               "WED_L","WED_R","ME_L","ME_R","AME_L","AME_R","LO_L","LO_R","LOP_L","LOP_R","LA_L","LA_R","OCG"]
    
    np_order = ["FB","EB","PB","NO","AMMC_L","AMMC_R","FLA_L","FLA_R","CAN_L","CAN_R","PRW","SAD","GNG",
                "AL_L","AL_R","LH_L","LH_R","MB_CA_L","MB_CA_R","MB_PED_L","MB_PED_R","MB_VL_L","MB_VL_R",
                "MB_ML_L","MB_ML_R","BU_L","BU_R","GA_L","GA_R","LAL_L","LAL_R","SLP_L","SLP_R","SIP_L",
                "SIP_R","SMP_L","SMP_R","CRE_L","CRE_R","SCL_L","SCL_R","ICL_L","ICL_R","IB_L","IB_R","ATL_L",
                "ATL_R","VES_L","VES_R","EPA_L","EPA_R","GOR_L","GOR_R","SPS_L","SPS_R","IPS_L","IPS_R",
                "AOTU_L","AOTU_R","AVLP_L","AVLP_R","PVLP_L","PVLP_R","PLP_L","PLP_R","WED_L","WED_R","ME_L",
                "ME_R","AME_L","AME_R","LO_L","LO_R","LOP_L","LOP_R","LA_L","LA_R","OCG"]
    
    np_names = ["FB","EB","PB","NO","AMMC(L)","AMMC(R)","FLA(L)","FLA(R)","CAN(L)","CAN(R)","PRW","SAD",
                "GNG","AL(L)","AL(R)","LH(L)","LH(R)","MB-CA(L)","MB-CA(R)","MB-PED(L)","MB-PED(R)",
                "MB-VL(L)","MB-VL(R)","MB-ML(L)","MB-ML(R)","BU(L)","BU(R)","GA(L)","GA(R)","LAL(L)",
                "LAL(R)","SLP(L)","SLP(R)","SIP(L)","SIP(R)","SMP(L)","SMP(R)","CRE(L)","CRE(R)","SCL(L)"
                ,"SCL(R)","ICL(L)","ICL(R)","IB(L)","IB(R)","ATL(L)","ATL(R)","VES(L)","VES(R)","EPA(L)",
                "EPA(R)","GOR(L)","GOR(R)","SPS(L)","SPS(R)","IPS(L)","IPS(R)","AOTU(L)","AOTU(R)","AVLP(L)",
                "AVLP(R)","PVLP(L)","PVLP(R)","PLP(L)","PLP(R)","WED(L)","WED(R)","ME(L)","ME(R)","AME(L)",
                "AME(R)","LO(L)","LO(R)","LOP(L)","LOP(R)","LA(L)","LA(R)","OCG"]
    
    np_color = ["#049a93","#10cac8","#36cfdc","#21adc4","#145ddc","#145ddc","#274bfe","#274bfe","#2081f2","#2081f2",
                "#513bfe","#513bfe","#603ee4","#30d2fe","#30d2fe","#fe99b8","#fe99b8","#fe9e3f","#fe9e3f","#ffa88d",
                "#ffa88d","#ffae79","#ffae79","#ff9e69","#ff9e69","#5479ef","#5479ef","#3d8ce2","#3d8ce2","#285bfa",
                "#285bfa","#fed942","#fed942","#feb13a","#feb13a","#ffda59","#ffda59","#febd3b","#febd3b","#fdb95d",
                "#fdb95d","#fbb256","#fbb256","#fe9e3e","#fe9e3e","#fead49","#fead49","#02dcc0","#02dcc0","#07c4ac",
                "#07c4ac","#00b5d3","#00b5d3","#00957e","#00957e","#0dbfc2","#0dbfc2","#4c9efe","#4c9efe","#3d89fe",
                "#3d89fe","#1a57ee","#1a57ee","#50bcfe","#50bcfe","#3b8dfe","#3b8dfe","#dd41d3","#dd41d3","#bc21a2",
                "#bc21a2","#8a34d4","#8a34d4","#bc21a2","#bc21a2","#A21A78","#A21A78","#EA4BEA"]
    
    return all_regions, np_order, np_names, np_color
