import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
import matplotlib.pyplot as plt


data = {
    'Needed procedure': [True, True, True, False, False, True, False, True, False, False, 
                         False, True, True, True, False, False, True, True, True, False, 
                         False, True, False, True, False],
    'Prediction score': [53, 87, 72, 12, 33, 32, 66, 91, 11, 58, 
                         42, 22, 35, 90, 85, 22, 98, 65, 32, 15, 
                         22, 48, 52, 59, 12]
}

df = pd.DataFrame(data)


X = df['Prediction score'].values.reshape(-1, 1)
y = df['Needed procedure'].astype(int).values


model = LogisticRegression()
model.fit(X, y)

y_probs = model.predict_proba(X)[:, 1]  

best_boundary = 0
best_fp = len(y)
best_accuracy = 0

for boundary in np.linspace(0, 1, 100):  
    y_pred = (y_probs >= boundary).astype(int)
    accuracy = accuracy_score(y, y_pred)
    fp = confusion_matrix(y, y_pred)[0, 1] 
    
    if accuracy >= 0.65 and fp < best_fp:
        best_fp = fp
        best_boundary = boundary
        best_accuracy = accuracy

print(f"Best boundary: {best_boundary:.2f}")
print(f"Best Accuracy: {best_accuracy:.2f}")
print(f"False Positives: {best_fp}")


plt.scatter(X[:, 0], y, color='blue', label='Actual')
plt.plot(X[:, 0], y_probs, color='green', label='Predicted Probabilities')
plt.axhline(y=best_boundary, color='red', linestyle='--', label=f'Threshold: {best_boundary:.2f}')
plt.xlabel('Prediction Score')
plt.ylabel('Probability')
plt.title('Decision Boundary with Low False Positives')
plt.legend()
plt.show()