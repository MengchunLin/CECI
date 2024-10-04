import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 读取两个文件
file_1_path = 'C:/Users/yo/Desktop/CECI/02-50cm-soil_depth_statistics_with_ic.xlsx'
file_2_path = 'C:/Users/yo/Desktop/CECI/04-50cm-soil_depth_statistics_with_ic.xlsx'

df_1 = pd.read_excel(file_1_path)
df_2 = pd.read_excel(file_2_path)

# 合并数据
df_combined = pd.concat([df_1, df_2], ignore_index=True)

# 检查缺失值并删除缺失值
df_combined = df_combined.dropna()

# 创建新的特征（例如深度的区间分类）
df_combined['Depth Category'] = pd.cut(df_combined['Upper Depth'], bins=10)

# 假设我们要预测地层类型
X = df_combined[['Upper Depth', 'Lower Depth', 'Average IC']]
y = df_combined['Type']

# 分割数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 初始化并训练模型
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估模型
print(classification_report(y_test, y_pred))

# 将预测结果添加到 DataFrame
df_combined['Predicted Type'] = model.predict(X)

# 将结果保存为 Excel
df_combined.to_excel('predicted_geology_layers.xlsx', index=False)

# 可视化地层剖面
# 定义颜色映射，每种地层类型使用不同的颜色
type_colors = {1: 'lightgreen', 2: 'lightblue', 3: 'yellow', 4: 'orange', 5: 'tan', 6: 'red'}

# 创建图形
fig, ax = plt.subplots(figsize=(8, 12))

# 遍历每一行，根据地层类型绘制对应的填充区域
for idx, row in df_combined.iterrows():
    upper_depth = row['Upper Depth']
    lower_depth = row['Lower Depth']
    pred_type = row['Predicted Type']
    
    # 获取颜色
    color = type_colors.get(pred_type, 'gray')
    
    # 绘制地层条状图（X轴代表样本编号，Y轴代表深度）
    ax.bar([idx], lower_depth - upper_depth, bottom=upper_depth, width=0.8, color=color, edgecolor='black')

# 设置坐标轴和标题
ax.set_title("Predicted Geology Layers by Depth")
ax.set_xlabel("Samples")
ax.set_ylabel("Depth (m)")

# 反转Y轴（地层从上到下）
ax.invert_yaxis()

# 添加图例
legend_labels = [f'Type {t}' for t in type_colors.keys()]
legend_colors = [plt.Line2D([0], [0], color=c, lw=4) for c in type_colors.values()]
ax.legend(legend_colors, legend_labels, title="Soil Types", loc="upper right")

plt.tight_layout()
plt.show()
