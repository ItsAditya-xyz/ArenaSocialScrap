import json
import requests
import time
from datetime import datetime
import sys
from dotenv import load_dotenv
import os

load_dotenv()



AUTH_TOKEN = os.getenv("AUTH_TOKEN")
def load_existing_data(filename="user_data.json"):
    """Load the original user data"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_progress_data(filename="user_data_with_createdOn.json"):
    """Load existing progress if any"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_progress(data, filename="user_data_with_createdOn.json"):
    """Save current progress"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def fetch_creation_date(twitter_handle):
    """Fetch creation date for a user from the API"""
    if not twitter_handle:
        return None

    url = f"https://api.starsarena.com/user/handle?handle={twitter_handle}"
    
    try:

        headers = {
            "Authorization": f"Bearer {AUTH_TOKEN}",
            "Content-Type": "application/json",
            "Referer": "https://arena.social/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        return data.get('user', {}).get('createdOn')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {twitter_handle}: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing response for {twitter_handle}: {str(e)}")
        return None
    
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

def process_users():
    # Load original data
    print("Loading original user data...")
    original_data = load_existing_data()
    
    # Load existing progress if any
    progress_data = load_progress_data()
    
    if progress_data:
        print("Found existing progress, continuing from where we left off...")
        working_data = progress_data
    else:
        print("Starting fresh...")
        working_data = {
            "total_users": original_data["total_users"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "users": []
        }
    
    # Create set of handles we've already processed
    processed_handles = {user.get('twitter_handle') for user in working_data['users']}
    
    # Process each user
    total_users = len(original_data['users'])
    
    for i, user in enumerate(original_data['users'], 1):
        twitter_handle = user.get('twitter_handle')
        
        # Skip if we've already processed this user
        if twitter_handle in processed_handles:
            continue
            
        print(f"Processing {i}/{total_users}: {twitter_handle or 'No handle'}")
        
        # Copy original user data
        user_data = user.copy()
        
        if twitter_handle:
            # Add delay to avoid rate limiting
            time.sleep(1)
            
            # Fetch creation date
            created_on = fetch_creation_date(twitter_handle)
            if created_on:
                user_data['createdOn'] = created_on
                print(f"Found creation date: {created_on}")
            else:
                user_data['createdOn'] = None
                print("Could not fetch creation date")
        else:
            user_data['createdOn'] = None
            print("No Twitter handle available")
        
        # Add to working data
        working_data['users'].append(user_data)
        
        # Save progress every 10 users
        if i % 10 == 0:
            save_progress(working_data)
            print(f"Progress saved: {i}/{total_users} users processed")
    
    # Final save
    save_progress(working_data)
    print("All users processed!")

def main():
    try:
        process_users()
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Progress has been saved.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()