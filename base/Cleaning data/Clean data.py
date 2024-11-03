import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Load the tab-delimited file into a pandas DataFrame
df = pd.read_csv('EcologicalData.txt', delimiter='\t')

# Select the relevant columns
selected_columns = df[['5-1_AdultBodyMass_g', '17-1_MaxLongevity_m', 'MSW93_Genus', 'MSW93_Species']]

# Filter out rows where 'Max_Longevity' has the value -999.0 (which likely represents missing data)
filtered_data = selected_columns[selected_columns['17-1_MaxLongevity_m'] != -999.0]

# Rename the columns for better readability
filtered_data = filtered_data.rename(columns={
    '5-1_AdultBodyMass_g': 'Body_Mass',
    '17-1_MaxLongevity_m': 'Max_Longevity',
    'MSW93_Genus': 'Genus',
    'MSW93_Species': 'Species'
})

# Concatenate Genus and Species to create a new combined 'Species' column
filtered_data['Species'] = filtered_data['Genus'] + ' ' + filtered_data['Species']

# Drop the original Genus column
filtered_data = filtered_data.drop(columns=['Genus'])

# Remove rows with NaN, zeros, or infinity in 'Body_Mass' or 'Max_Longevity'
filtered_data = filtered_data.replace([np.inf, -np.inf], np.nan)  # Replace infinities with NaN
filtered_data = filtered_data.dropna(subset=['Body_Mass', 'Max_Longevity'])  # Drop rows with NaN
filtered_data = filtered_data[(filtered_data['Body_Mass'] > 0) & (filtered_data['Max_Longevity'] > 0)]  # Keep only positive values

# Apply log transformation to 'Body_Mass' and 'Max_Longevity'
filtered_data['Body_Mass'] = np.log(filtered_data['Body_Mass'])
filtered_data['Max_Longevity'] = np.log(filtered_data['Max_Longevity'])

# Save the cleaned data to a tab-delimited text file
filtered_data.to_csv('Ecological_cleaned_data.txt', sep='\t', index=False)

# Load and display the cleaned data
df_cleaned = pd.read_csv('Ecological_cleaned_data.txt', delimiter='\t')
print(df_cleaned.head())
