import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# 全局设置字体和字号
plt.rcParams['font.size'] = 20                  # 设置全局字号
plt.rcParams['mathtext.fontset'] = 'stix'       # 数学公式字体（与Times New Roman风格一致）

# 你的数据
n_noise_list_int = np.array([1, 2, 3, 4])
x_values = np.array(n_noise_list_int)
y_values = np.real(np.array([0.13280, 0.07428, 0.03862, 0.02536]))

# 定义多项式模型
def poly_func(x, a, b, c):
    return a * x**2 + b * x + c


# 拟合
popt, pcov = curve_fit(poly_func, x_values, y_values, p0=(1, -0.1, 0))
x_fit = np.linspace(-0.5, max(x_values), 100)
y_fit = poly_func(x_fit, *popt)

# 创建图表
plt.figure(figsize=(10, 6))

# 添加标题和标签（字号自动继承全局设置）
plt.title('ZNE for Ising model(n=9, 500 times)')
plt.xlabel('Number of Noisy Layer')
plt.ylabel('Expectation <Z0>')

# 设置坐标轴范围和刻度
# plt.xlim(-0.5, max(x_values) + 0.5)
# plt.ylim(0.00, 0.04)
# plt.xticks([0, 4, 8, 12, 16, 20])  # 手动设置x轴刻度

# 添加网格
plt.grid(True, linestyle='--', alpha=0.7)

# 绘制数据点、拟合曲线和理论值
theor_exp = 0.21607
plt.scatter(0, theor_exp, color='red', s=100, label='Theoretical expectation (no noise)')
plt.scatter(0, poly_func(0, *popt), color='blue', s=100, label='Fitted expectation (no noise)')
plt.scatter(x_values, y_values, facecolors='none', edgecolors='blue', s=100, label='Measured Data Points')
plt.plot(x_fit, y_fit, 'b-', label="Polynomial Fit", linewidth=2)

# 添加图例（字体自动继承全局设置）
plt.legend()

# 自动调整布局
plt.tight_layout()
plt.savefig('zne_extrapolation_plot.png')