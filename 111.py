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
depth_ranges = [(0, 60),(60,80),(80,110)]  # 定義深度區間

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
        if idx_1==idx_2 and type_1 == type_2:
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
            print('順序相同，直接匹配',idx_1,idx_2)
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
            print('數量相同，找到不在matched_layers中的第一個相同的type',idx_1,idx_2)
        # 如果向下找3個type_2，如果3個type_2以內有1個以上的type_1
        # 向下檢查最多 3 個 type_2
        else:
            match_count = 0  # 計算匹配次數
            include_type_2 = []  # 記錄匹配的 type_2 的索引
            mezzanine=[]
            # 檢查 type_1 和接下來 3 層的 type_2 是否有匹配
            #skip_flag = False  # 設置跳過標誌

            for i in range(0, 4):
                if idx_2 + i < len(soil_type_2):  # 確保不超出範圍
                    if soil_type_2.iloc[idx_2 + i] == type_1:  # 如果找到與 type_1 匹配的 type_2
                        match_count += 1
                        include_type_2.append(idx_2 + i)  # 記錄匹配的 type_2 的索引
                    else:
                        mezzanine.append(soil_type_2.iloc[idx_2 + i])

            if match_count > 1:  # 如果有多於一個匹配
                # skip_flag = True  # 設置跳過標誌
                for i in include_type_2:
                    # 檢查匹配的 type_2 層是否在當前 type_1 的上下限深度之內
                    if lower_depth_2.iloc[i] <= lower_depth_1.iloc[idx_1] and upper_depth_2.iloc[i] >= upper_depth_1.iloc[idx_1]:
                        # 分割 type_1 的土層：將其一分為二，並創建一個新的土層
                        half_depth = (lower_depth_1.iloc[idx_1] - upper_depth_1.iloc[idx_1]) / 2 + upper_depth_1.iloc[idx_1]
                        bottom_depth = lower_depth_1.iloc[idx_1]

                        # 插入新的一層
                        copy_layer = pd.DataFrame([[np.nan] * section_df_1.shape[1]], columns=section_df_1.columns)
                        section_df_1 = pd.concat([section_df_1.iloc[:idx_1], copy_layer, section_df_1.iloc[idx_1:]]).reset_index(drop=True)
                        section_df_1.at[idx_1, 'Upper Depth'] = upper_depth_1.iloc[idx_1]
                        section_df_1.at[idx_1, 'Lower Depth'] = half_depth
                        section_df_1.at[idx_1 + 1, 'Upper Depth'] = half_depth
                        section_df_1.at[idx_1 + 1, 'Lower Depth'] = bottom_depth
                        section_df_1.at[idx_1, 'Type'] = type_1
                        section_df_1.at[idx_1 + 1, 'Type'] = type_1
                        section_df_1.at[idx_1, 'Average Ic'] = Ic_1.iloc[idx_1]
                        section_df_1.at[idx_1 + 1, 'Average Ic'] = Ic_1.iloc[idx_1]
                        layers.append({
                            "points": [(borehole_position_1, upper_depth_draw_1),
                                    (borehole_position_2, upper_depth_draw_2),
                                    (borehole_position_2, lower_depth_draw_2),
                                    (borehole_position_1, half_depth)],
                            "color": color_mapping[str(type_1)],
                            "label": type_1 if type_1 not in legend_labels else None
                        })
                        print('向下找3個type_2，如果3個type_2以內有1個以上的type_1',idx_1,idx_2)
                        # 重新取得更新後的 'Upper Depth' 列
                        upper_depth_1 = section_df_1['Upper Depth']
                        # 更新深度並繼續配對
                        upper_depth_draw_1 = lower_depth_draw_1
                        upper_depth_draw_2 = lower_depth_draw_2
                        idx_1 += 1

                        # 配對第二部分 `type_1` 與第二個與type_1相同的 `type_2`
                        upper_depth_draw_1 = upper_depth_1.at[idx_1]
                        upper_depth_draw_2 = upper_depth_2.at[i]  # 這裡有問題
                        lower_depth_draw_1 = lower_depth_1.iloc[idx_1 - 1] # 這裡有問題
                        lower_depth_draw_2 = lower_depth_2.iloc[i]
                        print(upper_depth_draw_1, upper_depth_draw_2, lower_depth_draw_1, lower_depth_draw_2)
                        print('向下找3個type_2，如果3個type_2以內有1個以上的type_1',idx_1,idx_2)
                        # 添加匹配的 layer 到 layers
                        layers.append({
                            "points": [(borehole_position_1, upper_depth_draw_1),
                                    (borehole_position_2, upper_depth_draw_2),
                                    (borehole_position_2, lower_depth_draw_2),
                                    (borehole_position_1, lower_depth_draw_1)],
                            "color": color_mapping[str(type_1)],
                            "label": type_1 if type_1 not in legend_labels else None
                        })
                        
                        # 記錄已匹配的層索引
                        matched_layers_1.add(idx_1)
                        matched_layers_2.add(i)
                        legend_labels.add(type_1)

                        # 更新深度，準備下一層的匹配
                        upper_depth_draw_1 = lower_depth_draw_1
                        upper_depth_draw_2 = lower_depth_draw_2
                        idx_1 += 1
                        # 更新 idx_2，跳過處理過的 `type_2`，避免重複處理
                        idx_2 = i + 1  # 跳過已匹配過的 `type_2` 層
                        
                        # 處理夾層
                        for m in mezzanine:
                            lower_depth_draw_1 = lower_depth_1.iloc[idx_1]
                            lower_depth_draw_2 = lower_depth_2.iloc[idx_2]
                            layers.append({
                                "points": [(borehole_position_1, upper_depth_draw_1),
                                        (borehole_position_2, upper_depth_draw_2),
                                        (borehole_position_2, lower_depth_draw_2),
                                        (borehole_position_1, lower_depth_draw_1)],
                                "color": color_mapping[str(m)],
                                "label": m if m not in legend_labels else None
                            })
                            upper_depth_draw_1 = lower_depth_draw_1
                            upper_depth_draw_2 = lower_depth_draw_2
                            idx_1 += 1
                            idx_2 += 1
                            legend_labels.add(m)

            elif match_count == 1:  # 如果只有一個匹配
                # 找到匹配的 type_2
                matched_idx = include_type_2[0]
                lower_depth_draw_1 = lower_depth_1.iloc[idx_1]
                lower_depth_draw_2 = lower_depth_2.iloc[matched_idx]
                layers.append({
                    "points": [(borehole_position_1, upper_depth_draw_1),
                            (borehole_position_2, upper_depth_draw_2),
                            (borehole_position_2, lower_depth_draw_2),
                            (borehole_position_1, lower_depth_draw_1)],
                    "color": color_mapping[str(type_1)],
                    "label": type_1 if type_1 not in legend_labels else None
                })
                matched_layers_1.add(idx_1)
                matched_layers_2.add(matched_idx)
                legend_labels.add(type_1)
                upper_depth_draw_1 = lower_depth_draw_1
                upper_depth_draw_2 = lower_depth_draw_2
                count_1[type_1] -= 1
                count_2[type_2] -= 1
                idx_1 += 1
                idx_2 = matched_idx + 1
                print('向下找3個type_2，如果3個type_2以內有1個以上的type_1',idx_1,idx_2)

            else:  # 如果只有0個匹配
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
                print('增加厚度為0的土層',idx_1)

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