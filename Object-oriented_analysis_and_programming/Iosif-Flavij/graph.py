import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Results.csv', header=None, names=['X', 'Y'])
df = df.sort_values('X')

plt.figure(figsize=(10, 6))
plt.plot(df['X'], df['Y'], marker='o', linewidth=2, markersize=4)

plt.xlabel('Amount numbers')
plt.ylabel('Time')
plt.title('Correlation between amount of numbers and time')
plt.grid()
plt.savefig('visual.png') 
plt.show()