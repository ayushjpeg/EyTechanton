import pandas as pd

# Read the CSV files
eligibility_data = pd.read_csv('eligibilityData.csv')
extracted_data = pd.read_csv('extracted_data.csv')

# Merge the data on 'Scheme Name' and 'URL'
merged_data = pd.merge(eligibility_data, extracted_data, on=['Scheme Name', 'URL'])

# Remove duplicate tags in the 'Tags' column
def remove_duplicate_tags(tags):
    if isinstance(tags, str):
        tag_list = [tag.strip() for tag in tags.split(',')]
        unique_tags = sorted(set(tag_list))  # Remove duplicates and sort
        return ', '.join(unique_tags)
    return tags

merged_data['Tags'] = merged_data['Tags'].apply(remove_duplicate_tags)

# Save the cleaned data to a new CSV file
merged_data.to_csv('data.csv', index=False)

print("Files combined successfully with unique tags. The result is stored in 'data.csv'.")
