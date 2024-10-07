import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import pdist, squareform
import scipy
import scipy.linalg as la
import pandas as pd


# import two file to compare
file_1=pd.read_excel('02-soil_depth_statistics_with_ic.xlsx',header=0)
file_2=pd.read_excel('04-soil_depth_statistics_with_ic.xlsx',header=0)

# read the data from the file
Type_1 = file_1['Type']
Type_2 = file_2['Type']
Upper_1 = file_1['Upper Depth']
Upper_2 = file_2['Upper Depth']
Lower_1 = file_1['Lower Depth']
Lower_2 = file_2['Lower Depth']
depth_tolerance = 5
borehole_position_1=1
borehole_position_2=1558.53	
paired_data = []	

# determine the structure of the data
for i 




# 定義地層數據
layers = [
    {"name": "1", "color": "lightgreen", "points": [(0, 0.9), (6, 1)]},
    {"name": "CL1", "color": "lightblue", "points": [(0, 0.8), (6, 0.9)]},
    {"name": "SM2", "color": "yellow", "points": [(0, 0.6), (3, 0.7), (6, 0.8)]},
    {"name": "CL2", "color": "lightgreen", "points": [(0, 0.55), (6, 0.6)]},
    {"name": "SM3", "color": "orange", "points": [(2, 0.2), (4, 0.5)]},
    {"name": "CL3", "color": "tan", "points": [(0, 0), (6, 0.2)]}
]

# 創建圖形
fig, ax = plt.subplots(figsize=(10, 6))

# 繪製每個地層
for layer in layers:
    x, y = zip(*layer["points"])
    ax.fill_between(x, y, y2=0, color=layer["color"], alpha=0.7, label=layer["name"])

# 繪製鑽孔位置
drill_holes = [0,3,6]
for x in drill_holes:
    ax.axvline(x=x, color='yellow', linestyle='-', linewidth=2)
k
# 設置圖形屬性
ax.set_xlim(0, 6)
ax.set_ylim(0, 1)
ax.set_title("Kringing ")
ax.set_xlabel("Distance")
ax.set_ylabel("Depth")
ax.legend(loc='upper right')

plt.show()