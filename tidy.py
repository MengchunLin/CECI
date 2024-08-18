import pandas as pd
from openpyxl import Workbook
import numpy as np
import tkinter as tk
from tkinter import filedialog

def select_file():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    file_path = filedialog.askopenfilename()  # 打开文件选择对话框
    print(f"Selected file: {file_path}")
    
    return file_path

# 使用文件选择器选择文件路径
selected_file = select_file()

# 这里你可以将 selected_file 用作读取 Excel 文件的路径


# Read the Excel file
# file_path = 'simple kriging.xlsx'
df = pd.read_excel(selected_file, header=0)

# Create a new workbook and select the active worksheet
new_wb = Workbook()
new_ws = new_wb.active

# Assuming your data is in the 4th and 5th columns (index 3 and 4)
depth = df.iloc[:, 0].dropna()  # Clean depth values
depth = np.round(depth, 2)  # Round to 2 decimal places

value = df.iloc[:, 1].dropna()  # Clean value column

data_dict = dict(zip(depth, value))

# Get the number of rows in the DataFrame
num_points = int(max(depth)/0.02)


# Write numbers in column A and lookup values in column B
for i in range(1, num_points + 1):
    depth_value = round(0.02*i, 2)  # Calculate depth value
    new_ws.cell(row=i, column=1, value=depth_value)  # Write depth in the 1st column
    if depth_value in data_dict:
        new_ws.cell(row=i, column=2, value=data_dict[depth_value])  # Write value in the 2nd column

# 将工作表中的数据读取到pandas DataFrame中
new_df = pd.DataFrame(new_ws.values)

# 对缺失值进行插值
new_df[1] = new_df[1].interpolate()

# 将插值后的数据写回到工作表
for i in range(1, num_points + 1):
    new_ws.cell(row=i, column=2, value=new_df.iloc[i-1, 1])

# Save the modified file
new_wb.save('modified_file.xlsx')
