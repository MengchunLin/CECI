import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# 假設已經讀取了數據
file_path = r'C:\Users\Janet\Desktop\CECI\data.xlsx'
data = pd.read_excel(file_path, sheet_name='工作表1')

# 確保數據按深度排序
data = data.sort_values(by='Y')

# 過濾掉含有 NaN 值的行
data_cleaned = data.dropna(subset=['X', 'Y'])

# 提取深度和 qc 值
depths = data_cleaned['Y'].values
qc_values = data_cleaned['X'].values

# 依照 0.25 公尺區間進行分組
interval = 0.25
min_depth = np.floor(depths.min() / interval) * interval
max_depth = np.ceil(depths.max() / interval) * interval
bins = np.arange(min_depth, max_depth + interval, interval)

# 初始化存儲分組結果的列表
avg_depths = []
avg_qc_values = []

# 對每個 0.25 公尺區間進行處理
for i in range(1, len(bins)):
    # 找到該區間內的數據點
    mask = (depths >= bins[i - 1]) & (depths < bins[i])
    if np.any(mask):  # 如果區間內有數據
        qc_in_bin = qc_values[mask]
        max_qc = np.max(qc_in_bin)
        min_qc = np.min(qc_in_bin)
        avg_qc = (max_qc + min_qc) / 2
        avg_depth = (bins[i - 1] + bins[i]) / 2
        
        avg_depths.append(avg_depth)
        avg_qc_values.append(avg_qc)


# 繪製原始數據點、每 0.25 公尺分組的最大最小平均值和線性回歸線
plt.figure(figsize=(12, 8))

# 繪製原始的 qc 值對應深度
plt.plot(qc_values, depths, 'go-', label='Original qc data')

# 繪製每 0.25 公尺的最大最小平均值
plt.plot(avg_qc_values, avg_depths, 'bo-', label='Averaged qc (max-min) per 0.25m')


# 設置標題和標籤
plt.xlabel('qc (MPa)')
plt.ylabel('Depth (m)')
plt.title('qc vs Depth with Original Data, Averaged qc')
plt.legend()

# 設置 XY 軸的刻度間隔為 0.25 並啟用網格
plt.gca().set_xticks(np.arange(min(qc_values), max(qc_values) + 0.25, 0.25))  # X 軸每 0.25 一格
plt.gca().set_yticks(np.arange(min(avg_depths), max(avg_depths) + 0.25, 0.25))  # Y 軸每 0.25 一格

plt.grid(True)  # 顯示網格

# 反轉 Y 軸，使深度正向向下
plt.gca().invert_yaxis()

# 保存圖形
plt.savefig('0.25取平均.png')

# 顯示圖形
plt.show()

# 輸出擬合的線性回歸參數
slope = model.coef_[0]
intercept = model.intercept_
print(f"線性回歸方程: Depth = {slope:.2f} * qc + {intercept:.2f}")
