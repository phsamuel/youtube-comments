# Author: Annie Vu

# This script is to build a graph with 2 types of nodes: videos and commenters; edges connect a commenter to videos they commented on
# Refer to Figure 4 in the "Analyzing Disinformation and Crowd Manipulation Tactics on YouTube" Article
# Produces 2 csv files 'videocommenter_nodes.csv' and 'videocommenter_edges.csv' to import into Gephi
# csv files will save to the same location as the code

# You can edit the following:
# Line 71: Number of videos to process

import os
import csv

def parse_comments(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line.startswith('Author:') and '@' in line:
                author = line.split('@')[1].strip()
                if author:
                    data.append(author)  # Collect only author name
    return data

def process_files(directory_path, num_videos):
    print(f"Processing {num_videos} videos...")
    all_commenters = set()
    all_videos = set()
    edges = set()  # Using a set to avoid duplicate edges

    txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
    txt_files = txt_files[:num_videos]  # Limit to the number of videos specified
    total_files = len(txt_files)
    files_processed = 0

    for filename in txt_files:
        files_processed += 1
        print(f"Processing file {files_processed}/{total_files}: {filename}")
        
        video_id = filename.replace('.txt', '')
        all_videos.add(video_id)  # Add video ID to set
        file_path = os.path.join(directory_path, filename)
        commenters = parse_comments(file_path)
        
        for commenter in commenters:
            all_commenters.add(commenter)
            edges.add((commenter, video_id))  # Create an edge from commenter to video


    # Write nodes and edges to CSV files
    node_csv_path = os.path.join(directory_path, 'videocommenter_nodes.csv')
    edge_csv_path = os.path.join(directory_path, 'videocommenter_edges.csv')

    with open(node_csv_path, 'w', newline='', encoding='utf-8') as node_file:
        writer = csv.writer(node_file)
        writer.writerow(['Id', 'Label', 'Type'])
        for video_id in all_videos:
            writer.writerow([video_id, video_id, 'Video'])
        for commenter in all_commenters:
            writer.writerow([commenter, commenter, 'Commenter'])

    with open(edge_csv_path, 'w', newline='', encoding='utf-8') as edge_file:
        writer = csv.writer(edge_file)
        writer.writerow(['Source', 'Target'])
        for edge in edges:
            writer.writerow([edge[0], edge[1]])

# Example usage
if __name__ == '__main__':
    directory_path = os.path.dirname(os.path.abspath(__file__))
    num_videos = 10
    process_files(directory_path, num_videos)
