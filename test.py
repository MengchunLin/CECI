import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
import numpy as np
import matplotlib.ticker as ticker

# 設置文件路徑
script_dir = Path('.')
file_1_path = script_dir / '02_for_predict_data.xlsx'
file_2_path = script_dir / '04_for_predict_data.xlsx'

borehole_position_1 = 1
borehole_position_2 = 1558.53

# 讀取文件
df_1 = pd.read_excel(file_1_path)
df_2 = pd.read_excel(file_2_path)

# 定義顏色映射
color_mapping = {
    '1': 'lightsalmon',
    '2': 'lightblue',
    '3': 'thistle',
    '4': 'lemonchiffon',
    '5': 'sandybrown',
}

# 初始化變量
layers = []
legend_labels = set()

depth_ranges = [(0, 60),(60,80),(80,110)]  # 定義深度區間

last_major_lower_depth = 0
last_minor_lower_depth = 0

previous_section_1 = None
previous_section_2 = None
# 對比兩個文件的深度區間尋找相近Ic
for depth_range in depth_ranges:
    
    start_depth, end_depth = depth_range
    print('range[',start_depth,end_depth,']')
    matched_layers_major = set()
    matched_layers_minor = set()
    all_types = set()
    section_df_1 = df_1[(df_1['Upper Depth']>start_depth) & (df_1['Upper Depth'] < end_depth) ].reset_index(drop=True)
    section_df_2 = df_2[(df_2['Upper Depth']>start_depth) & (df_2['Upper Depth'] < end_depth) ].reset_index(drop=True)

    # 確認範圍外下一筆資料是否存在並有相同土壤類型
    next_row_1 = df_1[df_1['Upper Depth'] >= end_depth].iloc[:1]
    next_row_2 = df_2[df_2['Upper Depth'] >= end_depth].iloc[:1]
    last_row_1 = section_df_1.iloc[-1]
    last_row_2 = section_df_2.iloc[-1]

    # 確保我們至少有一筆範圍外的資料可供比較
    if not next_row_1.empty and not next_row_2.empty:
    # 取得範圍外的第一筆資料
        next_soil_type_1 = next_row_1.iloc[0]['Type']
        next_soil_type_2 = next_row_2.iloc[0]['Type']

        # 比較範圍外的土壤類型是否相同
        if next_soil_type_1 == last_row_2['Type']:
            # 如果相同，則將範圍外的資料整行加入範圍內
            section_df_1 = section_df_1._append(next_row_1.iloc[0]).reset_index(drop=True)
            print(next_soil_type_1,last_row_2['Type'])
        elif next_soil_type_2 == last_row_1['Type']:
            section_df_2 = section_df_2._append(next_row_2.iloc[0]).reset_index(drop=True)
            print(next_soil_type_2,last_row_1['Type'])

# 刪除與上一區間重複的資料
    if previous_section_1 is not None:
        # 使用merge找出重複的行
        duplicates_1 = pd.merge(section_df_1, previous_section_1, how='inner')
        if not duplicates_1.empty:
            # 刪除重複的行
            section_df_1 = section_df_1[~section_df_1.apply(tuple, 1).isin(duplicates_1.apply(tuple, 1))]
            
    if previous_section_2 is not None:
        # 使用merge找出重複的行
        duplicates_2 = pd.merge(section_df_2, previous_section_2, how='inner')
        if not duplicates_2.empty:
            # 刪除重複的行
            section_df_2 = section_df_2[~section_df_2.apply(tuple, 1).isin(duplicates_2.apply(tuple, 1))]
    
    # 重置索引
    section_df_1 = section_df_1.reset_index(drop=True)
    section_df_2 = section_df_2.reset_index(drop=True)
    
    # 保存當前區間的數據作為下一次迭代的previous
    previous_section_1 = section_df_1.copy()
    previous_section_2 = section_df_2.copy()
    
    idx_1 = 0
    idx_2 = 0

    len_1 = len(section_df_1)
    len_2 = len(section_df_2)
    # 選出較短的文件
    major_section = section_df_1 if len_1 < len_2 else section_df_2
    minor_section = section_df_2 if len_1 < len_2 else section_df_1
    major_position = borehole_position_1 if len_1 < len_2 else borehole_position_2
    minor_position = borehole_position_2 if len_1 < len_2 else borehole_position_1

    soil_type_major= major_section['Type']
    soil_type_minor = minor_section['Type']
    # 如果數據需要清理，可以這樣處理：
    upper_depth_major = major_section['Upper Depth'].astype(float)
    upper_depth_minor = minor_section['Upper Depth'].astype(float)
    lower_depth_major = major_section['Lower Depth'].astype(float)
    lower_depth_minor = minor_section['Lower Depth'].astype(float)
    Ic_major = major_section['Average Ic']
    Ic_minor = minor_section['Average Ic']
    count_major = soil_type_major.value_counts()
    count_minor = soil_type_minor.value_counts()
    # 統計count_1和count_2中所有的soil type
    all_types.update(count_major.index)
    all_types.update(count_minor.index)

    match_layer = 0


    for idx in range(len(major_section)):
        

        include = []
        interpolation = 100
        flag = False
        for i in range(0, 3):
            if idx + i < len(minor_section) and soil_type_major[idx] == soil_type_minor[idx + i] and idx + i not in matched_layers_minor:
                x = abs(Ic_major[idx] - Ic_minor[idx + i])
                if x < interpolation:
                    interpolation = x
                    match_layer = idx + i
                    flag = True


        # 刪除include裡<match_layer的數字
        for i in range(idx, match_layer):
            if i not in matched_layers_minor:
                include.append(i)

        # 匹配match_layer
        if flag:
            layers.append({
                "upper_depth_major": (major_position, upper_depth_major[idx]),
                "lower_depth_major": (major_position, lower_depth_major[idx]),
                "upper_depth_minor": (minor_position, upper_depth_minor[match_layer]),
                "lower_depth_minor": (minor_position, lower_depth_minor[match_layer]),
                "points": [
                    (major_position, upper_depth_major[idx]),
                    (major_position, lower_depth_major[idx]),
                    (minor_position, lower_depth_minor[match_layer]),
                    (minor_position, upper_depth_minor[match_layer]),
                ],
                "label": soil_type_major[idx],
                "color": color_mapping[str(int(soil_type_major[idx]))],
                "soil_type": soil_type_major[idx],
            })
            matched_layers_major.add(idx)
            matched_layers_minor.add(match_layer)
            print('match',idx,match_layer)

        
        elif not flag:
            if idx != 0:
                layers.append({
                    "upper_depth_major": (major_position, upper_depth_major[idx]),
                    "lower_depth_major": (major_position, lower_depth_major[idx]),
                    "upper_depth_minor": (minor_position, lower_depth_minor[match_layer]),
                    "lower_depth_minor": (minor_position, lower_depth_minor[match_layer]),
                    "points": [
                        (major_position, upper_depth_major[idx]),
                        (major_position, lower_depth_major[idx]),
                        (minor_position, lower_depth_minor[match_layer]),
                        (minor_position, lower_depth_minor[match_layer]),
                    ],
                    "label": soil_type_major[idx],
                    "color": color_mapping[str(int(soil_type_major[idx]))],
                    "soil_type": soil_type_major[idx],
                })
                matched_layers_major.add(idx)
                
                print('match',idx,match_layer)
            else:
                # 當主鑽孔第一筆資料的upper_depth_1小於副鑽孔第一筆資料的upper_depth_2
                if upper_depth_minor[idx] < upper_depth_major[0]:
                    layers.append({
                        "upper_depth_major": (major_position, upper_depth_major[0]),
                        "lower_depth_major": (major_position, lower_depth_major[0]),
                        "upper_depth_minor": (minor_position, upper_depth_minor[idx]),
                        "lower_depth_minor": (minor_position, lower_depth_minor[idx]),
                        "points": [
                            (major_position, lower_depth_major[0]),
                            (major_position, lower_depth_major[0]),
                            (minor_position, lower_depth_minor[idx]),
                            (minor_position, upper_depth_minor[idx]),
                        ],
                        "label": soil_type_minor[idx],
                        "color": color_mapping[str(int(soil_type_minor[idx]))],
                        "soil_type": soil_type_minor[idx],
                    })
                    matched_layers_minor.add(idx)
                    layers.append({
                        "upper_depth_major": (major_position, upper_depth_major[idx]),
                        "lower_depth_major": (major_position, lower_depth_major[idx]),
                        "upper_depth_minor": (minor_position, lower_depth_minor[0]),
                        "lower_depth_minor": (minor_position, lower_depth_minor[0]),
                        "points": [
                            (major_position, upper_depth_major[idx]),
                            (major_position, lower_depth_major[idx]),
                            (minor_position, lower_depth_minor[0]),
                            (minor_position, lower_depth_minor[0]),
                        ],
                        "label": soil_type_minor[0],
                        "color": color_mapping[str(int(soil_type_major[0]))],
                        "soil_type": soil_type_minor[0],
                    })
                    matched_layers_major.add(idx)

                    
                # 當副鑽孔的深度大於主鑽孔的深度
                elif upper_depth_minor[idx] > upper_depth_major[0]:
                    layers.append({
                        "upper_depth_major": (major_position, upper_depth_major[0]),
                        "lower_depth_major": (major_position, lower_depth_major[0]),
                        "upper_depth_minor": (minor_position, upper_depth_minor[idx]),
                        "lower_depth_minor": (minor_position, upper_depth_minor[idx]),
                        "points": [
                            (major_position, upper_depth_major[0]),
                            (major_position, lower_depth_major[0]),
                            (minor_position, upper_depth_minor[idx]),
                            (minor_position, upper_depth_minor[idx]),
                        ],
                        "label": soil_type_major[0],
                        "color": color_mapping[str(int(soil_type_major[0]))],
                        "soil_type": soil_type_major[0],
                    })
                    matched_layers_major.add(0)
                    layers.append({
                        "upper_depth_major": (major_position, lower_depth_major[idx]),
                        "lower_depth_major": (major_position, lower_depth_major[idx]),
                        "upper_depth_minor": (minor_position, lower_depth_minor[0]),
                        "lower_depth_minor": (minor_position, upper_depth_minor[0]),
                        "points": [
                            (major_position, lower_depth_major[idx]),
                            (major_position, lower_depth_major[idx]),
                            (minor_position, upper_depth_minor[0]),
                            (minor_position, lower_depth_minor[0]),
                        ],
                        "label": soil_type_major[idx],
                        "color": color_mapping[str(int(soil_type_minor[idx]))],
                        "soil_type": soil_type_major[idx],
                    })
                    matched_layers_minor.add(idx)

        for i in include:
            print('i',i)
            layers.append({
                "upper_depth_major": (major_position, upper_depth_major[idx]),
                "lower_depth_major": (major_position, upper_depth_major[idx]),
                "upper_depth_minor": (minor_position, upper_depth_minor[i]),
                "lower_depth_minor": (minor_position, lower_depth_minor[i]),
                "points": [
                    (major_position, upper_depth_major[idx]),
                    (major_position, upper_depth_major[idx]),
                    (minor_position, upper_depth_minor[i]),
                    (minor_position, lower_depth_minor[i]),
                ],
                "label": soil_type_minor[i],
                "color": color_mapping[str(int(soil_type_minor[i]))],
                "soil_type": soil_type_minor[i],
            })
            matched_layers_minor.add(i)
    # 匹配剩下的
    for i in range(len(minor_section)):
        if i not in matched_layers_minor:
            layers.append({
                "upper_depth_major": (major_position, lower_depth_major[idx]),
                "lower_depth_major": (major_position, lower_depth_major[idx]),
                "upper_depth_minor": (minor_position, upper_depth_minor[i]),
                "lower_depth_minor": (minor_position, lower_depth_minor[i]),
                "points": [
                    (major_position, lower_depth_major[idx]),
                    (major_position, lower_depth_major[idx]),
                    (minor_position, lower_depth_minor[i]),
                    (minor_position, upper_depth_minor[i]),
                ],
                "label": soil_type_minor[i],
                "color": color_mapping[str(int(soil_type_minor[i]))],
                "soil_type": soil_type_minor[i],
            })
            matched_layers_minor.add(idx)
    # 紀錄layers最後一筆資料的lower_depth_1和lower_depth_2
    last_major_lower_depth = lower_depth_major[idx]
    last_minor_lower_depth = lower_depth_minor[i]

weight_1 = 0.5
weight_2 = 0.5

# 把 layers 的資料轉換成 DataFrame
df_layers = pd.DataFrame(layers)
print(df_layers)

# 清理資料、四捨五入到小數點後兩位並轉換為浮點數

# 建立 predict_borehole DataFrame 並新增欄位
# 建立 predict_borehole DataFrame 並新增欄位
predict_borehole = pd.DataFrame()
predict_borehole['Type'] = df_layers['soil_type']

# 分別取出深度值進行計算，並四捨五入到小數點後兩位
predict_borehole['Upper Depth'] = (
    df_layers['upper_depth_major'].apply(lambda x: x[1]) * weight_1 + 
    df_layers['upper_depth_minor'].apply(lambda x: x[1]) * weight_2
).round(2)

predict_borehole['Lower Depth'] = (
    df_layers['lower_depth_major'].apply(lambda x: x[1]) * weight_1 + 
    df_layers['lower_depth_minor'].apply(lambda x: x[1]) * weight_2
).round(2)





print(predict_borehole)


# 繪圖
fig, ax = plt.subplots(figsize=(12, 8))

# 建立不重複的圖例
used_labels = set()
legend_handles = []

for layer in layers:
    upper_depth_major = layer["upper_depth_major"]
    lower_depth_major = layer["lower_depth_major"]
    upper_depth_minor = layer["upper_depth_minor"]
    lower_depth_minor = layer["lower_depth_minor"]
    points = [upper_depth_major, lower_depth_major, lower_depth_minor, upper_depth_minor] # 更新 points 為四點的列表
    label = layer["label"]
    color = layer["color"]

    # 定義多邊形，使用四個點構成的列表
    polygon = Polygon(points, closed=True, color=color, alpha=0.7)
    ax.add_patch(polygon)
    
    if label not in used_labels:
        legend_handles.append(plt.Rectangle((0, 0), 1, 1, fc=color, alpha=0.7, label=label))
        used_labels.add(label)

# 添加鑽孔位置線
ax.axvline(x=borehole_position_1, color='black', linestyle='--', linewidth=1, label='Borehole 1')
ax.axvline(x=borehole_position_2, color='black', linestyle='--', linewidth=1, label='Borehole 2')
ax.axvline(x=780, color='black', linestyle='--', linewidth=1, label='Borehole 2')
ax.axvline(x=785, color='black', linestyle='--', linewidth=1, label='Borehole 2')

# 設置圖例
ax.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(1.15, 1))

# 設置軸和標題
ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
plt.gca().invert_yaxis()
ax.set_xlim(0, borehole_position_2)
ax.set_ylim(105, 0)
ax.set_title("Soil Type Visualization between Boreholes")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Depth (m)")

plt.tight_layout()
plt.show()