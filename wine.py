import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = {
    'Alcohol': [10, 30, 20, 60, 50, 90, 20, 20, 60],
    'Acidity': [50, 60, 50, 10, 40, 80, 90, 70, 50],
    'Sweetness': [10, 30, 30, 60, 120, 80, 100, 130, 90],
    'Tannin': [20, 60, 80, 30, 100, 10, 110, 30, 60],
    'Body': [10, 10, 20, 30, 70, 50, 50, 80, 60],
    'Price': [0, 20, 15, 50, 80, 50, 60, 120, 80]
}
df = pd.DataFrame(data)

corr_matrix = df.corr()

plt.figure(figsize=(8, 6))
plt.imshow(corr_matrix, cmap='coolwarm', interpolation='nearest')
plt.title('Correlation Matrix')
plt.colorbar()
tick_marks = np.arange(len(corr_matrix.columns))
plt.xticks(tick_marks, corr_matrix.columns, rotation=45)
plt.yticks(tick_marks, corr_matrix.columns)
plt.tight_layout()
plt.show()