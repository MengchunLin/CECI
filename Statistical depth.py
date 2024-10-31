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

# 選擇儲存位置及名稱
def select_save_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
    if not file_path:  # 如果使用者取消了儲存對話框
        print("未選擇儲存檔案。")
        return None
    print(f"Selected file: {file_path}")
    return file_path

# 統計每種土壤的深度範圍，並計算平均IC（前200筆資料不納入計算）
def calculate_depth_statistics_with_qc_avg(df):
    depth_col = df['Depth (m)']
    type_col = df['合併後']
    ic_col = df['Ic']
    Mark_1 = df['Mark1']
    Mark_2 = df['Mark2']
    SBTn = df['SBTn']
    Bq = df['Bq']

    # 準備變量來記錄每段土壤的範圍和平均IC值
    result = []
    current_type = type_col.iloc[0]  # 從第201筆資料開始
    start_depth = depth_col.iloc[0]

    ic_values = []

# 遍歷每一行，從第201筆開始，當遇到土壤類型變化或標記改變時，記錄當前土壤段的範圍
# 遍歷每一行，從第201筆開始，當遇到土壤類型變化或標記改變時，記錄當前土壤段的範圍
    for i in range(201, len(df)):
        # 總是記錄範圍，不受條件影響
        if type_col.iloc[i] != current_type:  # 當類型變化時，記錄當前段的數據
            # 記錄當前土壤的範圍
            end_depth = depth_col.iloc[i - 1]
            if len(ic_values) > 0:  # 確保列表不為空
                average_ic = sum(ic_values) / len(ic_values)  # 計算該段土壤的平均IC
            else:
                average_ic = None  # 如果沒有符合條件的IC，記為 None

            # 添加到結果中
            result.append([current_type, start_depth, end_depth, average_ic])

            # 更新當前土壤類型和新的開始深度
            current_type = type_col.iloc[i]
            start_depth = depth_col.iloc[i]
            ic_values = []  # 重置IC值列表

        # 僅在條件符合時記錄 Ic 值
        if Mark_2.iloc[i] != '*' and pd.notna(Bq.iloc[i]) and Bq.iloc[i] != 0 and Mark_1.iloc[i] != '*':
            ic_values.append(ic_col.iloc[i])

    # 記錄最後一段土壤的範圍及平均IC值
    end_depth = depth_col.iloc[-1]
    if len(ic_values) > 0:
        average_ic = sum(ic_values) / len(ic_values)
    else:
        average_ic = None
    result.append([current_type, start_depth, end_depth, average_ic])



    # 創建 DataFrame 保存結果
    depth_stats_df = pd.DataFrame(result, columns=['Type', 'Upper Depth', 'Lower Depth', 'Average Ic'])

    print("土壤類型深度統計和平均 IC（排除前200筆資料，且排除 Mark2 有 *、SBTn=0 或 Mark1 有 * 的數據）：")
    print(depth_stats_df)

    # 選擇保存路徑
    save_path = select_save_file()
    if save_path:  # 如果成功選擇保存路徑，則保存文件
        depth_stats_df.to_excel(save_path, index=False)
        print(f"結果已保存到: {save_path}")
    else:
        print("未保存檔案。")
    
    return depth_stats_df



# 主程式
if __name__ == "__main__":
    # 選擇文件
    file_path = select_file()

    # 讀取數據
    new_df = read_data(file_path)



    # 計算深度範圍及平均 IC，並保存結果於一個新的 xlsx 文件
    calculate_depth_statistics_with_qc_avg(new_df)
