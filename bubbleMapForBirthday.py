import json
import matplotlib.pyplot as plt
import mplcursors
from datetime import datetime
from collections import defaultdict

# Load JSON data from file
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Process data to get birthdays and user details by day of the year
def get_birthdays_by_day(data):
    birthdays = defaultdict(int)  # Use int to count occurrences
    seen_users = set()  # Track unique users by their twitter_handle

    for user in data.get("users", []):
        twitter_handle = user.get("twitter_handle")
        
        # Skip if twitter_handle is missing or already seen
        if not twitter_handle or twitter_handle in seen_users:
            continue
        
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

            # Increment the count for that day
            birthdays[day_of_year] += 1
            seen_users.add(twitter_handle)
            
        except ValueError:
            # Skip users with invalid dates without logging
            continue

    return birthdays

# Generate a bar chart to visualize the data
def plot_bar_chart(birthdays):
    # Prepare data for plotting
    days = list(birthdays.keys())
    counts = [birthdays[day] for day in days]

    # Sort by date
    sorted_days = sorted(days, key=lambda d: datetime.strptime(d, "%B %d"))
    sorted_counts = [counts[days.index(day)] for day in sorted_days]

    # Create a bar chart
    plt.figure(figsize=(12, 6))
    bars = plt.bar(sorted_days, sorted_counts, color='skyblue')

    # Customize plot
    plt.title("User Birthdays by Date")
    plt.xlabel("Month")
    plt.ylabel("Number of Birthdays")

    # Format x-axis to display only month names
    months = [datetime.strptime(day, "%B %d").strftime("%B") for day in sorted_days]
    plt.xticks(range(len(sorted_days)), months, rotation=45)

    # Annotate bars with exact date and count (on hover)
    mplcursors.cursor(bars, hover=True).connect(
        "add", lambda sel: sel.annotation.set_text(f"{sorted_days[sel.index]}\n{sorted_counts[sel.index]}"))

    # Show the plot
    plt.tight_layout()
    plt.show()

# Main function
def main():
    input_file = "user_data_with_createdOn.json"  # Replace with your JSON file path

    data = load_json(input_file)
    birthdays = get_birthdays_by_day(data)
    plot_bar_chart(birthdays)

if __name__ == "__main__":
    main()
