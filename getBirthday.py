import json
import csv
from datetime import datetime
from collections import defaultdict

# Load JSON data from file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Process data to get birthdays and user details by day of the year
def get_birthdays_by_day(data):
    birthdays = defaultdict(list)
    seen_users = {}  # Dictionary to track users by their twitter_handle

    for user in data.get("users", []):
        created_on = user.get("createdOn")
        if not created_on:  # Skip if createdOn is null or missing
            continue
        
        # Remove 'Z' from the timestamp to avoid issues with datetime.fromisoformat
        created_on = created_on.replace("Z", "+00:00")
        
        try:
            date_obj = datetime.fromisoformat(created_on)
            day_of_year = date_obj.strftime("%B %d")

            # If February 29th is found, move the user to March 1st
            if day_of_year == "February 29":
                day_of_year = "March 01"  # Move to March 1st

            twitter_handle = user.get("twitter_handle", "N/A")
            twitter_username = user.get("twitter_username", "N/A")
            last_price = user.get("last_price", "N/A")  # Assuming 'last_price' exists in the data
            created_on = user.get("createdOn", "N/A")
            
            # Check if the user is already added by their twitter_handle
            if twitter_handle not in seen_users:
                user_details = {
                    "twitter_handle": twitter_handle,
                    "twitter_username": twitter_username,
                    "last_price": last_price,
                    "createdOn": created_on
                }
                # Add the user to the day's list
                birthdays[day_of_year].append(user_details)
                # Mark the user as seen
                seen_users[twitter_handle] = True

        except ValueError:
            # Skip users with invalid dates without logging
            continue

    return birthdays

# Write birthdays and user details to CSV
def write_birthdays_to_csv(birthdays, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Day of Year", "Twitter Handle", "Twitter Username", "Last Price", "Created On"])

        valid_days = []

        # Validate and sort days
        for day in birthdays.keys():
            try:
                # Validate date format
                datetime.strptime(day, "%B %d")
                valid_days.append(day)
            except ValueError:
                continue  # Ignore invalid days

        # Write valid days to CSV
        for day in sorted(valid_days, key=lambda d: datetime.strptime(d, "%B %d")):
            writer.writerow([day])
            for user in birthdays[day]:
                writer.writerow([
                    user["twitter_handle"],
                    user["twitter_username"],
                    user["last_price"],
                    user["createdOn"]
                ])

# Main function
def main():
    input_file = "user_data_with_createdOn.json"  # Replace with your JSON file path
    output_file = "birthdays_by_day.csv"

    data = load_json(input_file)
    birthdays = get_birthdays_by_day(data)
    write_birthdays_to_csv(birthdays, output_file)

    print(f"CSV file '{output_file}' created successfully.")

if __name__ == "__main__":
    main()
