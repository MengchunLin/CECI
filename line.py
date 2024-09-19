import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# 读取Excel文件
file_path = 'data.xlsx'  # 替换为你的Excel文件路径
sheet_name = '工作表1'  # 如果你知道工作表名称，填入这里
data = pd.read_excel(file_path, sheet_name=sheet_name)

# 假设Excel文件有两列，分别为 'X' 和 'Y'
x = data['X']
y = data['Y']

# 过滤掉包含 NaN 的行
mask_not_nan = ~(x.isna() | y.isna())
x = x[mask_not_nan]
y = y[mask_not_nan]

# 过滤掉 X 或 Y 为 0 的数据点
mask_not_zero = (x != 0) & (y != 0)
x_filtered = x[mask_not_zero]
y_filtered = y[mask_not_zero]

# 定义正弦函数用于拟合
def sin_func(x, A, B, C, D):
    return A * np.sin(B * x + C) + D

# 定义分段点（这里假设我们将数据分为3段）
segments = [x_filtered.min(), x_filtered.min() + (x_filtered.max() - x_filtered.min()) / 3,
            x_filtered.min() + 2 * (x_filtered.max() - x_filtered.min()) / 3, x_filtered.max()]

# 创建一个图形对象
plt.figure(figsize=(12, 8))

# 对每个段落进行拟合和预测
colors = ['red', 'green', 'blue']
for i in range(len(segments) - 1):
    start, end = segments[i], segments[i+1]
    mask = (x_filtered >= start) & (x_filtered < end)
    
    x_segment = x_filtered[mask]
    y_segment = y_filtered[mask]
    
    # 使用 curve_fit 拟合正弦函数
    params, _ = curve_fit(sin_func, x_segment, y_segment, p0=[1, 1, 0, np.mean(y_segment)])
    
    # 生成拟合曲线的点
    x_fit = np.linspace(start, end, 500)
    y_fit = sin_func(x_fit, *params)
    
    # 绘制原始数据点和拟合曲线
    plt.scatter(x_segment, y_segment, alpha=0.5, label=f'Data Points Segment {i+1}')
    plt.plot(x_fit, y_fit, color=colors[i], label=f'Sinusoidal Fit Segment {i+1}')

# 反转 Y 轴
plt.gca().invert_yaxis()

# 添加标签
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('XY Plot with Segmented Sinusoidal Trend Lines')
plt.legend()

# 保存图片
plt.savefig('分段周期趨勢線.png')

# 显示图形
plt.show()

# 预测缺失值
predicted_y = np.array([])
for i in range(len(segments) - 1):
    start, end = segments[i], segments[i+1]
    mask = (x >= start) & (x < end)
    
    x_segment = x_filtered[x_filtered >= start][x_filtered < end]
    y_segment = y_filtered[x_filtered >= start][x_filtered < end]
    
    params, _ = curve_fit(sin_func, x_segment, y_segment, p0=[1, 1, 0, np.mean(y_segment)])
    
    predicted = sin_func(x[mask], *params)
    predicted_y = np.concatenate([predicted_y, predicted])

# 将预测结果添加到原始数据框中
data['Predicted_Y'] = predicted_y

# 计算预测误差
data['Error'] = data['Y'] - data['Predicted_Y']
mse = np.mean(data['Error']**2)
print(f"Mean Squared Error: {mse}")

# 保存结果到新的Excel文件
data.to_excel('predicted_data.xlsx', index=False)

print("分析完成，结果已保存到 'predicted_data.xlsx'")