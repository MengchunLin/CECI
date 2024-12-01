import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog
import json
from tkinter import messagebox

created_file = []
# 選擇檔案
def select_file():
    root = tk.Tk()
    root.withdraw()
    file= filedialog.askopenfilename(title="選擇檔案")
    return file

# 設定合併層厚度閾值
def get_thickness_threshold():
    root = tk.Tk()
    root.withdraw()
    thickness_threshold = (simpledialog.askinteger(
    "合併層厚度", 
    "請輸入合併厚度 (cm):\n最小建議厚度為100cm"
    )) / 2
    if thickness_threshold is None:
        thickness_threshold = 5  # 默認為5cm
    root.destroy()
    return thickness_threshold

# 分類土壤類型
def classify_soil_type(Ic):
    # 把Ic轉為float

    Ic = round(Ic, 2)
    if Ic <= 2.05:
        return 1
    elif 2.05 < Ic <= 2.3:
        return 2
    elif 2.3 < Ic < 2.6:
        return 3
    elif 2.6 < Ic < 2.95:
        return 4
    elif Ic >= 2.95:
        return 5

# 標記差異
def mark(previous_data, current_data):
    mark_list = [''] * len(current_data)
    for i in range(len(current_data)):
        if i < len(previous_data) and previous_data[i] != current_data[i]:
            mark_list[i] = '*'
    return mark_list

# 數據組織 (土壤類型、厚度、Ic 平均)
def data_array(Soil_Type, Ic):
    layer, thickness, ic_avg = [], [], []
    current_soil_type = None
    current_count = 0

    for i in range(len(Soil_Type)):
        soil_type = Soil_Type[i]
        if soil_type != current_soil_type and current_soil_type is not None:
            layer.append(current_soil_type)
            thickness.append(current_count)
            ic_avg.append(np.mean(Ic[i - current_count:i]))
            current_count = 0

        current_soil_type = soil_type
        current_count += 1

    if current_soil_type is not None:
        layer.append(current_soil_type)
        thickness.append(current_count)
        ic_avg.append(np.mean(Ic[len(Soil_Type) - current_count:]))

    return [layer, thickness, ic_avg]

# 合併層
def merge_layer(soil_data, thickness_threshold):
    i = 0  # Start index at 0 and manually control the iteration
    while i < len(soil_data):
        if soil_data.iloc[i, 1] <= thickness_threshold:
            if i == len(soil_data) - 1:  # If it's the last row
                soil_data.iloc[i - 1, 1] += soil_data.iloc[i, 1]  # Merge with the previous row
                soil_data.iloc[i, 0] = soil_data.iloc[i - 1, 0]  # Adjust layer designation
            else:
                if soil_data.iloc[i + 1, 0] == soil_data.iloc[i - 1, 0]:  # Merge with surrounding layers
                    soil_data.iloc[i - 1, 1] += soil_data.iloc[i, 1]
                elif soil_data.iloc[i - 1, 0] != soil_data.iloc[i + 1, 0]:
                    if abs(soil_data.iloc[i - 1, 2] - soil_data.iloc[i, 2]) > abs(soil_data.iloc[i, 2] - soil_data.iloc[i + 1, 2]):
                        soil_data.iloc[i + 1, 1] += soil_data.iloc[i, 1]  # Merge with the next row
                    else:
                        soil_data.iloc[i - 1, 1] += soil_data.iloc[i, 1]  # Merge with the previous row
            
            # Drop the current row after merging
            soil_data = soil_data.drop(i).reset_index(drop=True)
            i -= 1  # Move back one index to compensate for the dropped row
        
        i += 1  # Move to the next index

    return soil_data

# 簡化合併soil data
def merge_processed_data(soil_data):
    i = 0
    while i < len(soil_data) - 1:
        # 如果相邻两行的土壤类型相同
        if soil_data.iloc[i, 0] == soil_data.iloc[i + 1, 0]:
            # 合并厚度
            soil_data.iloc[i, 1] += soil_data.iloc[i + 1, 1]
            
            # 删除合并后的行
            soil_data = soil_data.drop(i + 1).reset_index(drop=True)
        else:
            # 只有在没有合并的情况下才增加索引
            i += 1
    
    return soil_data

# 生成最終數據
def write_merged_data(soil_data):
    data_input = []
    for i in range(len(soil_data)):
        soil_type = soil_data.iloc[i, 0]
        thickness = int(soil_data.iloc[i, 1])
        data_input.extend([soil_type] * thickness)
    return data_input

def process_file(file, thickness_threshold):
    df = pd.read_excel(file, header=0)
    df_copy = df.copy()

    # 資料處理
    # 把Ic轉為float
    df_copy['Ic'] = df_copy['Ic'].replace(' ', 0).astype(float)
    df_copy['Ic'] = df_copy['Ic'].interpolate(method='linear')
    df_copy['Soil Type'] = df_copy['Soil Type'].ffill()

    # 分類土壤類型
    Soil_Type_5 = df_copy['Ic'].apply(classify_soil_type)
    df_copy['Soil Type 5 type'] = Soil_Type_5
    df_copy['Mark1'] = ''

    # 計算層數、厚度和 Ic 平均值
    layers, thicknesses, ic_avgs = data_array(Soil_Type_5, df_copy['Ic'])
    result_df = pd.DataFrame({'Soil Type': layers, 'Thickness': thicknesses, 'Ic_avg': ic_avgs})

    # 第一次合併（合併厚度 <= 5cm）
    result_array1 = merge_layer(result_df, 5)

    # 寫入第一次處理後的數據
    data_input1 = write_merged_data(result_array1)
    df_copy['10cm'] = data_input1
    df_copy['Mark2'] = ''
    result_array1 = merge_processed_data(result_array1)
    
    # 確保數據長度匹配
    if len(data_input1) > len(df_copy):
        data_input1 = data_input1[:len(df_copy)]  # 截斷數據以匹配長度
    elif len(data_input1) < len(df_copy):
        data_input1.extend([''] * (len(df_copy) - len(data_input1)))  # 填充空值以匹配長度

    #對比soil type 5 和 5cm
    mark_array = mark(Soil_Type_5, data_input1)

    # 標記第一次合併後的數據
    df_copy['Mark1'] = mark_array

    # 第二次合併（基於用戶輸入的厚度閾值）
    result_array2 = merge_layer(result_array1, thickness_threshold)

    # 寫入第二次處理後的數據
    data_input = write_merged_data(result_array2)

    # 確保數據長度匹配
    if len(data_input) > len(df_copy):
        data_input = data_input[:len(df_copy)]  # 截斷數據以匹配長度
    elif len(data_input) < len(df_copy):
        data_input.extend([''] * (len(df_copy) - len(data_input)))  # 填充空值以匹配長度

    df_copy['合併後'] = data_input

    # 標記第二次合併後的數據
    mark_array = mark(data_input1, data_input)
    df_copy['Mark2'] = mark_array  # 標記第二次合併的變化

    # 將處理後的資料存入新的 Excel 檔案
    processed_file = file.replace('.xlsx', '_processed.xlsx')
    df_copy.to_excel(processed_file, index=False)
    created_file.append(processed_file)
    print(f'處理完成，已儲存：{processed_file}')
    return processed_file
# 輸入檔案名稱及位置
import tkinter as tk
from tkinter import messagebox
import sys

def input_file_name_and_position():
    """輸入鑽孔名稱及位置，返回兩者值。"""
    root = tk.Tk()
    root.withdraw()  # 隱藏主窗口

    user_input = {}

    def on_confirm():
        user_input['file_name'] = file_name_entry.get()
        user_input['position'] = float(position_entry.get())
        if user_input['file_name'] and user_input['position']:
            input_window.destroy()  # 關閉輸入窗口
            root.quit()  # 結束主事件循環
        else:
            messagebox.showwarning("輸入錯誤", "請完整輸入鑽孔名稱和位置")

    def on_cancel():
        user_input['file_name'] = None
        user_input['position'] = None
        input_window.destroy()  # 關閉輸入窗口
        root.quit()  # 結束主事件循環
        sys.exit("使用者取消操作，程式已退出")

    input_window = tk.Toplevel(root)
    input_window.title("輸入鑽孔名稱及位置")
    input_window.geometry("300x200")

    tk.Label(input_window, text="請輸入鑽孔名稱:").pack(pady=10)
    file_name_entry = tk.Entry(input_window)
    file_name_entry.pack(pady=5)

    tk.Label(input_window, text="請輸入位置 (x軸):").pack(pady=10)
    position_entry = tk.Entry(input_window)
    position_entry.pack(pady=5)

    tk.Button(input_window, text="確定", command=on_confirm).pack(side=tk.LEFT, padx=20, pady=20)
    tk.Button(input_window, text="取消", command=on_cancel).pack(side=tk.RIGHT, padx=20, pady=20)

    root.mainloop()  # 啟動事件循環
    return user_input['file_name'], user_input['position']

# 輸入預測位置及鑽孔名稱
def input_prediction():
    """輸入預測位置及鑽孔名稱，返回兩者值。"""
    root = tk.Tk()
    root.title("輸入預測位置及鑽孔名稱")
    root.geometry("300x200")

    user_input = {}

    def on_confirm():
        """確認按鈕的動作"""
        user_input['prediction'] = prediction_entry.get()
        user_input['prediction_position'] = float(prediction_position_entry.get())
        if user_input['prediction'] and user_input['prediction_position']:
            root.quit()  # 使用 quit() 結束 mainloop
        else:
            messagebox.showwarning("輸入錯誤", "請輸入完整的預測位置和鑽孔名稱！")

    def on_cancel():
        """取消按鈕的動作"""
        user_input['prediction'] = None
        user_input['prediction_position'] = None
        root.quit()  # 終止 mainloop

    # 創建輸入框和標籤
    tk.Label(root, text="請輸入預測鑽孔名稱:").pack(pady=10)
    prediction_entry = tk.Entry(root)
    prediction_entry.pack(pady=5)

    tk.Label(root, text="請輸入預測位置 (x軸):").pack(pady=10)
    prediction_position_entry = tk.Entry(root)
    prediction_position_entry.pack(pady=5)

    # 確認和取消按鈕
    tk.Button(root, text="確定", command=on_confirm).pack(side=tk.LEFT, padx=20, pady=20)
    tk.Button(root, text="取消", command=on_cancel).pack(side=tk.RIGHT, padx=20, pady=20)

    root.mainloop()  # 進入事件循環

    return user_input['prediction'], user_input['prediction_position']

from typing import Dict
# 用清單儲存每次處理後的檔案路徑
processed_files = []
def main():
    # 獲取閾值並初始化列表儲存處理結果
    thickness_threshold = get_thickness_threshold()
    processed_files = []
    result: Dict[str, str | float]= {
        "file1": "",
        "positions_1": 0.0,
        "file2": "",
        "positions_2": 0.0,
        "prediction": "",
        "prediction_position": 0.0,
        "weight_1": 0.0,
        "weight_2": 0.0,
    }
    # 假設處理兩個檔案
    for i in range(2):
        file = select_file()
        file_name, position = input_file_name_and_position()
        result[f"file{i+1}"] = file_name
        result[f"positions_{i+1}"] = position
        processed_file = process_file(file, thickness_threshold)
        processed_files.append(processed_file)

    # 輸入預測鑽孔位置
    prediction, prediction_position = input_prediction()
    result["prediction"] = prediction
    result["prediction_position"] = prediction_position
    print("預測鑽孔位置：", prediction)

    # 將處理後的檔案列表寫入文件
    with open("processed_files.xlsx", "w") as f:
        f.write("\n".join(processed_files))
    print("所有檔案簡化土層完成")

    # 將檔案名稱寫入 JSON 文件
    output_file = "result.json"

    with open(output_file, "w") as json_file:
        json.dump(result, json_file, indent=4)
        
    print(f"已儲存的檔案：{processed_files}")

if __name__ == "__main__":
    main()