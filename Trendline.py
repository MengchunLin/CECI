import matplotlib.pyplot as plt
import numpy as np

# 生成深度数据
depth = np.linspace(0, 100, 500)
values = np.sin(depth / 10)

# 定义颜色函数，根据条件返回颜色
def get_color(value):
    if value > 0.5:
        return 'red'
    elif value > 0:
        return 'orange'
    elif value > -0.5:
        return 'green'
    else:
        return 'blue'

# 创建一个空白图
fig, ax = plt.subplots()

# 根据条件绘制线条
for i in range(len(depth) - 1):
    color = get_color(values[i])
    ax.plot(depth[i:i+2], values[i:i+2], color=color, lw=2)

plt.xlabel('Depth')
plt.ylabel('Value')
plt.title('Line with Different Colors Based on Values')
plt.show()
