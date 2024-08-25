import numpy as np

## A
M = np.arange(5, 21)
print(M, '\n')

## B
M = M.reshape(4, -1)
print(M, '\n')

## C
M[1:3, 1:3] = 0
print(M, '\n')

## D
M = np.dot(M, M)
print(M, '\n')

## E
sum = 0
for i in M[0]:
    sum +=  i ** 2
m = np.sqrt(sum)
print(m)