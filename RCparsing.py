import pandas as pd
import re

pattern = r"""
^(?P<authors>.+?)                # Match authors until the year
\s\((?P<year>\d{4})\)\.\s       # Match year in parentheses
(?P<title>.+?)\.\s              # Match title until the next period
(?P<journal>[^\d,]+)?           # Match journal name (optional, excluding digits and commas)
(?:,\s?(?P<volume>\d+))?        # Match volume number (optional)
(?:\((?P<issue>\d+)\))?         # Match issue in parentheses (optional)
(?:,\s?(?P<pages>\d+-\d+))?\.   # Match pages (optional)
"""

# Compile the regex
regex = re.compile(pattern, re.VERBOSE)
# Load the Excel file
input_file = r'C:\Users\VincentKinget\Documents\ParsedAPA.xlsx'
output_file = "RCparsed_citations_output.xlsx"  # Desired output file name

# Read the Excel file
df = pd.read_excel(input_file)

# Initialize a list to store parsed data
parsed_data = []

# Parse each reference in the 'APA citation' column
ref = df['APA citation'][1]
    
print(f"Processing: {ref}")
match = re.search(pattern, str(ref))
if match:
    print(f"Matched: {match.groupdict()}")
    parsed_data.append(match.groupdict())
else:
    # Handle missing matches gracefully
    print("no match")
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
print(parsed_df)
print("__X_X_X_X")
print(parsed_df.head())
# Save the parsed data to an Excel file
parsed_df.to_excel(output_file, index=False)

print(f"Parsed data has been saved to {output_file}")
