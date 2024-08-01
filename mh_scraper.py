import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

# Define the base URL
base_url = "https://www.mhvillage.com/parks/"

# Initialize an empty list to store data for each park
park_data = []

# Define the states of interest
states_of_interest = ["MT", "KS", "CO", "FL"]

# Define the park IDs
park_ids = park_ids = ['listID1', 'listID2', 'listID3']

# Initialize a requests session
session = requests.Session()

# Define request headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Initialize a dictionary to count the number of sites in each state
state_site_count = {state: 0 for state in states_of_interest}

# Iterate through the park IDs
for park_id in park_ids:
    # Construct the URL for the current park ID
    url = base_url + str(park_id) + "/"

    try:
        # Send a GET request to the URL
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")

        # Debugging: Print the HTML content for inspection
        # print(soup.prettify())

        # Extract data
        park_name_element = soup.find("h1", class_="fc-brand-mhv-red")
        park_name = park_name_element.text.strip() if park_name_element else None

        site_count_element = soup.find("div", class_="mt-3 ng-star-inserted")
        number_of_sites = None
        if site_count_element:
            number_of_sites_text = site_count_element.get_text(strip=True)
            number_of_sites_match = re.search(r'Number of Sites:\s*(\d+)', number_of_sites_text)
            number_of_sites = int(number_of_sites_match.group(1)) if number_of_sites_match else None
#working here
        # Scrape and look for peaked roofs percentage
        peaked_roofs_element = soup.find("li", string=re.compile(r"Homes w/ Peaked Roofs"))
        peaked_roofs_percentage = None
        if peaked_roofs_element:
            percentage_text = peaked_roofs_element.find("span", class_="ng-star-inserted")
            if percentage_text:
                match = re.search(r'\d+%', percentage_text.get_text(strip=True))
                peaked_roofs_percentage = match.group() if match else None
#working above

        lap_siding_element = soup.find("div", string=re.compile(r"Homes w/ Lap Siding"))
        lap_siding_percentage = None
        if lap_siding_element:
            percentage_text = lap_siding_element.find_next_sibling("span")
            if percentage_text:
                percentage_text = percentage_text.get_text(strip=True)
                match = re.search(r'\d+%', percentage_text)
                lap_siding_percentage = match.group() if match else None

        distance_to_water_element = soup.find("div", string=re.compile(r"Distance to Water"))
        distance_to_water = None
        if distance_to_water_element:
            distance_to_water_text = distance_to_water_element.find_next_sibling("span")
            if distance_to_water_text:
                distance_to_water = distance_to_water_text.get_text(strip=True)

        potential_address_elements = soup.find_all(["span", "div"])
        address = None
        for element in potential_address_elements:
            text = element.get_text(strip=True)
            if re.search(r'\b\d{1,5}\s+\w+\s+\w+\b', text):
                address = text
                break

        if address and any(state in address for state in states_of_interest):
            park_data.append({
                'Park ID': park_id,
                'Park Name': park_name,
                'Number of Sites': number_of_sites,
                'Homes w/ Peaked Roofs Percentage': peaked_roofs_percentage,
                'Homes w/ Lap Siding Percentage': lap_siding_percentage,
                'Distance to Water': distance_to_water,
                'Address': address
            })

        # Throttle requests to avoid overwhelming the server
        time.sleep(1)

    except requests.RequestException as e:
        print(f"Failed to retrieve or parse page for Park {park_id}. Error: {e}")

# Create a DataFrame from the list
df = pd.DataFrame(park_data)
print(df.head())
print(df.tail())

# Ensure the DataFrame is not empty before proceeding
if not df.empty:
    # Extract data for each state and save to separate CSV files
    for state in states_of_interest:
        state_df = df[df['Address'].str.contains(state)]
        state_df.to_csv(f'Mobile_Home_Parks_{state}.csv', index=False)

    # Display the DataFrame
    print(df)

else:
    print("No valid data was collected.")
