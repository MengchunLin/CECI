import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path


# 获取当前脚本目录
script_dir = Path('.')

# 搜索 Excel 文件
file_1_name = '02-soil_depth_statistics_with_ic_and_qc_avg_skipping_200.xlsx'
file_2_name = '04-soil_depth_statistics_with_ic_and_slope_skipping_200.xlsx'

# 组合目录与文件名
file_1_path = script_dir / file_1_name
file_2_path = script_dir / file_2_name

borehole_position_1 = 1
borehole_position_2 = 1558.53

# 检查文件是否存在
if not file_1_path.exists() or not file_2_path.exists():
    raise FileNotFoundError("One or both of the files were not found in the script directory.")

# 读取两个文件
df_1 = pd.read_excel(file_1_path)
df_2 = pd.read_excel(file_2_path)


# 定义深度范围分段
sections_df_1 = [
    {"name": "Section 11", "min_depth": 0, "max_depth": 60},
]

sections_df_2 = [
    {"name": "Section 21", "min_depth": 0, "max_depth": 60},
]

def segment_data(df, sections):
    segmented_data = {}
    for section in sections:
        section_df = df[(df['Upper Depth'] >= section['min_depth']) & (df['Upper Depth'] < section['max_depth'])]
        if section['min_depth'] == 0 and not section_df.empty:
            section_df.loc[section_df.index[0], 'Upper Depth'] = 0
        segmented_data[section['name']] = section_df.reset_index(drop=True)
    return segmented_data

# 分段
segmented_df_1 = segment_data(df_1, sections_df_1)
segmented_df_2 = segment_data(df_2, sections_df_2)

# 比较分段数据框中的相同土壤类型
layers = []  # 用于存储层信息

# 定义颜色映射
color_mapping = {
    '1': 'lightblue',
    '2': 'yellow',
    '3': 'lightgreen',
    '4': 'orange',
    '5': 'tan',
}

# 遍历每个分段
for section1, section2 in zip(segmented_df_1.values(), segmented_df_2.values()):
    length = min(len(section1), len(section2))  # 确保不会超出短表的长度

    for i in range(length):
        # 确保访问的索引在范围内
        if i >= len(section1) or i >= len(section2):
            break  # 退出循环以避免索引超出范围

        # 获取土壤类型和深度信息
        type1 = section1['Type'].iloc[i]
        type2 = section2['Type'].iloc[i]
        upper1 = section1['Upper Depth'].iloc[i]
        upper2 = section2['Upper Depth'].iloc[i]
        lower1 = section1['Lower Depth'].iloc[i]
        lower2 = section2['Lower Depth'].iloc[i]
        count1 = section1['Type'].value_counts()
        count2 = section2['Type'].value_counts()
        # 确定颜色
        color = color_mapping.get(str(type1))

        # 绘制第一个层
        if i == 0:
            layers.append({
                "name": type1,
                "color": color,
                "points": [(borehole_position_1, 0), (borehole_position_2, 0), (borehole_position_2, lower2), (borehole_position_1, lower1)]
            })
            count1[type1] -= 1
            count2[type2] -= 1
        #如果土讓數量相同
        if count1[type1] == count2[type2]:
            #直接找到第一個相同的土壤做連線
            for j in range(i, length):
                if section1['Type'].iloc[i] == section2['Type'].iloc[j]:
                    upper1 = section1['Upper Depth'].iloc[j]
                    upper2 = section2['Upper Depth'].iloc[j]
                    lower1 = section1['Lower Depth'].iloc[j]
                    lower2 = section2['Lower Depth'].iloc[j]
                    layers.append({
                        "name": type1,
                        "color": color,
                        "points": [(borehole_position_1, upper1), (borehole_position_2, upper2), (borehole_position_2, lower2), (borehole_position_1, lower1)]
                    })
                    count1[type1] -= 1
                    count2[type2] -= 1
                    break
            

        # 如果土壤數量不同
        else:
            print("type1",type1)
            # 如果差值為1
            if count1[type1] == 1 and count2[type2] ==0 :
                layers.append({
                    "name": type1,
                    "color": color,
                    "points": [(borehole_position_1, upper1), (borehole_position_2, previous_lower2), (borehole_position_2, previous_lower2), (borehole_position_1, lower1)]
                })
                print("type1",type1)
                break
    # 記錄前一個土壤下限
    previous_lower1 = lower1
    previous_lower2 = lower2


# 绘图
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制每个土壤层为多边形
for layer in layers:
    points = layer["points"]
    polygon = Polygon(points, closed=True, color=layer["color"], alpha=0.7, label=layer["name"])
    ax.add_patch(polygon)

# 绘制钻孔位置
ax.axvline(x=borehole_position_1, color='black', linestyle='--', linewidth=1, label='Borehole 1')
ax.axvline(x=borehole_position_2, color='black', linestyle='--', linewidth=1, label='Borehole 2')

# 反转Y轴
plt.gca().invert_yaxis()

# 设置图形属性
ax.set_xlim(0, 1600)
ax.set_ylim(60, 0)  # 反转 y 轴范围，深度从上到下
ax.set_title("Kriging of Soil Layers")
ax.set_xlabel("Distance")
ax.set_ylabel("Depth")
ax.legend(loc='upper right')

plt.show()

