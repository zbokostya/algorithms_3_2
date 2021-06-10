
# Функция нахождения минимального элемента, исключая текущий элемент
def Min(lst, myindex):
    return min(x for idx, x in enumerate(lst) if idx != myindex)


# функция удаления нужной строки и столбцах
def Delete(matrix, index1, index2):
    del matrix[index1]
    for i in matrix:
        del i[index2]
    return matrix



def insertInf(matrix):
    stroka = 0
    for i in range(len(matrix)):
        if inf not in matrix[i]:
            stroka = i
            column = []
            stolbets = 0
            for j in range(len(matrix)):
                column.append(matrix[j][i])
                stolbets = j
            if inf not in column:
                matrix[stroka][stolbets] = inf
                return


# Функция вывода матрицы
def PrintMatrix(matrix):
    print("---------------")
    for i in range(len(matrix)):
        print(matrix[i])
    print("---------------")


n = 6
matrix = []
H = 0
PathLenght = 0
Str = []
Stb = []
res = []
result = []
StartMatrix = []

for i in range(n):
    Str.append(i)
    Stb.append(i)

inf = float('inf')
matrix = [
    [inf, inf, 3, 4, 2, 8],
    [inf, inf, 7, 5, 8, 3],
    [3, 10, inf, 12, 6, 4],
    [4, 5, 12, inf, 8, 3],
    [2, 8, 6, 8, inf, 10],
    [8, inf, 4, 3, 10, inf]
]

for i in range(n): StartMatrix.append(matrix[i].copy())

while True:
    for i in range(len(matrix)):
        temp = min(matrix[i])
        H += temp
        for j in range(len(matrix)):
            matrix[i][j] -= temp

    for i in range(len(matrix)):
        temp = min(row[i] for row in matrix)
        H += temp
        for j in range(len(matrix)):
            matrix[j][i] -= temp

    NullMax = 0
    index1 = 0
    index2 = 0
    tmp = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0:
                tmp = Min(matrix[i], j) + Min((row[j] for row in matrix), i)
                if tmp >= NullMax:
                    NullMax = tmp
                    index1 = i
                    index2 = j

    res.append(Str[index1] + 1)
    res.append(Stb[index2] + 1)

    oldIndex1 = Str[index1]
    oldIndex2 = Stb[index2]

    if oldIndex2 in Str and oldIndex1 in Stb:
        NewIndex1 = Str.index(oldIndex2)
        NewIndex2 = Stb.index(oldIndex1)
        matrix[NewIndex1][NewIndex2] = float('inf')
    else:
        insertInf(matrix)

    del Str[index1]
    del Stb[index2]
    matrix = Delete(matrix, index1, index2)
    if len(matrix) == 1:
        break

print(res)
result = []

for i in range(0, len(res) - 1, 2):
    if res.count(res[i]) < 2:
        result.append(res[i])
        result.append("->")
        result.append(res[i + 1])

for i in range(0, len(res) - 1, 2):
    for j in range(0, len(res) - 1, 2):
        if result[len(result) - 1] == res[j]:
            result.append(res[j])
            result.append("->")
            result.append(res[j + 1])
result.append(result[len(result) - 1])
result.append("->")
result.append(result[0])

print("salesman")
for i in range(0, len(result), 3):
    print(result[i] - 1, result[i + 1], result[i + 2] - 1)
# -------------
print("floyd")
def floyd(matrix_dist):
    MAX_VAL = float('inf')
    indexes = [[0 for i in range(len(matrix_dist))] for j in range(len(matrix_dist))]
    for i in range(len(matrix_dist)):
        for j in range(len(matrix_dist)):
            indexes[i][j] = j

    for k in range(len(matrix_dist)):
        for i in range(len(matrix_dist)):
            if i == k or matrix_dist[i][k] == MAX_VAL:
                continue
            for j in range(len(matrix_dist)):
                if j == k or matrix_dist[k][j] == MAX_VAL:
                    continue
                if matrix_dist[i][k] + matrix_dist[k][j] < matrix_dist[i][j]:
                    matrix_dist[i][j] = matrix_dist[i][k] + matrix_dist[k][j]
                    indexes[i][j] = indexes[i][k]


floyd(matrix)
PrintMatrix(matrix)
