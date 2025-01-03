import requests
import time
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

AERNA_ACTIVITY_AUTH_TOKEN = os.getenv("AERNA_ACTIVITY_AUTH_TOKEN")
def repost_thread(thread_id: str, auth_token: str) -> bool:
    """Make a repost request"""
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        'Referer': 'https://starsarena.com/',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    response = requests.post(
        'https://api.starsarena.com/threads/repost',
        headers=headers,
        json={"threadId": thread_id}
    )
    
    print(response.json())
    return response.status_code == 200

def undo_repost(thread_id: str, auth_token: str) -> bool:
    """Undo a repost"""
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
        'Referer': 'https://starsarena.com/',
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }
    
    response = requests.delete(
        f'https://api.starsarena.com/threads/repost?threadId={thread_id}',
        headers=headers
    )
    return response.status_code == 200

def main():
    # Configuration
    THREAD_ID = "bc388f27-6f9f-4c7b-915d-000504ba682e"
    AUTH_TOKEN = AERNA_ACTIVITY_AUTH_TOKEN
    WAIT_TIME = 100  # 5 minutes in seconds

    print("Starting repost automation...")
    
    try:
        while True:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Make repost
            print(f"\n[{current_time}] Attempting to repost...")
            if repost_thread(THREAD_ID, AUTH_TOKEN):
                print("✓ Repost successful")
            else:
                print("✗ Repost failed")
            
            # Wait 5 minutes
            print(f"Waiting {WAIT_TIME} seconds...")
            time.sleep(WAIT_TIME)
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Undo repost
            print(f"\n[{current_time}] Attempting to undo repost...")
            if undo_repost(THREAD_ID, AUTH_TOKEN):
                print("✓ Undo repost successful")
            else:
                print("✗ Undo repost failed")
            
            # Wait 5 minutes before next cycle
            print(f"Waiting {WAIT_TIME} seconds...")
            time.sleep(WAIT_TIME)
            
    except KeyboardInterrupt:
        print("\nStopping automation...")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()