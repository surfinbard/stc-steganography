## Import

import random

## Constant

cst_n = 3 #256
cst_grayLength = 256
cst_alpha = 1 #0.1
cst_h = 4
cst_w = 10

## Function

def createRandomImage():
    randomImage = []
    for i in range(cst_n):
        line = []
        for j in range(cst_n):
            line.append(random.randint(0, cst_grayLength-1))
        randomImage.append(line)
    return randomImage

def transformMatrixToVector(matrix):
    vector = []
    for i in range(cst_n):
        for j in range(cst_n):
            vector.append(matrix[i][j])
    return vector

def transformVectorToMatrix(vector):
    matrix = []
    for i in range(cst_n):
        matrix.append([])
        for j in range(cst_n):
            matrix[i].append(vector[i*cst_n + j])
    return matrix

def leastSignificantBitOfNumber(number):
    return number%2

def leastSignificantBitForVector(vector):
    result = []
    for i in range(len(vector)):
        result.append(leastSignificantBitOfNumber(vector[i]))
    return result

def createX(image):
    return leastSignificantBitForVector(transformMatrixToVector(image))

def createSubH():
    subH = [[1, 0], [1, 1]]
    return subH

def createH(subH):
    return

def createRandomM():
    m = []
    for i in range(cst_n*cst_alpha):
        m.append(random.randint(0,1))
    return m

def codeTrellis(H, x):
    return

def createStegoImage(image, y):
    return

def showResult(image, stegoImage):
    return

## Initialise Data

image = createRandomImage()
subH = createSubH()
H = createH(subH)
m = createRandomM()

## Play

x = createX(image)
y = codeTrellis(H, x)
stegoImage = createStegoImage(image, y)
showResult(image, stegoImage)