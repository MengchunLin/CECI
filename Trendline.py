import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# 假設你的數據保存在CSV文件中，讀取數據
df = pd.read_csv('Trendline-02.csv')

# 假設數據是兩列，depth和qc
depth = df['Depth (m)']
qc = df['qc (MPa)']

# 分段數據
segment_size = 250  # 每段的大小
segments = [depth[i:i + segment_size] for i in range(0, len(depth), segment_size)]
qc_segments = [qc[i:i + segment_size] for i in range(0, len(qc), segment_size)]

# 計算每段的斜率
slopes = []
for seg_depth, seg_qc in zip(segments, qc_segments):
    if len(seg_depth) > 1:
        slope, intercept, r_value, p_value, std_err = linregress(seg_depth, seg_qc)
        slopes.append((slope, intercept))
    else:
        slopes.append((None, None))

# 繪製圖表
plt.figure(figsize=(10, 6))
plt.plot(qc, depth, label='qc data', color='blue')

# 繪製趨勢線
for (slope, intercept), seg_depth in zip(slopes, segments):
    if slope is not None:
        plt.plot(slope * seg_depth + intercept, seg_depth, label=f'Segment trendline', color='red')

plt.gca().invert_yaxis()  # 反轉y軸，因為深度越深數值越大
plt.xlabel('qc')
plt.ylabel('Depth')
plt.title('Trendline-02')
plt.legend()
plt.savefig('Trendline-02.png')  # 保存圖表為PNG文件
plt.show()

