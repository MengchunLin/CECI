import pandas as pd
from openpyxl import Workbook
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    print(f"Selected file: {file_path}")
    return file_path

# Select file
selected_file = select_file()

# Read the Excel file
df = pd.read_excel(selected_file, header=0)

# Create a new workbook and select the active worksheet
new_wb = Workbook()
new_ws = new_wb.active

# Assuming your data is in the 1st, 2nd, and 13th columns (index 0, 1, and 12)
depth = df.iloc[:, 0].dropna()  # Clean depth values
#depth = np.round(depth, 2)  # Round to 2 decimal places
value = df.iloc[:, 4].dropna()  # Clean value column



# 畫圖
plot_depth=df.iloc[0]
plot_value=df.iloc[1]

# 创建一个空白图
fig, ax = plt.subplots(figsize=(6, 12))
ax.plot(value, depth, label='qc', color='blue')
ax.set_ylim(max(depth), 0)
plt.xlabel('qc')
plt.ylabel('Depth(m)')
plt.title('03 qc and soil type')

# 先保存圖片
plt.savefig('03 qc and soil type.png')

# 然後顯示圖片
plt.show()