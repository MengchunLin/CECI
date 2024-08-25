import pandas as pd
from openpyxl import Workbook
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt


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
# depth = df.iloc[:, 0].dropna()  # Clean depth values
# #depth = np.round(depth, 2)  # Round to 2 decimal places
# value = df.iloc[:, 4].dropna()  # Clean value column



# 畫圖
plot_depth_old=df.iloc[:,0]
plot_value_old=df.iloc[:,1]
plot_depth_new=df.iloc[:,2]
plot_value_new=df.iloc[:,3]
print(df)

# 创建一个空白图
fig, ax = plt.subplots(figsize=(6, 12))
plt.plot(plot_value_old, plot_depth_old, label='real', color='red')
plt.plot(plot_value_new, plot_depth_new, label='simple kriging', color='blue')
plt.xlabel('Ic')
plt.ylabel('Depth(m)')
plt.title('03 qc and soil type')

# Add a legend
ax.legend()

# 先保存圖片
plt.savefig('03 qc and soil type.png')

# 然後顯示圖片
plt.show()