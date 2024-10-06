import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 读取两个文件
file_1_path = 'C:/Users/Janet/Desktop/CECI/02soil_depth_statistics_with_ic_and_qc_avg_skipping_invalid.xlsx'
file_2_path = 'C:/Users/Janet/Desktop/CECI/04soil_depth_statistics_with_ic_and_qc_avg_skipping_invalid.xlsx'

df_1 = pd.read_excel(file_1_path)
df_2 = pd.read_excel(file_2_path)
section1 = [0,40]
section2 = [40, 60]
section3 = [60, 80]
section4 = [80, 100]
length = max(len(df_1), len(df_2))
print(length)

data_to_process = 
# 把兩個數據分段
for i in range(0, length, 20):
    # 把Depth (m)列的值分段
    if df_1['Upper Depth'].iloc[i] >= section1[0] and df_1['Upper Depth'].iloc[i] < section1[1]:
        df_1['Section'] = 'Section1'
