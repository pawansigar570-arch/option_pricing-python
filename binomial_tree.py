import numpy as np

S = 100
K = 100
T = 1
r = 0.05
sigma = 0.2

N = 3

dt = T/N
u = np.exp(sigma*np.sqrt(dt))
d = 1/u
p = (np.exp(r*dt)-d)/(u-d)

stock = np.zeros(N+1)

for i in range(N+1):
    stock[i] = S*(u**(N-i))*(d**i)

option = np.maximum(stock-K,0)

for step in range(N-1,-1,-1):
    for i in range(step+1):
        option[i] = np.exp(-r*dt)*(p*option[i] + (1-p)*option[i+1])

print("Binomial Call Price =", option[0])