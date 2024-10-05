import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 读取两个文件
file_1_path = 'C:/Users/yo/Desktop/CECI/02-soil_depth_statistics_with_ic_and_qc_avg_skipping_200.xlsx'
file_2_path = 'C:/Users/yo/Desktop/CECI/04-soil_depth_statistics_with_ic_and_slope_skipping_200.xlsx'

df_1 = pd.read_excel(file_1_path)
df_2 = pd.read_excel(file_2_path)
section1 = [0,40]
section2 = [40, 60]
section3 = [60, 80]
section4 = [80, 100]
length = max(len(df_1), len(df_2))
print(length)

# 把兩個數據分段
