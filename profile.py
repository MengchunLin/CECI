import numpy as np
import matplotlib.pyplot as plt

# 创建两个数组
array1 = np.random.randint(0, 10, size=(10, 10))
array2 = np.random.randint(0, 10, size=(10, 10))

# 找到两个数组中相同的部分
same_elements = array1 == array2

# 创建一个空白图像
image = np.zeros_like(array1, dtype=np.uint8)

# 将相同部分的值设为1
image[same_elements] = 1

# 绘制图像
plt.imshow(image, cmap='gray', interpolation='none')
plt.title('Connected Same Elements')
plt.show()
