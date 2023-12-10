import requests

def fetch_and_sort_data(url):
    try:
        # Fetch data from the URL
        response = requests.get(url)
        response.raise_for_status()  # This will raise an error if the request failed

        # Load the JSON data
        data = response.json()

        # Sort the data based on the 'rating' key
        return sorted(data, key=lambda x: x.get('Rating', 0), reverse=False)
    except requests.RequestException as e:
        return f"An error occurred: {e}"

# URL of the JSON data
url = "https://zerotrac.github.io/leetcode_problem_rating/data.json"

# Fetch, sort, and print the data
sorted_data = fetch_and_sort_data(url)

if isinstance(sorted_data, list):
    for item in sorted_data:
        print(item)
else:
    print(sorted_data)  # Print the error message if the fetching failed
