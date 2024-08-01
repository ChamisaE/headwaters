import re
import os

def clean_urls(input_file, output_file):
    seen_urls = set()
    pattern = re.compile(r'\d+$')  # Pattern to check if URL ends with numbers
    
    # Debugging: Print the current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                url = line.strip()
                if url not in seen_urls:
                    if pattern.search(url):  # Check if URL ends with numbers
                        seen_urls.add(url)
                        outfile.write(url + '\n')
        print(f"Cleaned URLs have been written to {output_file}")
    except FileNotFoundError as e:
        print(f"Error: {e}")

# Prompt the user for input and output file names
input_file = input("Enter the name of the input file (with URLs): ")
output_file = input("Enter the name of the output file for cleaned URLs: ")

clean_urls(input_file, output_file)