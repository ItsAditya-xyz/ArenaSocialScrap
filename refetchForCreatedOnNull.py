import json
import requests
import time
from datetime import datetime
import sys
from dotenv import load_dotenv
import os

load_dotenv()

AUTH_TOKEN = os.getenv("AUTH_TOKEN")


def load_existing_data(filename="user_data_with_createdOn.json"):
    """Load the user data with createdOn field."""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_new_data(data, filename="newFinal.json"):
    """Save updated data to a new JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def fetch_creation_date(twitter_handle):
    """Fetch creation date for a user from the API."""
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

def process_null_createdOn_users():
    # Load existing data
    print("Loading user data...")
    data = load_existing_data()
    users = data.get("users", [])
    
    # Process users with null createdOn
    updated_users = []
    total_users = len(users)
    null_createdOn_users = [user for user in users if user.get("createdOn") is None]

    print(f"Found {len(null_createdOn_users)} users with null createdOn.")
    
    for i, user in enumerate(null_createdOn_users, 1):
        twitter_handle = user.get("twitter_handle")
        print(f"Processing {i}/{len(null_createdOn_users)}: {twitter_handle or 'No handle'}")

        if twitter_handle:
            # Add delay to avoid rate limiting
            time.sleep(1)
            
            # Fetch creation date
            created_on = fetch_creation_date(twitter_handle)
            if created_on:
                user["createdOn"] = created_on
                print(f"Found creation date: {created_on}")
            else:
                print("Could not fetch creation date")
        else:
            print("No Twitter handle available")
        
        updated_users.append(user)
    
    # Save updated data
    data["users"] = users
    save_new_data(data)
    print(f"Updated data saved to 'newFinal.json'.")

def main():
    try:
        process_null_createdOn_users()
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
