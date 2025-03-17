A = [[1,0,-1],[8,18,49]]
B = [[7,8,6,5],[2,3,5,6],[4,3,2,6]]
C = [[0 for i in range(4)] for j in range(2)]
for i in range(len(A)):
    for j in range(len(B[0])):
        for k in range(len(B)):
            C[i][j]+=A[i][k]*B[k][j]
print(C)