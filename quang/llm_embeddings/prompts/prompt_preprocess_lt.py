import pandas as pd
from datetime import datetime

# Load the CSV file
file_path = 'Dataset/preprocess_AirBnB.csv'
df = pd.read_csv(file_path, low_memory=False)

# Group the DataFrame by 'ADM_NM' and 'Reporting Month'
grouped = df.groupby(['ADM_NM', 'Reporting Month'])

# Get the list of unique group keys
group_keys = list(grouped.groups.keys())

# Function to format date from '2014-11-01' to 'November 2014'
def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    return date_obj.strftime('%B %Y')

# Open a file to write the results
with open('listing_prompts_new.txt', 'w', encoding='utf-8') as f:
    # Process each group
    for group_key in group_keys:
        location, report_month = group_key
        group_data = grouped.get_group(group_key)
        
        # Format the date
        formatted_date = format_date(report_month)
        
        # Get all non-null listing titles
        listing_titles = group_data['Listing Title'].dropna().tolist()
        
        # Add quotes around each title
        quoted_titles = [f'"{title}"' for title in listing_titles]
        
        # Calculate total properties and properties with titles
        total_properties = len(group_data)
        properties_with_titles = len(listing_titles)
        
        # Generate the report text
        report = f"""The following report gives some information about attributes and characteristics of Airbnb listings in {location} for {formatted_date}.

There are a total of {properties_with_titles} properties offer listing titles out of {total_properties} properties: {', '.join(quoted_titles)}.

Assume you are a data analyst that is familiar with BnB market. Give some comments for these AirBnB properties of {location} in {formatted_date}.

----------------------------"""
        
        # Write to file
        f.write(report + '\n')

print("Analysis has been written to listing_prompts_new.txt")