import pandas as pd
from collections import Counter
import ast

# Load the CSV file (replace 'your_file.csv' with your actual filename)
file_path = 'Dataset/preprocess_AirBnB.csv'
df = pd.read_csv(file_path, low_memory=False)

# Define attribute types
cluster_columns = [
    'Listing Type', 'Property Type', 'Cancellation Policy', 
    'Airbnb Response Time (Text)', 'Check-in Time', 'Checkout Time', 'Amenities'
]
binary_columns = ['Exact Location', 'Pets Allowed', 'Instantbook Enabled']
numerical_columns = ['Bedrooms', 'Bathrooms', 'Max Guests']

# Set this variable to control how many groups to analyze; set to None to analyze all groups
num_groups_to_analyze = None  # Set to None to analyze all groups

# Group the DataFrame by 'ADM_NM' and 'Reporting Month'
grouped = df.groupby(['ADM_NM', 'Reporting Month'])

# Get the list of unique group keys
group_keys = list(grouped.groups.keys())

# If num_groups_to_analyze is set to None, analyze all groups
if num_groups_to_analyze is None:
    num_groups_to_analyze = len(group_keys)

# Initialize the output text file
output_file = 'raw_prompts_new.txt'
with open(output_file, 'w', encoding='utf-8') as file:
    # Loop through only the specified number of groups
    for i, key in enumerate(group_keys[:num_groups_to_analyze]):
        group_data = grouped.get_group(key)
        num_rows = len(group_data)  # Total number of rows in the group
        
        # Write header information to the file
        file.write(f"\nAnalyzing group {i+1} with key: {key}\n")
        file.write(f"Total number of rows in this group: {num_rows}\n")
        
        # 1. Process Cluster Attributes (Including Amenities)
        file.write("\nCluster Attributes:\n")
        for column in cluster_columns:
            column_data = group_data[column].dropna()
            total_non_null = len(column_data)
            
            if total_non_null == 0:
                file.write(f"  Column '{column}': No information\n")
            else:
                file.write(f"  Column '{column}': Total rows with data: {total_non_null}\n")
                if column == 'Amenities':
                    # Handle amenities as a cluster attribute
                    amenities_counts = Counter()
                    for amenities_list in column_data:
                        try:
                            amenities = ast.literal_eval(amenities_list) if isinstance(amenities_list, str) else []
                            if isinstance(amenities, list):  # Ensure it's a list
                                amenities_counts.update(amenities)
                        except (ValueError, SyntaxError):
                            continue
                    for amenity, count in amenities_counts.items():
                        file.write(f"    {amenity}: {count}\n")
                else:
                    # Regular cluster attributes
                    unique_values = column_data.value_counts()
                    for value, count in unique_values.items():
                        file.write(f"    {value}: {count}\n")
        
        # 2. Process Binary Attributes
        file.write("\nBinary Attributes:\n")
        for column in binary_columns:
            column_data = group_data[column].dropna()
            total_non_null = len(column_data)
            
            if total_non_null == 0:
                file.write(f"  Column '{column}': No information\n")
            else:
                true_count = column_data.sum()
                percentage = (true_count / total_non_null) * 100
                file.write(f"  Column '{column}': Total rows with data: {total_non_null}, {percentage:.2f}% True ({true_count}/{total_non_null})\n")
        
        # 3. Process Numerical Attributes
        file.write("\nNumerical Attributes:\n")
        for column in numerical_columns:
            column_data = group_data[column].dropna()
            total_non_null = len(column_data)
            
            if total_non_null == 0:
                file.write(f"  Column '{column}': No information\n")
            else:
                stats = column_data.describe()
                file.write(f"  Column '{column}': Total rows with data: {total_non_null}\n")
                file.write(f"    Mean: {stats['mean']:.2f}\n")
                file.write(f"    Median: {column_data.median():.2f}\n")
                file.write(f"    Mode: {column_data.mode().iloc[0] if not column_data.mode().empty else 'N/A'}\n")
                file.write(f"    Min: {stats['min']:.2f}\n")
                file.write(f"    Max: {stats['max']:.2f}\n")
                file.write(f"    Std Dev: {stats['std']:.2f}\n")
        
        file.write("\n" + "-"*50 + "\n")

print(f"Analysis saved to '{output_file}'")
