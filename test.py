import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# 定義地層數據
layers = [
    {"name": "1", "color": "lightgreen", "points": [(0, 0.9), (6, 1), (6, 0), (0, 0)]},
    {"name": "CL1", "color": "lightblue", "points": [(0, 0.8), (6, 0.9), (6, 0.9), (0, 0.8)]},
    {"name": "SM2", "color": "yellow", "points": [(0, 0.6), (3, 0.7), (6, 0.8), (6, 0.6), (0, 0.6)]},
    {"name": "CL2", "color": "lightgreen", "points": [(0, 0.55), (6, 0.6), (6, 0.6), (0, 0.55)]},
    {"name": "SM3", "color": "orange", "points": [(2, 0.2), (4, 0.5), (6, 0), (2, 0.2)]},
    {"name": "CL3", "color": "tan", "points": [(0, 0), (6, 0), (6, 0.2), (0, 0.2)]}
]

# 創建圖形
fig, ax = plt.subplots(figsize=(10, 6))

# 繪製每個地層為多邊形
for layer in layers:
    polygon = Polygon(layer["points"], closed=True, color=layer["color"], alpha=0.7, label=layer["name"])
    ax.add_patch(polygon)

    # 計算每個地層的中心點，標注地層名稱
    center_x = sum(x for x, _ in layer["points"]) / len(layer["points"])
    center_y = sum(y for _, y in layer["points"]) / len(layer["points"])
    ax.text(center_x, center_y, layer["name"], color="black", ha="center", va="center", fontsize=10, weight="bold")

# 繪製鑽孔位置
drill_holes = [0, 3, 6]
for x in drill_holes:
    ax.axvline(x=x, color='yellow', linestyle='-', linewidth=2)

# 翻轉y軸，設置深度範圍從0到1
ax.set_ylim(1, 0)

# 設置圖形屬性
ax.set_xlim(0, 6)
ax.set_title("Kriging of Soil Layers")
ax.set_xlabel("Distance")
ax.set_ylabel("Depth")
ax.legend(loc='upper right')

plt.show()
