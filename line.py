import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy import optimize 

# 讀取 Excel 文件
file_path = r'C:\Users\Janet\Desktop\CECI\data.xlsx'
data = pd.read_excel(file_path, sheet_name='工作表1')

# 過濾掉含有 NaN 值的行
data_cleaned = data.dropna(subset=['X', 'Y'])

# 提取沒有 NaN 的 X 和 Y 值
x_values = data_cleaned['X'].values
y_values = data_cleaned['Y'].values

# 創建繪圖
plt.figure(figsize=(12, 9))

# 繪製原始數據點
plt.scatter(x_values, y_values, color='violet', alpha=0.5, label='qc')

# 計算線性趨勢線-------------------------------------
# slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
# line = slope * x_values + intercept

# # 繪製趨勢線
# plt.plot(x_values, line, color='skyblue', linestyle='--', label='Trend Line')

# # 計算 R 平方值
# r_squared = r_value**2

# # 添加線性方程式和 R 平方值到圖表
# equation = f'y = {slope:.4f}x + {intercept:.4f}'
# r_squared_text = f'R² = {r_squared:.4f}'
# plt.text(0.05, 0.95, equation + '\n' + r_squared_text, transform=plt.gca().transAxes,
#          verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# 定義指數函數-------------------------------------
# def exp_func(x, a, b):
#     return a * np.exp(b * x)

# 使用 curve_fit 進行指數擬合
# popt, pcov = optimize.curve_fit(exp_func, x_values, y_values)

# 生成用於繪製趨勢線的 x 值
# x_line = np.linspace(min(x_values), max(x_values), 100)

# 繪製指數趨勢線
# plt.plot(x_line, exp_func(x_line, *popt), color='red', linestyle='--', label='Exponential Trend')

# 計算 R 平方值
# residuals = y_values - exp_func(x_values, *popt)
# ss_res = np.sum(residuals**2)
# ss_tot = np.sum((y_values - np.mean(y_values))**2)
# r_squared = 1 - (ss_res / ss_tot)

# 設置圖表標籤和標題
# plt.xlabel('qc (MPa)')
# plt.ylabel('depth (m)')
# plt.title('Exponential Trend Line')

# 添加指數方程式和 R 平方值到圖表
# equation = f'y = {popt[0]:.4f} * e^({popt[1]:.4f}x)'
# r_squared_text = f'R² = {r_squared:.4f}'
# plt.text(0.05, 0.95, equation + '\n' + r_squared_text, transform=plt.gca().transAxes,
#          verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

#---------------------------------------------------

# 計算二次趨勢線-------------------------------------
#使用 numpy 的 polyfit 進行二次擬合 (degree=2)
#使用 numpy 的 polyfit 進行二次擬合 (degree=2)
# coefficients = np.polyfit(x_values, y_values, 2)
# quadratic_trend = np.polyval(coefficients, x_values)

# # 繪製二次趨勢線
# plt.plot(x_values, quadratic_trend, color='skyblue', linestyle='--', label='Quadratic Trend Line')

# # 計算 R 平方值
# residuals = y_values - quadratic_trend
# ss_res = np.sum(residuals**2)
# ss_tot = np.sum((y_values - np.mean(y_values))**2)
# r_squared = 1 - (ss_res / ss_tot)

# # 添加二次方程式和 R 平方值到圖表
# equation = f'y = {coefficients[2]:.4f} + {coefficients[1]:.4f}x + {coefficients[0]:.4f}x²'
# r_squared_text = f'R² = {r_squared:.4f}'
# plt.text(0.05, 0.95, equation + '\n' + r_squared_text, transform=plt.gca().transAxes,
#          verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# 計算三次趨勢線-------------------------------------
# 使用 numpy 的 polyfit 進行三次擬合 (degree=3)
coefficients = np.polyfit(x_values, y_values, 3)
cubic_trend = np.polyval(coefficients, x_values)

# 繪製三次趨勢線
plt.plot(x_values, cubic_trend, color='skyblue', linestyle='--', label='Cubic Trend Line')

# 計算 R 平方值
residuals = y_values - cubic_trend
ss_res = np.sum(residuals**2)
ss_tot = np.sum((y_values - np.mean(y_values))**2)
r_squared = 1 - (ss_res / ss_tot)

# 添加三次方程式和 R 平方值到圖表
equation = (f'y = {coefficients[3]:.4f} + {coefficients[2]:.4f}x '
            f'+ {coefficients[1]:.4f}x² + {coefficients[0]:.4f}x³')
r_squared_text = f'R² = {r_squared:.4f}'
plt.text(0.05, 0.95, equation + '\n' + r_squared_text, transform=plt.gca().transAxes,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
#---------------------------------------------------


# 設置圖表標籤和標題
plt.xlabel('qc (MPa)')
plt.ylabel('depth (m)')
plt.title('Trend Line 6-11m')

# 反轉 Y 軸
plt.gca().invert_yaxis()

# 添加圖例
plt.legend()

# 顯示網格
plt.grid(True)

# 保存圖表
plt.savefig('trend_line_index_6-11m.png')

# 顯示圖表
plt.show()

# 輸出被排除的點的數量
excluded_points = len(data) - len(data_cleaned)
print(f"排除的數據點數量: {excluded_points}")

# 輸出線性方程式和 R 平方值
print(f"線性方程式: {equation}")
print(f"R 平方值: {r_squared:.4f}")