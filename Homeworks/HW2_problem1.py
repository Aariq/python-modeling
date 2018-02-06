import numpy as np
m = np.array([0, 1, 5/6, 0])
p = np.array([0.6, 0.8, 2/3, 0])
n = np.array([0.0, 1200.0, 900.0, 900.0])
n_next = np.array([0.0, 0.0, 0.0, 0.0])

for i in range(70):
    n_next[1:4] = n[0:3] * p[0:3]

    n_next[0] = np.dot(n_next[1:4], m[1:4])

    n = n_next
    print(n)
