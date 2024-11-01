import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

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

# 自動命名並選擇儲存路徑
def auto_save_file(file_path):
    directory, original_filename = os.path.split(file_path)
    name, ext = os.path.splitext(original_filename)
    new_filename = f"{name}_statistical_depth{ext}"
    save_path = os.path.join(directory, new_filename)
    print(f"自動儲存檔案: {save_path}")
    return save_path

# 統計每種土壤的深度範圍，並計算平均IC（前200筆資料不納入計算）
def calculate_depth_statistics_with_qc_avg(df, original_file_path):
    depth_col = df['Depth (m)']
    type_col = df['合併後']
    ic_col = df['Ic']
    Mark_1 = df['Mark1']
    Mark_2 = df['Mark2']
    Bq = df['Bq']

    # 準備變量來記錄每段土壤的範圍和平均IC值
    result = []
    current_type = type_col.iloc[0]  # 從第201筆資料開始
    start_depth = depth_col.iloc[0]
    ic_values = []

    # 遍歷每一行，從第201筆開始，當遇到土壤類型變化或標記改變時，記錄當前土壤段的範圍
    for i in range(201, len(df)):
        if type_col.iloc[i] != current_type:  # 當類型變化時，記錄當前段的數據
            end_depth = depth_col.iloc[i - 1]
            average_ic = sum(ic_values) / len(ic_values) if ic_values else None
            result.append([current_type, start_depth, end_depth, average_ic])
            current_type = type_col.iloc[i]
            start_depth = depth_col.iloc[i]
            ic_values = []  # 重置IC值列表

        # 僅在條件符合時記錄 Ic 值
        if Mark_2.iloc[i] != '*' and pd.notna(Bq.iloc[i]) and Bq.iloc[i] != 0 and Mark_1.iloc[i] != '*':
            ic_values.append(ic_col.iloc[i])

    # 記錄最後一段土壤的範圍及平均IC值
    end_depth = depth_col.iloc[-1]
    average_ic = sum(ic_values) / len(ic_values) if ic_values else None
    result.append([current_type, start_depth, end_depth, average_ic])

    # 創建 DataFrame 保存結果
    depth_stats_df = pd.DataFrame(result, columns=['Type', 'Upper Depth', 'Lower Depth', 'Average Ic'])

    # 自動保存結果
    save_path = auto_save_file(original_file_path)
    depth_stats_df.to_excel(save_path, index=False)
    print(f"結果已自動保存到: {save_path}")

    return depth_stats_df

# 主程式
if __name__ == "__main__":

    procerssed_files = []
    for i in range(2):
    # 選擇文件
        file_path = select_file()
        # 讀取數據
        new_df = read_data(file_path)
        procerssed_files.append(file_path)

    # 計算深度範圍及平均 IC，並保存結果於自動命名的 xlsx 文件
    calculate_depth_statistics_with_qc_avg(new_df, file_path)
