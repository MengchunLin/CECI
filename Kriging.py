from scipy.spatial.distance import pdist, squareform
import numpy as np
import scipy.linalg as la

# 已知鑽孔的位置和測量值
positions = np.array([1, 1559.53])
values = np.array([38.72, 37.92])

# 預測點位置
pos_pred = 781.48

# 定義球狀半變異函數模型
def spherical_variogram(h, range_, sill):
    return np.where(h <= range_, sill * (1.5 * (h / range_) - 0.5 * (h / range_) ** 3), sill)

# 設定半變異函數參數
range_ = 1559.53  # 半變異函數的影響範圍
sill = 1       # 極差

# 計算已知點之間的距離矩陣
dist_matrix = squareform(pdist(positions.reshape(-1, 1), metric='euclidean'))

# 計算半變異函數值（已知點之間的半變異函數值矩陣）
gamma_matrix = spherical_variogram(dist_matrix, range_, sill)

# 增加普通克利金中的拉格朗日乘數條件
gamma_matrix = np.vstack([np.hstack([gamma_matrix, np.ones((len(positions), 1))]),
                          np.hstack([np.ones((1, len(positions))), np.zeros((1, 1))])])
print('gamma_matrix'+'\n',gamma_matrix)


# 計算預測點到已知點的距離
dist_pred_to_known = np.abs(positions - pos_pred)
print(dist_pred_to_known)

# 計算預測點到已知點的半變異函數值
gamma_pred = spherical_variogram(dist_pred_to_known, range_, sill)


# 增加拉格朗日乘數條件
gamma_pred = np.append(gamma_pred, [1])
print('gamma_pred',gamma_pred)


# 解普通克利金方程組
weights = la.solve(gamma_matrix, gamma_pred)

# 提取權重（不包含最後的拉格朗日乘數）
weights_known = weights[:-1]
print('weights_known',weights_known)

# 使用權重計算預測點的值
P3_value_ordinary = np.dot(weights_known, values)
print(P3_value_ordinary)
