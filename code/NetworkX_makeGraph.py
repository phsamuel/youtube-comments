import json
import networkx as nx
import os
import matplotlib.pyplot as plt
from itertools import combinations
import community as community_louvain

# Define the file path directly
file_path = "C:\\Users\\annv4\\OneDrive - University of Oklahoma\\Annie's Research Files with Dr. Samuel Cheng\\YouTube Files\\Uz0vRIcJ5kg.txt"


def parse_comments(file_path):
    print(f"Reading and parsing file: {file_path}")
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.read().split('--------------------------------------------------\n')
        for comment_block in lines:
            comment_data = {}
            lines_in_block = comment_block.strip().split('\n')
            for line in lines_in_block:
                if line.startswith('Author:') and '@' in line:
                    comment_data['author'] = line.split('@')[1].strip()
                elif line.startswith('Comment:'):
                    comment_data['comment'] = line[len('Comment:'):].strip()
                elif line.startswith('Likes:'):
                    comment_data['likes'] = int(line[len('Likes:'):].strip())
                elif line.startswith('Published At:'):
                    comment_data['published_at'] = line[len('Published At:'):].strip()
                elif line.startswith('Comment ID:'):
                    comment_data['comment_id'] = line[len('Comment ID:'):].strip()
            if 'author' in comment_data:
                data.append(comment_data)
    return data

# Process the specific file
comments_data = parse_comments(file_path)

# Save processed comments to a JSON file
json_filename = os.path.join(os.path.dirname(file_path), 'specific_comments_data.json')
with open(json_filename, 'w', encoding='utf-8') as json_file:
    json.dump(comments_data, json_file, ensure_ascii=False, indent=4)
print(f"Processed comments saved to JSON: {json_filename}")

# Create and visualize the co-commenter network graph
# (This part remains unchanged, just ensure the data loaded is from 'comments_data' instead of reading from the file again)

G = nx.Graph()
print("Creating the co-commenter network graph...")

for comment in comments_data:
    author = comment.get('author')
    if author:
        G.add_node(author)  # Ensure each author is added as a node

# Add edges between commenters
for pair in combinations([comment.get('author') for comment in comments_data if 'author' in comment], 2):
    if G.has_edge(*pair):
        G[pair[0]][pair[1]]['weight'] += 1
    else:
        G.add_edge(*pair, weight=1)

print(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

# Detect communities and visualize the network as before
# Detect communities using the Louvain method
print("Detecting communities...")
partition = community_louvain.best_partition(G)

# Visualization setup
print("Visualizing the network...")
pos = nx.spring_layout(G, k=0.1)
cmap = plt.get_cmap('viridis')
plt.figure(figsize=(10, 10))
for com in set(partition.values()):
    list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size=20, node_color=[cmap(com / len(set(partition.values())))])
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.axis('off')
plt.show()
print("Visualization complete.")