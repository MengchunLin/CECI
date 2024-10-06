import matplotlib.pyplot as plt
import pandas as pd

# Load the two Excel files to check their contents
file_1_path = 'C:/Users/yo/Desktop/CECI/02-soil_depth_statistics_with_ic.xlsx'
file_2_path = 'C:/Users/yo/Desktop/CECI/04-soil_depth_statistics_with_ic.xlsx'

# Read the Excel files to examine their structure
file_1_data = pd.read_excel(file_1_path)
file_2_data = pd.read_excel(file_2_path)

# Display the first few rows of each file to understand their structure
file_1_data_head = file_1_data.head()
file_2_data_head = file_2_data.head()

file_1_data_head, file_2_data_head


# Prepare the data for plotting
def plot_borehole_profile(data, borehole_name):
    fig, ax = plt.subplots(figsize=(6, 10))
    
    # Plot each layer as a rectangle (from Upper Depth to Lower Depth)
    for index, row in data.iterrows():
        # Define the rectangle for each layer
        rect = plt.Rectangle((0, row['Upper Depth']), 1, row['Lower Depth'] - row['Upper Depth'],
                             color=f'C{row["Type"] % 10}', edgecolor='black', label=f'Type {row["Type"]}')
        ax.add_patch(rect)
    
    # Set the labels and limits
    ax.set_xlim(0, 1)
    ax.set_ylim(data['Lower Depth'].max(), 0)  # Invert y-axis so depth goes downwards
    ax.set_xlabel('Borehole')
    ax.set_ylabel('Depth (m)')
    ax.set_title(f'Borehole Profile: {borehole_name}')
    plt.gca().invert_yaxis()
    
    # Remove x-axis ticks
    ax.set_xticks([])
    
    # Show the plot
    plt.show()

# Plot both borehole profiles
plot_borehole_profile(file_1_data[['Type', 'Upper Depth', 'Lower Depth']], "Borehole 1")
plot_borehole_profile(file_2_data[['Type', 'Upper Depth', 'Lower Depth']], "Borehole 2")
