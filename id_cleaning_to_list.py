# Strip and clean
# Create a list of ids to scrape and use in the scraper

file_in_path = input("What file do you want to use? ")
state_cleaned = input("What state are you cleaning? ")

with open(file_in_path, "r") as file_in, open(f"ids_cleaned_{state_cleaned}.txt", "w") as file_out:
    cleaned_ids = []

    for line in file_in:
        line = line.strip()  # strip any whitespace from the line
        if line:  # only process non-empty lines
            parts = line.split('/')  # split the line at '/'
            if parts:  # check if the split resulted in any parts
                cleaned_id = parts[-1]  # get the last part as the ID
                cleaned_ids.append(cleaned_id)

    # Write the cleaned IDs as a list to output file
    file_out.write(str(cleaned_ids))


print(f"Cleaned IDs have been written to ids_cleaned_{state_cleaned}.txt")
