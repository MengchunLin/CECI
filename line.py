import pandas as pd
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# tkinter 選擇文件
def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    print(f"Selected file: {file_path}")
    return file_path

# 讀取數據
def read_data(file_path):
    data = pd.read_excel(file_path)
    return data

# 統計每種土壤的深度範圍，當遇到土壤類型變化時記錄範圍
def calculate_depth_statistics(df):
    # 假設 df 包含 'Depth (m)', 'qc (MPa)', '合併後' 三列
    depth_col = df['Depth (m)']
    type_col = df['合併後']

    # 準備變量來記錄每段土壤的範圍
    result = []
    current_type = type_col.iloc[0]
    start_depth = depth_col.iloc[0]

    # 遍歷每一行，當遇到土壤類型變化時，記錄當前土壤段的範圍
    for i in range(1, len(df)):
        if type_col.iloc[i] != current_type:
            # 土壤類型變化，記錄當前土壤的上限和下限
            end_depth = depth_col.iloc[i-1]
            result.append([current_type, start_depth, end_depth])
            
            # 更新當前土壤類型和新的開始深度
            current_type = type_col.iloc[i]
            start_depth = depth_col.iloc[i]

    # 記錄最後一段土壤的範圍
    result.append([current_type, start_depth, depth_col.iloc[-1]])

    # 創建 DataFrame 保存結果
    depth_stats_df = pd.DataFrame(result, columns=['Type', 'Upper Depth', 'Lower Depth'])
    
    print("土壤類型深度統計：")
    print(depth_stats_df)

    # 將結果保存為 Excel 文件
    depth_stats_df.to_excel('soil_depth_statistics.xlsx', index=False, engine='openpyxl')
    
    return depth_stats_df

# 繪製數據圖像
def plot_data(df):
    # 假設 df 包含 'Depth', 'Value', 'Type' 三列
    plot_depth = df['Depth (m)']
    plot_value = df['qc (MPa)']
    plot_type = df['合併後']

    print(plot_type)

    # 定義顏色函數，根據類型返回對應顏色
    def get_color(plot_type_value):
        if plot_type_value == 1:
            return 'red'
        elif plot_type_value == 2:
            return 'orange'
        elif plot_type_value == 3:
            return 'green'
        elif plot_type_value == 4:
            return 'blue'
        else:
            return 'black'
    
    # 创建图形
    fig, ax = plt.subplots(figsize=(6, 12))
    
    # x軸範圍 0-70，y軸範圍 0-110
    plt.xlim(0, 70)
    plt.ylim(0, 110)

    # 繪製每一段的線條
    for i in range(len(plot_type)-1):
        color = get_color(plot_type.iloc[i])
        print(color)
        ax.plot(plot_value.iloc[i:i+2], plot_depth.iloc[i:i+2], color=color, lw=2)
    
    # 反轉y軸
    plt.gca().invert_yaxis()

    # 添加圖例
    red_patch = mpatches.Patch(color='red', label='Type 1')
    orange_patch = mpatches.Patch(color='orange', label='Type 2')
    green_patch = mpatches.Patch(color='green', label='Type 3')
    blue_patch = mpatches.Patch(color='blue', label='Type 4')
    black_patch = mpatches.Patch(color='black', label='Other')
    plt.legend(handles=[red_patch, orange_patch, green_patch, blue_patch, black_patch])
    
    # 添加標籤和標題
    plt.xlabel('qt(MPa)')
    plt.ylabel('Depth (m)')
    plt.title('50cm-03 qc and soil type')
    
    # 添加網格
    plt.grid(linestyle='--', linewidth=0.5)
    
    # 設置 x 和 y 軸的刻度
    x_major_locator = plt.MultipleLocator(5)
    y_major_locator = plt.MultipleLocator(2)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.yaxis.set_major_locator(y_major_locator)

    # 保存圖片
    plt.savefig('50m-03_qc_and_soil_type.png')

    # 顯示圖片
    plt.show()

# 主程式
if __name__ == "__main__":
    # 選擇文件
    file_path = select_file()

    # 讀取數據
    new_df = read_data(file_path)

    # 繪製圖像
    plot_data(new_df)

    # 計算深度範圍並保存結果於一個新的 xlsx 文件
    calculate_depth_statistics(new_df)
