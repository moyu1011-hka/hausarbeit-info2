import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 🔧 Генерируем синтетические данные: 100 дней, случайные доходности ~1%
np.random.seed(42)
n_days = 100
returns = np.random.normal(loc=0.001, scale=0.02, size=n_days)  # обычные доходности

# 📌 Логарифмические доходности
log_returns = np.log(1 + returns)

# 📈 Накопленная обычная доходность
cumulative_simple = (1 + returns).cumprod() - 1

# 📉 Накопленная логарифмическая доходность
cumulative_log = np.exp(log_returns.cumsum()) - 1

# 📊 Построение графика
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
#xgxfgxfg
