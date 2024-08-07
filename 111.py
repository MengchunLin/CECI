import pandas as pd
import matplotlib.pyplot as plt

# 讀取 Excel 檔案
df孔1 = pd.read_excel('profile_test.xlsx', sheet_name='borehole-02')
df孔2 = pd.read_excel('profile_test.xlsx', sheet_name='borehole-04')

# 提取數據
深度孔1 = df孔1['depth']
土層孔1 = df孔1['borehole2']

深度孔2 = df孔2['depth']
土層孔2 = df孔2['borehole4']

# 顏色字典
color = {
    '1': 'yellow',
    '2': 'green',
    '3': 'blue',
    '4': 'red',
}

# 畫圖
plt.figure(figsize=(12, 8))

# 繪製孔1的剖面圖
for i in range(len(深度孔1) - 1):
    plt.barh(
        y=深度孔1[i] + (深度孔1[i+1] - 深度孔1[i]) / 2,  # 中間點
        width=深度孔1[i+1] - 深度孔1[i],
        height=0.8,
        color=color.get(土層孔1[i], 'grey'),
        edgecolor='black'
    )

# 繪製孔2的剖面圖
for i in range(len(深度孔2) - 1):
    plt.barh(
        y=深度孔2[i] + (深度孔2[i+1] - 深度孔2[i]) / 2 + 10,  # 調整位置以避免與孔1重疊
        width=深度孔2[i+1] - 深度孔2[i],
        height=0.8,
        color=color.get(土層孔2[i], 'grey'),
        edgecolor='black'
    )

plt.xlabel('深度')
plt.ylabel('鑽孔位置')
plt.title('鑽孔剖面圖')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()
