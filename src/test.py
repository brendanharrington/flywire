import graph_tool.all as gt

g_fly = gt.load_graph('data/connections.gt.gz')
fly_motif_graphs, fly_motif_counts = gt.motifs(g=g_fly, k=3, p=1.0, motif_list=None, return_maps=False)

print('Number of motif graphs of length 3:', len(fly_motif_graphs))
print('Counts for each graph isomorphism:', fly_motif_counts)