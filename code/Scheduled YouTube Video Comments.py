# Author: Annie Vu

# 03/04/2024
# This code saves all videos from the search results in a file titled the search phrase and includes the timestamp of the search
# It runs through and takes each video from the file and saves all of the comments and replies of each video to a file titled the video ID
# If all comments are saved succesfully to its file, it adds the video to a file called "Video List" 
# Keeps track of API usage 
# Only searches for videos if the search results file doesn't exist yet
# Continues to save comments from videos in the existing search results list
# Adds number of comments/videos at the top of each text file
# Uses pagination to compile more search results
# New: Removes videos with disabled comments
# New: Instead of going through the entire search result list to find where it left off, it takes the last video ID in "Video List" and starts queueing the following video
# New: Prevent duplicate videos in search results

# You can edit the following:
# Line 31: API Key
# Under Line 84: Search Phrase, Max Search Results, and results order

import os
import time
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import pytz  # Ensure pytz is installed for timezone handling

# Initialize global variables
api_usage_counter = 0
api_daily_limit = 10000  
api_key = "xxxxxx"  # Place your actual API key here

# Initialize the YouTube API client
youtube = build('youtube', 'v3', developerKey=api_key)

# Load API usage counter from file
def load_api_usage_counter():
    try:
        with open('api_usage_counter.json', 'r') as f:
            data = json.load(f)
            return data.get('api_usage_counter', 0)
    except FileNotFoundError:
        return 0

# Save API usage counter to file
def save_api_usage_counter():
    with open('api_usage_counter.json', 'w') as f:
        json.dump({'api_usage_counter': api_usage_counter}, f)

# Adjusted initialization for the API usage counter
api_usage_counter = load_api_usage_counter()

# Modified increment_api_usage to save state
def increment_api_usage():
    global api_usage_counter
    api_usage_counter += 1
    save_api_usage_counter()

# Function to check API limit and sleep if necessary, now considers timezone
def check_api_limit_and_sleep():
    global api_usage_counter
    if api_usage_counter >= api_daily_limit:
        now = datetime.now(pytz.timezone('US/Pacific'))
        tomorrow = now + timedelta(days=1)
        reset_time = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        sleep_time = (reset_time - now).total_seconds() + 60  # Adding a 1-minute buffer
        print(f"API limit reached, sleeping for {sleep_time} seconds until reset...")
        time.sleep(sleep_time)
        api_usage_counter = 0  # Reset the counter after waiting
        save_api_usage_counter()

def save_state(video_id, next_page_token=None):
    state = {'video_id': video_id, 'next_page_token': next_page_token}
    with open('api_state.json', 'w') as f:
        json.dump(state, f)

def load_state():
    try:
        with open('api_state.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# Define search parameters
#keyword = "Ukraine War"
#keyword = "Ukraine Matters"
#keyword = "Ukraine War News"
#keyword = "Russia Ukraine"
#keyword = "Russia Ukraine war update today"
#keyword = "Russia and Ukraine Updates"
keyword = "Russia and Ukraine"
max_results = 2000
order = "relevance"  # Can be "relevance", "date", "rating", or "title"


def get_last_processed_video_id():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    video_list_path = os.path.join(current_directory, "Video List.txt")
    last_video_id = None
    try:
        with open(video_list_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith("Video ID:"):
                    last_video_id = line.strip().split("Video ID:")[1].strip()
    except FileNotFoundError:
        pass  # File does not exist
    return last_video_id

def save_search_results_to_file(search_results, keyword):
    # Format keyword for filename
    keyword_for_filename = keyword.replace(" ", "_")
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, f'{keyword_for_filename}_search_results.txt')
    search_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"Search Timestamp: {search_timestamp}\n")
        file.write(f"Search Phrase: {keyword}\n")
        file.write(f"Number of Videos: {len(search_results)}\n\n")  # Write the count of videos
        for video in search_results:
            file.write(f"Video ID: {video['video_id']}\n")
            file.write(f"Video Title: {video['title']}\n")
            file.write(f"Channel Title: {video['channelTitle']}\n")
            file.write(f"Published At: {video['publishedAt']}\n\n")

def is_video_id_in_list(video_id):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    video_list_path = os.path.join(current_directory, "Video List.txt")
    try:
        with open(video_list_path, 'r', encoding='utf-8') as file:
            for line in file:
                if video_id in line:
                    return True
    except FileNotFoundError:
        # If the file does not exist, no video IDs are in the list
        return False
    return False

def save_comments_to_file(comments, video_id):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, f'{video_id}.txt')
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(f"Number of Comments: {len(comments)}\n\n")  # Write the count of comments
        for comment in comments:
            if comment['type'] == 'comment':
                file.write(f"Author: {comment['author']}\n")
                file.write(f"Comment: {comment['comment']}\n")
                file.write(f"Likes: {comment['like_count']}\n")
                file.write(f"Published At: {comment['published_at']}\n")
                file.write(f"Comment ID: {comment['comment_id']}\n")
                file.write("--------------------------------------------------\n\n")
            elif comment['type'] == 'reply':
                file.write(f"Author: {comment['author']} (Reply to Comment ID: {comment['reply_to']})\n")
                file.write(f"Reply: {comment['comment']}\n")
                file.write(f"Likes: {comment['like_count']}\n")
                file.write(f"Published At: {comment['published_at']}\n")
                file.write(f"Comment ID: {comment['comment_id']}, Reply to ID: {comment['reply_to']}\n")
                file.write("--------------------------------------------------\n\n")
    
    print(f"Comments for video ID {video_id} saved successfully.")

def compile_and_save_search_results():
    search_response = youtube.search().list(
        q=keyword,
        part="id,snippet",
        maxResults=50,  # This is the maximum allowed by the API
        order=order,
        type='video'
    ).execute()
    
    search_results = []
    seen_video_ids = set()  # Initialize an empty set to track seen video IDs

    while True:
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                video_id = search_result["id"]["videoId"]
                if video_id not in seen_video_ids:  # Check if the video ID has been seen
                    title = search_result["snippet"]["title"]
                    channelTitle = search_result["snippet"]["channelTitle"]
                    publishedAt = search_result["snippet"]["publishedAt"]
                    search_results.append({
                        'video_id': video_id,
                        'title': title,
                        'channelTitle': channelTitle,
                        'publishedAt': publishedAt
                    })
                    seen_video_ids.add(video_id)  # Mark this video ID as seen

        # Check for nextPageToken to continue fetching results
        nextPageToken = search_response.get('nextPageToken')
        if nextPageToken:
            search_response = youtube.search().list(
                q=keyword,
                part="id,snippet",
                maxResults=50,
                order=order,
                type='video',
                pageToken=nextPageToken
            ).execute()
        else:
            break  # Exit the loop if there is no nextPageToken

    # Save compiled search results to a file
    save_search_results_to_file(search_results, keyword)
    
    # Now, pass the keyword when calling process_and_save_comments
    process_and_save_comments(search_results, keyword)  # Updated to pass 'keyword'

def process_existing_or_new_search_results():
    last_video_id = get_last_processed_video_id()
    found_last_video = last_video_id is None  # If no last video ID, start from the beginning

    keyword_for_filename = keyword.replace(" ", "_")
    current_directory = os.path.dirname(os.path.abspath(__file__))
    search_results_file_path = os.path.join(current_directory, f'{keyword_for_filename}_search_results.txt')

    if os.path.exists(search_results_file_path):
        print("Found existing search results. Processing videos starting from the next unprocessed video...")
        with open(search_results_file_path, 'r', encoding='utf-8') as file:
            search_results = []
            for line in file:
                if line.startswith("Video ID:"):
                    video_id = line.split("Video ID:")[1].strip()
                    if found_last_video:
                        title = next(file).split("Video Title:")[1].strip()
                        channelTitle = next(file).split("Channel Title:")[1].strip()
                        publishedAt = next(file).split("Published At:")[1].strip()
                        search_results.append({
                            'video_id': video_id,
                            'title': title,
                            'channelTitle': channelTitle,
                            'publishedAt': publishedAt
                        })
                    elif video_id == last_video_id:
                        found_last_video = True  # Next video will be the starting point
        process_and_save_comments(search_results, keyword)
    else:
        print("No existing search results found. Performing search...")
        compile_and_save_search_results()

def get_all_comments(api_key, video_id):
    global api_usage_counter
    youtube = build('youtube', 'v3', developerKey=api_key)
    all_comments_grouped = []
    next_page_token = None
    success = True

    try:
        while True:
            increment_api_usage()  # Track API usage
            check_api_limit_and_sleep()  # Sleep if limit is reached

            request = youtube.commentThreads().list(
                part='snippet,replies',
                videoId=video_id,
                pageToken=next_page_token,
                textFormat='plainText',
                maxResults=100
            )
            response = request.execute()

            for item in response['items']:
                top_level_comment = item['snippet']['topLevelComment']['snippet']
                comment_entry = {
                    'type': 'comment',
                    'author': top_level_comment['authorDisplayName'],
                    'comment': top_level_comment['textDisplay'],
                    'like_count': top_level_comment['likeCount'],
                    'published_at': top_level_comment['publishedAt'],
                    'comment_id': item['id']
                }
                all_comments_grouped.append(comment_entry)

                # Fetch all replies if there are more than initially returned
                if item['snippet']['totalReplyCount'] > 0:
                    all_comments_grouped.extend(fetch_all_replies_for_comment(youtube, item['id'], item['snippet']['topLevelComment']['id']))

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

    except HttpError as e:
        success = False
        if e.resp.status == 403 and 'commentsDisabled' in str(e):  # Adjust based on the actual API response for disabled comments
            print(f"Comments are disabled for video {video_id}, skipping.")
            return None, False
        elif e.resp.status == 403 and 'quotaExceeded' in str(e):  # Check for quota exceeded error
            print("API limit reached, please try again later.")
            return None, False
        else:
            print(f"An error occurred: {e}")
            return None, False

    return all_comments_grouped, success

def fetch_all_replies_for_comment(youtube, comment_thread_id, parent_id):
    replies = []
    next_page_token = None

    try:
        while True:
            replies_request = youtube.comments().list(
                part='snippet',
                parentId=comment_thread_id,
                pageToken=next_page_token,
                textFormat='plainText',
                maxResults=100
            )
            replies_response = replies_request.execute()

            for reply in replies_response['items']:
                reply_snippet = reply['snippet']
                reply_entry = {
                    'type': 'reply',
                    'author': reply_snippet['authorDisplayName'],
                    'comment': reply_snippet['textDisplay'],
                    'like_count': reply_snippet['likeCount'],
                    'published_at': reply_snippet['publishedAt'],
                    'comment_id': reply['id'],
                    'reply_to': parent_id  # Indicates the parent comment ID
                }
                replies.append(reply_entry)

            next_page_token = replies_response.get('nextPageToken')
            if not next_page_token:
                break
    except HttpError as e:
        print(f"An error occurred fetching replies: {e}")

    return replies

def add_video_to_list(video, keyword):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    video_list_path = os.path.join(current_directory, "Video List.txt")
    add_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Attempt to read the existing video list and count the videos
    video_lines = []
    num_videos = 0
    video_count_line = "Number of Videos: "
    try:
        with open(video_list_path, 'r', encoding='utf-8') as file:
            video_lines = file.readlines()
            # Find and extract the current number of videos
            for i, line in enumerate(video_lines):
                if line.startswith(video_count_line):
                    num_videos = int(line.strip().split(video_count_line)[-1])
                    break
    except FileNotFoundError:
        # File does not exist; it will be created below
        pass

    # Increment the video count since we're adding a new video
    num_videos += 1

    # Re-write the file with the updated video count and video information
    with open(video_list_path, 'w', encoding='utf-8') as file:
        file.write(f"{video_count_line}{num_videos}\n")
        if len(video_lines) > 1:  # If there were existing videos, keep their details
            # Skip the first line if it was the count line, preserve the rest
            start_index = 1 if video_lines[0].startswith(video_count_line) else 0
            file.writelines(video_lines[start_index:])
        # Now add the new video details
        file.write(f"Added Timestamp: {add_timestamp}\n")
        file.write(f"Search Phrase: {keyword}\n")
        file.write(f"Video ID: {video['video_id']}\n")
        file.write(f"Video Title: {video['title']}\n")
        file.write(f"Channel Title: {video['channelTitle']}\n")
        file.write(f"Published At: {video['publishedAt']}\n\n")

    print(f"Video ID {video['video_id']} added to list. Total videos now: {num_videos}.")

def process_and_save_comments(search_results, keyword):
    global api_usage_counter
    
    for video in search_results:
        video_id = video['video_id']
        
        # Check if video is already processed
        if not is_video_id_in_list(video_id):
            all_comments, success = get_all_comments(api_key, video_id)

            if all_comments is None:  # Indicates comments are disabled
                continue  # Skip this video entirely
            
            if success:
                save_comments_to_file(all_comments, video_id)
                add_video_to_list(video, keyword)  # This function updates "Video List" with the processed video.
                print(f'Comments saved to {video_id}.txt and video added to the list.')
                    
                # Increment the API usage counter based on the number of calls made
                # This should be adjusted based on actual API calls made
                increment_api_usage()
            
            else:
                print(f'Failed to fetch comments for video {video_id}. Skipping.')
        else:
            print(f'Video ID {video_id} has already been processed. Skipping.')
        
        # Check if approaching the API limit after each video is fully processed
        check_api_limit_and_sleep()

# Execute the workflow
process_existing_or_new_search_results()
