import pandas as pd
from openpyxl import Workbook
import numpy as np

# Read the Excel file
file_path = 'simple kriging.xlsx'
df = pd.read_excel(file_path, header=5)

# Create a new workbook and select the active worksheet
new_wb = Workbook()
new_ws = new_wb.active

# Assuming your data is in the 4th and 5th columns (index 3 and 4)
depth = df.iloc[:, 1]
#除掉nan值
depth = depth.dropna()
#取小數點後兩位
depth = np.round(depth, 2)

value = df.iloc[:, 2]
value = value.dropna()

data_dict = dict(zip(depth, value))
print(data_dict)


# Get the number of rows in the DataFrame
num_points = len(df)

# Write numbers in column A and lookup values in column B
for i in range(1, num_points + 1):
    value = df.iloc[i-1, 2]  # Get the value from the 4th column (index 3)
    depth_value = round(0.02*i,2)
    new_ws.cell(row=i, column=1, value=depth_value)  # Write the row number in the 1st column
    if depth_value in data_dict:
        print(depth_value)
        new_ws.cell(row=i, column=2, value=data_dict[depth_value])  # Get the value from the 5th column (index 4)


    # 移動到下一行
    


# Save the modified file
new_wb.save('modified_file.xlsx')