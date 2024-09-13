import pandas as pd
import tkinter as tk
from tkinter import filedialog

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    print(f"選擇的檔案: {file_path}")
    return file_path

# 讀取 Excel 檔案
selected_file = select_file()
df = pd.read_excel(selected_file, header=0)

# 複製 DataFrame
df_copy = df.copy()

# 假設你想從第 10 行開始處理第二欄
start_row = 10 # 第十行的索引（Python 從 0 開始）
column_index = 2  # 第二欄的索引

# 獲取要處理的列
fs = df_copy.iloc[start_row:, column_index]

# 找到需要清除的單元格範圍
cells_to_clear = []
empty_count = 0
for i, value in enumerate(fs):
    if pd.isna(value) or value == '':  # 檢查 NaN 或空字符串
        start_clear = start_row + i - 2  # 第一個空格上面的兩個值
        end_clear = start_row + i + 8  # 最後一個空格往下的八個值
        cells_to_clear.extend(range(start_clear, end_clear + 1))
    # 如果不是空白值，則不做處理，也不需要重置 empty_count


# 清除找到的單元格值
cleared_count = 0
for row in cells_to_clear:
    if row < len(df_copy):
        df_copy.iloc[row, 1] = None
        df_copy.iloc[row, 2] = None  # 將值設為 None（在 Excel 中顯示為空白）
        df_copy.iloc[row, 3] = None
        cleared_count += 1

# 將處理後的資料寫入新的 Excel 檔案
new_file_path = 'processed_data-02.xlsx'
df_copy.to_excel(new_file_path, index=False)

print(f"處理後的資料已儲存到 {new_file_path}")
print(f"清除的單元格數: {cleared_count}")