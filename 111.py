import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pathlib import Path
import numpy as np

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
    '1': 'lightblue',
    '2': 'yellow',
    '3': 'lightgreen',
    '4': 'orange',
    '5': 'tan',
}

# 初始化變量
layers = []
legend_labels = set()
matched_layers_1 = set()
matched_layers_2 = set()
depth_ranges = [(0, 60)]  # 定義深度區間

upper_depth_draw_1 = 0
upper_depth_draw_2 = 0
lower_depth_draw_1 = 0
lower_depth_draw_2 = 0

for depth_start, depth_end in depth_ranges:
    section_df_1 = df_1[(df_1['Upper Depth'] > depth_start) & (df_1['Lower Depth'] <= depth_end)].reset_index(drop=True)
    section_df_2 = df_2[(df_2['Upper Depth'] > depth_start) & (df_2['Lower Depth'] <= depth_end)].reset_index(drop=True)

    soil_type_1 = section_df_1['Type']
    soil_type_2 = section_df_2['Type']
    upper_depth_1 = section_df_1['Upper Depth']
    upper_depth_2 = section_df_2['Upper Depth']
    lower_depth_1 = section_df_1['Lower Depth']
    lower_depth_2 = section_df_2['Lower Depth']

    count_1 = soil_type_1.value_counts()
    count_2 = soil_type_2.value_counts()

    Ic_1 = df_1['Average Ic']
    Ic_2 = df_2['Average Ic']

    idx_1 = 0
    idx_2 = 0
    
    while idx_1 < len(soil_type_1) and idx_2 < len(soil_type_2):
        type_1 = soil_type_1.iloc[idx_1]
        type_2 = soil_type_2.iloc[idx_2]

        if idx_1 in matched_layers_1:
            idx_1 += 1
            continue
        if idx_2 in matched_layers_2:
            idx_2 += 1
            continue

        lower_depth_draw_1 = lower_depth_1.iloc[idx_1]
        lower_depth_draw_2 = lower_depth_2.iloc[idx_2]

        # 如果順序相同，直接匹配
        if type_1 == type_2:
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
            idx_1 += 1
            idx_2 += 1
        # 如果數量相同，找到不在matched_layers中的第一個相同的type
        elif count_1[type_1] == count_2[type_2]:
            matched_layers_1.add(idx_1)
            matched_layers_2.add(idx_2)
            layers.append({
                "points": [(borehole_position_1, upper_depth_draw_1),
                           (borehole_position_2, upper_depth_draw_2),
                           (borehole_position_2, lower_depth_draw_2),
                           (borehole_position_1, lower_depth_draw_1)],
                "color": color_mapping[str(type_1)],
                "label": type_1 if type_1 not in legend_labels else None
            })
            legend_labels.add(type_1)
            upper_depth_draw_1 = lower_depth_draw_1
            upper_depth_draw_2 = lower_depth_draw_2
            count_1[type_1] -= 1
            count_2[type_2] -= 1
            idx_1 += 1
            idx_2 += 1
        # 如果數量不同
        elif count_1[type_1] > count_2[type_2]:
            #向下找3個type_2，如果3個type_2以內有1個以上的type_1
            found = False
            x=0
            check_layer=[]
            for i in range(1, 4):
                if idx_2 + i < len(soil_type_2):
                    if soil_type_2.iloc[idx_2 + i] == type_1:
                        x+=1
                else:
                    check_layer.append(idx_2 + i)
            if x>1:
                found = True
            # 如果找到，則將檢查check_layer的深度上下限是否在idx_1的深度上下限內
            if found:
                for i in check_layer:
                    if lower_depth_2.iloc[i] <= lower_depth_1.iloc[idx_1] and upper_depth_2.iloc[i] >= upper_depth_1.iloc[idx_1]:
                        # 把idx_1的土層下限深度/2，並且新增一個土層
                        half_depth = (lower_depth_1.iloc[idx_1] + upper_depth_1.iloc[idx_1]) / 2
                        bottom_depth = lower_depth_1.iloc[idx_1]    
                        copy_layer = pd.DataFrame([[np.nan]*section_df_1.shape[1]], columns=section_df_1.columns)
                        ection_df_1 = pd.concat([section_df_1.iloc[:idx_1], copy_layer, section_df_1.iloc[idx_1:]]).reset_index(drop=True)
                        copy_layer['Upper Depth'] = half_depth
                        copy_layer['Lower Depth'] = bottom_depth
                        copy_layer['Type'] = type_1
                        copy_layer['Average Ic'] = Ic_1.iloc[idx_1]





        else:
            # 增加厚度為0的土層
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
            idx_1 += 1

    # 處理剩餘的層
    while idx_1 < len(soil_type_1):
        type_1 = soil_type_1.iloc[idx_1]
        lower_depth_draw_1 = lower_depth_1.iloc[idx_1]
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
        idx_1 += 1

    while idx_2 < len(soil_type_2):
        type_2 = soil_type_2.iloc[idx_2]
        lower_depth_draw_2 = lower_depth_2.iloc[idx_2]
        layers.append({
            "points": [(borehole_position_1, upper_depth_draw_1),
                       (borehole_position_2, upper_depth_draw_2),
                       (borehole_position_2, lower_depth_draw_2),
                       (borehole_position_1, upper_depth_draw_1)],
            "color": color_mapping[str(type_2)],
            "label": type_2 if type_2 not in legend_labels else None
        })
        matched_layers_2.add(idx_2)
        legend_labels.add(type_2)
        upper_depth_draw_2 = lower_depth_draw_2
        idx_2 += 1

# 繪圖部分保持不變
fig, ax = plt.subplots(figsize=(10, 6))

legend_handles = []

for layer in layers:
    points = layer["points"]
    polygon = Polygon(points, closed=True, color=layer["color"], alpha=0.7)
    ax.add_patch(polygon)

    if layer["label"] is not None:
        handle, = ax.plot([], [], color=layer["color"], label=layer["label"])
        legend_handles.append(handle)

ax.axvline(x=borehole_position_1, color='black', linestyle='--', linewidth=1, label='Borehole 1')
ax.axvline(x=borehole_position_2, color='black', linestyle='--', linewidth=1, label='Borehole 2')

ax.legend(handles=legend_handles, loc='upper right', bbox_to_anchor=(1.3, 1))

plt.gca().invert_yaxis()

ax.set_xlim(0, 1600)
ax.set_ylim(70, 0)
ax.set_title("Soil Type Visualization between Boreholes by Depth Sections")
ax.set_xlabel("Distance")
ax.set_ylabel("Depth")

plt.tight_layout()
plt.show()