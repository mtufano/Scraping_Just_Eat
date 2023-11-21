# Let's write a Python script to open a text file, read its lines, remove duplicates, and save to a new file.

# File paths for the input and output files
input_file_path = 'areas_url.txt'
output_file_path = 'areas_urls_unique.txt'

# Reading lines from the input file
with open(input_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Removing duplicates
unique_lines = list(set(lines))

# Writing unique lines to the new file
with open(output_file_path, 'w') as file:
    file.writelines(unique_lines)

output_file_path
