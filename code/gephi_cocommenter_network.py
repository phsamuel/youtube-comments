# Author: Annie Vu

# This script is to build a graph with all nodes being unique commenters; edges connect a commenter to another commenter that commented on the same video(s)
# Refer to Figure 5 in the "Analyzing Disinformation and Crowd Manipulation Tactics on YouTube" Article
# Produces 2 csv files 'cocommenter_nodes.csv' and 'cocommenter_edges.csv' to import into Gephi
# csv files will save to the same location as the code

# You can edit the following:
# Line 75: Number of videos to process

import os
import csv
from itertools import combinations

def parse_comments(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        comment_data = {}
        for line in file:
            line = line.strip()
            if line.startswith('Author:') and '@' in line:
                if 'author' in comment_data:
                    data.append(comment_data)
                comment_data = {'author': line.split('@')[1].strip(), 'video_id': os.path.basename(file_path).replace('.txt', '')}
            elif line.startswith('Comment:') or line.startswith('Likes:') or line.startswith('Published At:') or line.startswith('Comment ID:'):
                key = line.split(':')[0].strip().lower()
                comment_data[key] = line[len(key)+1:].strip()
    if 'author' in comment_data:
        data.append(comment_data)
    return data

def process_files(directory_path, num_videos):
    all_commenters = set()
    edge_data = []

    node_csv_path = os.path.join(directory_path, 'cocommenter_nodes.csv')
    edge_csv_path = os.path.join(directory_path, 'cocommenter_edges.csv')
    
    files_processed = 0
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            if files_processed < num_videos:
                files_processed += 1
                comments_data = parse_comments(file_path)
                for comment in comments_data:
                    author = comment.get('author')
                    if author:
                        all_commenters.add(author)
                commenter_list = [comment.get('author') for comment in comments_data if 'author' in comment]
                video_id = comments_data[0].get('video_id') if comments_data else None
                for pair in combinations(set(commenter_list), 2):
                    edge_data.append((*pair, video_id))
                print(f"Processing file {files_processed}/{num_videos}: {filename}")
            else:
                break
    
    # Write node CSV file
    with open(node_csv_path, 'w', newline='', encoding='utf-8') as node_file:
        writer = csv.writer(node_file)
        writer.writerow(['Id', 'Label'])
        for commenter in all_commenters:
            writer.writerow([commenter, commenter])
    
    # Write edge CSV file
    with open(edge_csv_path, 'w', newline='', encoding='utf-8') as edge_file:
        writer = csv.writer(edge_file)
        writer.writerow(['Source', 'Target', 'VideoID'])
        for edge in edge_data:
            writer.writerow(edge)

# Get the directory where the script is located
if __name__ == '__main__':
    directory_path = os.path.dirname(os.path.abspath(__file__))
    num_videos = 5
    process_files(directory_path, num_videos)
