# Author: Annie Vu

# This script is to build a graph with 2 types of nodes: comments and commenters; edges connect a commenter to their comment
# Will detect bot-like and spam behaviors and print the results in the terminal
# Refer to Figure 6 and 7 in the "Analyzing Disinformation and Crowd Manipulation Tactics on YouTube" Article
# Produces 2 csv files 'commentercomment_nodes.csv' and 'commentercomment_edges.csv' to import into Gephi
# csv files will save to the same location as the code

# You can edit the following:
# Line 125: Number of videos to process

import os
import csv
from collections import defaultdict

def parse_comments(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        author = None  # Initialize author variable
        for line in file:
            line = line.strip()
            if line.startswith('Author:') and '@' in line:
                author = line.split('@')[1].strip()
            elif line.startswith('Comment:') and author:
                comment = line[len('Comment:'):].strip()
                data.append((author, comment))
    return data

def process_files(directory_path, num_videos):
    print(f"Processing {num_videos} videos...")
    author_comments = defaultdict(list)
    comment_authors = defaultdict(set)

    files_processed = 0
    total_bot_like = 0
    total_spam = 0
    txt_files = [f for f in os.listdir(directory_path) if f.endswith('.txt')]
    txt_files = txt_files[:num_videos]  # Limit to the number of videos specified
    total_files = len(txt_files)

    for filename in txt_files:
        files_processed += 1
        print(f"Processing file {files_processed}/{total_files}: {filename}")
        file_path = os.path.join(directory_path, filename)
        comments_data = parse_comments(file_path)
        
        for author, comment in comments_data:
            author_comments[author].append(comment)
            comment_authors[comment].add(author)

    total_bot_like += detect_bot_like_behavior(comment_authors)
    total_spam += detect_spam_comments(author_comments)
    
    print("Detected behaviors:")
    print(f"Total bot-like comments detected: {total_bot_like}")
    print(f"Total spam comments detected: {total_spam}")

    # Write nodes and edges to CSV files
    write_csv_files(directory_path, author_comments, comment_authors)


def detect_bot_like_behavior(comment_authors):
    bot_like_count = 0
    print("Checking for bot-like behavior...")
    for comment, authors in comment_authors.items():
        if len(authors) > 5:  # Updated threshold for bot-like behavior
            print(f"Bot-like behavior detected for comment: '{comment}' posted by {len(authors)} authors.")
            bot_like_count += 1
    return bot_like_count

def detect_spam_comments(author_comments):
    spam_count = 0
    print("Checking for spam comments...")
    for author, comments in author_comments.items():
        comment_count = defaultdict(int)
        for comment in comments:
            comment_count[comment] += 1
        for comment, count in comment_count.items():
            if count > 5:  # Updated threshold for spam comments
                print(f"Spam comment detected: '{comment}' posted {count} times by {author}.")
                spam_count += 1
    return spam_count


def write_csv_files(directory_path, author_comments, comment_authors):
    node_csv_path = os.path.join(directory_path, 'commentercomment_nodes.csv')
    edge_csv_path = os.path.join(directory_path, 'commentercomment_edges.csv')

    with open(node_csv_path, 'w', newline='', encoding='utf-8') as node_file:
        writer = csv.writer(node_file)
        writer.writerow(['Id', 'Label', 'Type', 'Behavior'])
        for author, comments in author_comments.items():
            behaviors = set()
            for comment in comments:
                if len(comment_authors[comment]) > 5:
                    behaviors.add('Bot-like')
                if comments.count(comment) > 5:
                    behaviors.add('Spam')
            if behaviors:  # If there are any behaviors detected
                behavior_label = ' & '.join(behaviors)  # Join behaviors like 'Bot-like & Spam'
                writer.writerow([author, author, 'Commenter', behavior_label])

        for comment, authors in comment_authors.items():
            if len(authors) > 5 or any(author_comments[author].count(comment) > 5 for author in authors):
                behaviors = set()
                if len(authors) > 5:
                    behaviors.add('Bot-like')
                if any(author_comments[author].count(comment) > 5 for author in authors):
                    behaviors.add('Spam')
                behavior_label = ' & '.join(behaviors)
                writer.writerow([comment, comment, 'Comment', behavior_label])

    with open(edge_csv_path, 'w', newline='', encoding='utf-8') as edge_file:
        writer = csv.writer(edge_file)
        writer.writerow(['Source', 'Target', 'Weight'])
        for comment, authors in comment_authors.items():
            for author in authors:
                if len(authors) > 5 or author_comments[author].count(comment) > 5:
                    weight = author_comments[author].count(comment)
                    writer.writerow([author, comment, weight])

# Example usage
if __name__ == '__main__':
    directory_path = os.path.dirname(os.path.abspath(__file__))
    num_videos = 1000
    process_files(directory_path, num_videos)
