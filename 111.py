import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
import numpy as np

# 设置文件路径
script_dir = Path('.')
file_1_path = script_dir / '02_for_predict_data.xlsx'
file_2_path = script_dir / '04_for_predict_data.xlsx'

borehole_position_1 = 1
borehole_position_2 = 1558.53

# 读取文件
df_1 = pd.read_excel(file_1_path)
df_2 = pd.read_excel(file_2_path)

# 定义颜色映射
color_mapping = {
    '1': 'lightblue',
    '2': 'yellow',
    '3': 'lightgreen',
    '4': 'orange',
    '5': 'tan',
}

# 初始化变量
layers = []
legend_labels = set()
matched_layers_1 = set()
matched_layers_2 = set()
depth_ranges = [(0, 60)]  # 定义深度区间

upper_depth_draw_1 = 0
upper_depth_draw_2 = 0
lower_depth_draw_1 = 0
lower_depth_draw_2 = 0

for depth_start, depth_end in depth_ranges:
    section_df_1 = df_1[(df_1['Upper Depth'] > depth_start) & (df_1['Lower Depth'] <= depth_end)]
    section_df_2 = df_2[(df_2['Upper Depth'] > depth_start) & (df_2['Lower Depth'] <= depth_end)]

    soil_type_1 = section_df_1['Type']
    soil_type_2 = section_df_2['Type']

    lower_depth_1 = section_df_1['Lower Depth']
    lower_depth_2 = section_df_2['Lower Depth']

    count_1 = soil_type_1.value_counts()
    count_2 = soil_type_2.value_counts()

    for idx_1, type_1 in enumerate(soil_type_1):
        if idx_1 in matched_layers_1:
            continue
        lower_depth_draw_1 = lower_depth_1.iloc[idx_1]

        for idx_2 in range(len(soil_type_2)):
            if idx_2 in matched_layers_2:
                continue

            type_2 = soil_type_2.iloc[idx_2]

            # 如果順序相同，直接匹配
            if type_1 == type_2 and idx_1 == idx_2:
                lower_depth_draw_2 = lower_depth_2.iloc[idx_2]
                layers.append({
                    "points": [(borehole_position_1, upper_depth_draw_1),
                               (borehole_position_2, upper_depth_draw_2),
                               (borehole_position_2, lower_depth_draw_2),
                               (borehole_position_1, lower_depth_draw_1)],
                    "color": color_mapping[str(type_1)],
                    "label": type_1 if type_1 not in legend_labels else None
                })
                matched_layers_1.add(idx_1)
                matched_layers_2.add(idx_2)
                legend_labels.add(type_1)
                upper_depth_draw_1 = lower_depth_draw_1
                upper_depth_draw_2 = lower_depth_draw_2
                count_1[type_1] -= 1
                count_2[type_2] -= 1
                break

            # 數量相同，直接匹配
            if count_1[type_1] == count_2[type_2]:
                lower_depth_draw_1 = lower_depth_1.iloc[idx_1]
                lower_depth_draw_2 = lower_depth_2.iloc[idx_2]
                layers.append({
                    "points": [(borehole_position_1, upper_depth_draw_1),
                               (borehole_position_2, upper_depth_draw_2),
                               (borehole_position_2, lower_depth_draw_2),
                               (borehole_position_1, lower_depth_draw_1)],
                    "color": color_mapping[str(type_1)],
                    "label": type_1 if type_1 not in legend_labels else None
                })
                matched_layers_1.add(idx_1)
                matched_layers_2.add(idx_2)
                legend_labels.add(type_1)
                upper_depth_draw_1 = lower_depth_draw_1
                upper_depth_draw_2 = lower_depth_draw_2
                count_1[type_1] -= 1
                count_2[type_2] -= 1
                break

            # 數量不同，找最接近的Ic值(向下找3組)
            else:
                if count_1[type_1] != 0 and count_2[type_2] != 0:
                    # 往下3行找最接近的Ic值
                    x=0
                    difference = []
                    for i in range(3):
                        #如果往下3層有1個以上的相同土層，則分為兩層
                        if type_1 == soil_type_2.iloc[idx_2 + i]:
                            x+=1
                        else:
                            difference.append(idx_2 + i)
                    if x>1 :
                        #檢核difference的upper depth及lower depth是否在兩層土層的範圍內
                        for i in range(len(difference)):
                            if section_df_2.loc[difference[i], 'Upper Depth'] >= section_df_1.loc[idx_1-1, 'Upper Depth'] and section_df_2.loc[difference[i], 'Lower Depth'] <= section_df_1.loc[idx_1-1, 'Lower Depth']:
                                break
                        # 把此層土分為兩層
                        Ic_2 = section_df_2['Average Ic']
                        half_depth=(section_df_1.loc[idx_1-1,'Upper Depth']+section_df_1.loc[idx_1-1, 'Lower Depth']) / 2
                        bottom_depth=section_df_1.loc[idx_1-1, 'Lower Depth']
                        #新增一層空白土層在idx_1+1
                        # 創建一個空白行，所有欄位為 NaN
                        blank_row = pd.DataFrame([[np.nan] * section_df_1.shape[1]], columns=section_df_1.columns)
                        # 使用 pd.concat 在指定位置插入空白行
                        section_df_1 = pd.concat([section_df_1.iloc[:idx_1], blank_row, section_df_1.iloc[idx_1:]]).reset_index(drop=True)
                        section_df_1.loc[idx_1 , 'Type' ] = section_df_1.loc[idx_1-1,'Type']  # 複製上一行的值 v
                        section_df_1.loc[idx_1 , 'Lower Depth'] = bottom_depth  # 同樣深度
                        section_df_1.loc[idx_1 , 'Average Ic'] = section_df_1.loc[idx_1-1, 'Average Ic']  # 複製 Ic 值
                        section_df_1.loc[idx_1 , 'Upper Depth'] = half_depth  # 新增的土層的上界
                        section_df_1.loc[idx_1-1, 'Lower Depth'] = half_depth  # 更新原土層的下界
                        # 上層土層連接第一個找到的相同土層
                        layers.append({
                            "points": [(borehole_position_1, section_df_1.loc[idx_1-1, 'Upper Depth']),
                                        (borehole_position_2, section_df_1.loc[idx_1 , 'Upper Depth']),
                                        (borehole_position_2, section_df_1.loc[idx_1 , 'Lower Depth']),
                                        (borehole_position_1, section_df_1.loc[idx_1-1, 'Lower Depth'])],
                            "color": color_mapping[str(type_1)],
                            "label": type_1 if type_1 not in legend_labels else None
                        })
                        
                        matched_layers_1.add(idx_1-1)
                        legend_labels.add(type_1)
                        upper_depth_draw_1 = half_depth

                                


                    else:
                        Ic_2 = section_df_2['Average Ic']
                        target_Ic = section_df_1['Average Ic'].iloc[idx_1]
                        closest_value = Ic_2[np.abs(Ic_2 - target_Ic).argmin()]
                        idx_2 = Ic_2[Ic_2 == closest_value].index[0]
                        lower_depth_draw_2 = lower_depth_2.iloc[idx_2]
                        layers.append({
                            "points": [(borehole_position_1, upper_depth_draw_1),
                                        (borehole_position_2, upper_depth_draw_2),
                                        (borehole_position_2, lower_depth_draw_2),
                                        (borehole_position_1, lower_depth_draw_1)],
                            "color": color_mapping[str(type_1)],
                            "label": type_1 if type_1 not in legend_labels else None
                        })
                        matched_layers_1.add(idx_1)
                        matched_layers_2.add(idx_2)
                        legend_labels.add(type_1)
                        upper_depth_draw_1 = lower_depth_draw_1
                        upper_depth_draw_2 = lower_depth_draw_2
                        count_1[type_1] -= 1
                        count_2[type_2] -= 1
                        break

                        # 如果找不到最接近的Ic值，增加厚度为0的土层
                    else:
                        layers.append({
                            "points": [(borehole_position_1, upper_depth_draw_1),
                                        (borehole_position_2, upper_depth_draw_2),
                                        (borehole_position_2, upper_depth_draw_2),
                                        (borehole_position_1, lower_depth_draw_1)],
                            "color": color_mapping[str(type_1)],
                            "label": type_1 if type_1 not in legend_labels else None
                        })
                        matched_layers_1.add(idx_1)
                        legend_labels.add(type_1)
                        upper_depth_draw_1 = lower_depth_draw_1
                        upper_depth_draw_2 = lower_depth_draw_2
                        break

                # 如果某一方土层數量為0
                elif count_1[type_1] != 0 and count_1[type_2] == 0:
                    layers.append({
                        "points": [(borehole_position_1, upper_depth_draw_1),
                                    (borehole_position_2, upper_depth_draw_2),
                                    (borehole_position_2, upper_depth_draw_2),
                                    (borehole_position_1, lower_depth_draw_1)],
                        "color": color_mapping[str(type_1)],
                        "label": type_1 if type_1 not in legend_labels else None
                    })
                    matched_layers_1.add(idx_1)
                    legend_labels.add(type_1)
                    upper_depth_draw_1 = lower_depth_draw_1
                    upper_depth_draw_2 = lower_depth_draw_2
                    break
                elif count_1[type_1] == 0 and count_1[type_2] != 0:
                    break

# 初始化图形
fig, ax = plt.subplots(figsize=(10, 6))

# 用于存储图例条目的列表
legend_handles = []

# 绘制每个土壤层为多边形
for layer in layers:
    points = layer["points"]
    polygon = Polygon(points, closed=True, color=layer["color"], alpha=0.7)
    ax.add_patch(polygon)

    # 仅当需要添加图例时才绘制空的线以生成图例条目
    if layer["label"] is not None:
        handle, = ax.plot([], [], color=layer["color"], label=layer["label"])
        legend_handles.append(handle)

# 绘制钻孔位置
ax.axvline(x=borehole_position_1, color='black', linestyle='--', linewidth=1, label='Borehole 1')
ax.axvline(x=borehole_position_2, color='black', linestyle='--', linewidth=1, label='Borehole 2')

# 设置图例框在图的右上角，绘图区的外侧
ax.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(-0.05, 1))

# 反转Y轴
plt.gca().invert_yaxis()

# 设置图形属性
ax.set_xlim(0, 1600)
ax.set_ylim(70, 0)  # 反转 y 轴范围，深度从上到下
ax.set_title("Soil Type Visualization between Boreholes by Depth Sections")
ax.set_xlabel("Distance")
ax.set_ylabel("Depth")

plt.show()
