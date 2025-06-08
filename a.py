import numpy as np
import matplotlib.pyplot as plt

l = np.linspace(-1, 1, 1)
r = np.exp(1 * l)  # hàm mũ tạo hiệu ứng xoắn
x = r * np.cos(2 * np.pi * l)
y = r * np.sin(2 * np.pi * l)

plt.plot(x, y)
plt.title("Spiral curve")
plt.axis('equal')
plt.show()
