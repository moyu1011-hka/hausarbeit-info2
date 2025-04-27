# Sample 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 🔧 Generate 100 random data
np.random.seed(42)
n_days = 100
returns = np.random.normal(loc=0.001, scale=0.02, size=n_days)  # обычные доходности

# 📌 Log returns
log_returns = np.log(1 + returns)

# 📈 Cumulative returns
cumulative_simple = (1 + returns).cumprod() - 1

# 📉 Cumulative log returns
cumulative_log = np.exp(log_returns.cumsum()) - 1

# 📊 Graphic 
plt.figure(figsize=(10, 6))
plt.plot(cumulative_simple, label='Cumulative Return (Обычные доходности)', lw=2)
plt.plot(cumulative_log, label='Cumulative Return (Лог-доходности)', lw=2, linestyle='--')
plt.xlabel('День')
plt.ylabel('Накопленная доходность')
plt.title('Сравнение: обычные и логарифмические доходности')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
