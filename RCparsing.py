import pandas as pd
import re

# Define the regex pattern for parsing APA citations
pattern = r"^(?P<authors>.+?)\s\((?P<year>\d{4})\)\.\s(?P<title>.+?)\.\s(?P<journal>[^,]+),?\s?(?P<volume>\d+)?(?:\((?P<issue>\d+)\))?,?\s?(?P<pages>\d+-\d+)?\."

# Load the Excel file
input_file = r'C:\Users\VincentKinget\Documents\ParsedAPA.xlsx'
output_file = "RCparsed_citations_output.xlsx"  # Desired output file name

# Read the Excel file
df = pd.read_excel(input_file)

# Initialize a list to store parsed data
parsed_data = []

# Parse each reference in the 'APA citation' column
for ref in df['APA citation']:
    match = re.search(pattern, str(ref))
    if match:
        parsed_data.append(match.groupdict())
    else:
        # Handle missing matches gracefully
        parsed_data.append({
            "authors": None,
            "year": None,
            "title": None,
            "journal": None,
            "volume": None,
            "issue": None,
            "pages": None
        })

# Convert parsed data to a DataFrame
parsed_df = pd.DataFrame(parsed_data)

# Save the parsed data to an Excel file
parsed_df.to_excel(output_file, index=False)

print(f"Parsed data has been saved to {output_file}")
