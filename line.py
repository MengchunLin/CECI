import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取Excel文件
file_path = 'data.xlsx'  # 替换为你的Excel文件路径
sheet_name = '工作表1'  # 如果你知道工作表名称，填入这里
data = pd.read_excel(file_path, sheet_name=sheet_name)

# 假设Excel文件有两列，分别为 'X' 和 'Y'
x = data['X']
y = data['Y']

# 绘制散点图
plt.scatter(x, y, label='Data Points')

# 计算线性拟合
coefficients = np.polyfit(x, y, 1)  # 1 表示线性拟合
trendline = np.polyval(coefficients, x)

# 绘制趋势线
plt.plot(x, trendline, color='red', label='Trend Line')

# 添加标签
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('XY Plot from Excel Data')
plt.legend()
plt.show()
