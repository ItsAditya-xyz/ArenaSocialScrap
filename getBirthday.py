import json
import csv
from datetime import datetime
from collections import defaultdict

# Load JSON data from file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Process data to get birthdays by day of the year
def get_birthdays_by_day(data):
    birthdays = defaultdict(list)

    for user in data.get("users", []):
        created_on = user.get("createdOn")
        if not created_on:  # Skip if createdOn is null or missing
            print(f"Skipping user with missing createdOn: {user.get('user_address')}")
            continue
        try:
            # Attempt to parse the date and validate it
            date_obj = datetime.fromisoformat(created_on.replace("Z", "+00:00"))
            day_of_year = date_obj.strftime("%B %d")
            birthdays[day_of_year].append(user.get("user_address", "Unknown Address"))
        except ValueError:
            # Log the invalid date for debugging
            print(f"Skipping invalid date for user: {user.get('user_address')} - {created_on}")

    return birthdays

# Write birthdays to CSV
def write_birthdays_to_csv(birthdays, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Day of Year", "User Addresses"])

        for day in sorted(birthdays.keys(), key=lambda d: datetime.strptime(d, "%B %d")):
            writer.writerow([day, ", ".join(birthdays[day])])

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
