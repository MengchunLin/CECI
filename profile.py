import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#read excel file
df = pd.read_excel('profile_test.xlsx')

# 创建两个数组
#array = excel first column
array1 = df.iloc[:,0].values
print(array1)
array2 = df.iloc[:,1].values
print(array2)

# 找到两个数组中相同的部分
same_points = set(map(tuple, array1)).intersection(set(map(tuple, array2)))

# 将相同的部分转换回数组
same_points = np.array(list(same_points))

# 创建一个空白图像
image = np.zeros((100, 100), dtype=np.uint8)

# 在图像中将相同部分的值设为1
for point in same_points:
    image[point[0], point[1]] = 1

# 绘制图像
plt.imshow(image, cmap='gray', interpolation='none')
plt.title('Connected Same Points')
plt.show()
