import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances

# Load the two uploaded Excel files
file1_path = 'C:/Users/Janet/Desktop/borehole_data/02output.xlsx'
file2_path = 'C:/Users/Janet/Desktop/borehole_data/04output.xlsx'

# Read both datasets
data1 = pd.read_excel(file1_path)
data2 = pd.read_excel(file2_path)

# Select relevant soil properties for comparison
features = ['qc (MPa)', 'fs (MPa)', 'u (MPa)', 'qt(MPa)', 'ϒ(KN/m3)', 'Bq', 'σv(kPa)', 'σ\'v0(kPa)', 'Ic']

# Filter out rows with missing values in the selected features
data1_filtered = data1[features].dropna()
data2_filtered = data2[features].dropna()

# Standardize the data to bring all features to the same scale
scaler = StandardScaler()
data1_scaled = scaler.fit_transform(data1_filtered)
data2_scaled = scaler.transform(data2_filtered)

# Compute pairwise Euclidean distances between all depth layers
distances_optimized = euclidean_distances(data1_scaled, data2_scaled)

# Find the index of the minimum distance for each layer in data1 (most similar layer in data2)
closest_matches_optimized = distances_optimized.argmin(axis=1)

# Get the corresponding depth and soil properties for the closest matches
data1_closest_match = data1_filtered.iloc[closest_matches_optimized]

# Combine data1 depth with corresponding closest match from data2 for comparison
comparison_df = pd.DataFrame({
    'Data1 Depth (m)': data1_filtered.index,
    'Data2 Closest Match Depth (m)': data2_filtered.index[closest_matches_optimized],
    'Distance': distances_optimized.min(axis=1)
})

# Display the comparison result
comparison_df.head()

# If you want to save the full comparison result to a file:
comparison_df.to_csv("C:/Users/Janet/Desktop/soil_comparison_results.csv", index=False)
