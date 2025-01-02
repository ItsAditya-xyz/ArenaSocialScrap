import requests
import time
import json
from typing import List, Dict

def fetch_user_data(base_url: str, batch_size: int = 50, total_users: int = 10000, rate_limit_delay: float = 0.5) -> List[Dict]:
    """
    Fetches user data from the API with pagination handling and rate limiting.
    
    Args:
        base_url (str): Base URL of the API endpoint
        batch_size (int): Number of users per request (default 15 as per API)
        total_users (int): Total number of users to fetch
        rate_limit_delay (float): Delay between requests in seconds
    
    Returns:
        List[Dict]: List of user data dictionaries
    """
    all_users = []
    num_batches = (total_users + batch_size - 1) // batch_size
    
    for batch in range(num_batches):
        offset = batch * batch_size
        
        try:
            # Construct URL with current offset
            url = f"{base_url}&offset={offset}"
            
            # Make request with proper error handling
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse response
            batch_data = response.json()
            
            # Add users from this batch
            if isinstance(batch_data, list):
                all_users.extend(batch_data)
            else:
                print(f"Warning: Unexpected response format at offset {offset}")
                continue
                
            # Progress update
            users_so_far = len(all_users)
            print(f"Fetched {users_so_far} users out of {total_users}")
            
            # Stop if we've reached the target number
            if users_so_far >= total_users:
                break
                
            # Rate limiting
            time.sleep(rate_limit_delay)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching batch at offset {offset}: {str(e)}")
            time.sleep(2)
            continue
            
        except json.JSONDecodeError as e:
            print(f"Error parsing response at offset {offset}: {str(e)}")
            continue
    
    return all_users[:total_users]  # Trim to exact number requested

def save_user_data(users: List[Dict], output_file: str = "user_data.json") -> None:
    """
    Saves the collected user data to a JSON file.
    
    Args:
        users (List[Dict]): List of user data dictionaries
        output_file (str): Output file path
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "total_users": len(users),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "users": users
        }, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(users)} users to {output_file}")

def main():
    # API configuration
    BASE_URL = "https://api.arenabook.xyz/user_summary?&limit=50&order=last_price.desc.nullslast"
    TOTAL_USERS = 10000
    BATCH_SIZE = 50
    
    # Fetch data
    print(f"Starting data collection for {TOTAL_USERS} users...")
    users = fetch_user_data(BASE_URL, BATCH_SIZE, TOTAL_USERS)
    
    # Save data
    if users:
        save_user_data(users)
        print("Data collection completed successfully")
    else:
        print("No data collected")

if __name__ == "__main__":
    main()