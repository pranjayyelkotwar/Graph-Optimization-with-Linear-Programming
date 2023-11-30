import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import sys
# Load the CSV file into a Pandas DataFrame
df = pd.read_csv(sys.argv[1])

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges to the graph, avoiding duplicates
for _, row in df.iterrows():
    course = row['Course']
    professor = row['Professor']

    # Add nodes only if they don't already exist
    if not G.has_node(course):
        G.add_node(course, node_type='course')
    if not G.has_node(professor):
        G.add_node(professor, node_type='professor')

    # Add edge
    G.add_edge(professor, course)

# Separate nodes by type for coloring
professors = [node for node, data in G.nodes(data=True) if data['node_type'] == 'professor']
courses = [node for node, data in G.nodes(data=True) if data['node_type'] == 'course']

# Plot the graph with different colors for professors and courses
pos = nx.spring_layout(G)  # You can choose a different layout if needed
nx.draw_networkx_nodes(G, pos, nodelist=professors, node_color='lightblue')
nx.draw_networkx_nodes(G, pos, nodelist=courses, node_color='lightgreen')
nx.draw_networkx_edges(G, pos, edge_color='gray', width=0.5, arrowsize=10)
nx.draw_networkx_labels(G, pos, font_size=8, font_color='black', font_weight='bold')

plt.show()
