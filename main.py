## Import

import random

## Constant

# cst_n x cst_n is the size of the image
cst_n = 3 #256

# 8-bits of gray
cst_grayLength = 256

# cst_alpha = messageLength / cst_n
cst_alpha = 1 #0.1

# cst_h x cst_w is the size of the submatrix that help create the matrix H
cst_h = 4
cst_w = 10

## Function

# "matrix" refer to a list of list.
# "vector" refer to a list.

# Return matrix of size cst_n x cst_n with values being a random value beetween 0 and cst_grayLength-1
def createRandomImage():
    randomImage = []
    for i in range(cst_n):
        line = []
        for j in range(cst_n):
            line.append(random.randint(0, cst_grayLength-1))
        randomImage.append(line)
    return randomImage

# Given a matrix of size cst_n x cst_n
# Return a vector of length cst_n*cst_n that contains all the values of the matrix ordered by row and then column
def transformMatrixToVector(matrix):
    vector = []
    for i in range(cst_n):
        for j in range(cst_n):
            vector.append(matrix[i][j])
    return vector

# Given a vector of size cst_n*cst_n
# Return a matrix of size cst_n x cst_n that contains all the values of the vector. The i-th cst_n values are ranged in the i-th row.
def transformVectorToMatrix(vector):
    matrix = []
    for i in range(cst_n):
        matrix.append([])
        for j in range(cst_n):
            matrix[i].append(vector[i*cst_n + j])
    return matrix

# Given an int
# Return the value of the least significant bit of the int's binary form
def leastSignificantBitOfNumber(number):
    return number%2

# Given a vector
# Return a vector with its values being equals to the last significant bit of given vector's values
def leastSignificantBitForVector(vector):
    result = []
    for i in range(len(vector)):
        result.append(leastSignificantBitOfNumber(vector[i]))
    return result

# Given an image (matrix)
# Return the vector x
def createX(image):
    return leastSignificantBitForVector(transformMatrixToVector(image))

# Return the submatrix that help create the matrix H
def createSubH():
    subH = [[1, 0], [1, 1]]
    return subH

# Given a submatrix (matrix), a matrix and two int i, j
# Return the matrix with the submatrix place at position row i column j (the up left corner of the submatrix is at position row i column j). Ignore values that are supposed to be place out of bound of the matrix.
# Note : Has side effect on the matrix
def placeSubmatrixInMatrix(submatrix, matrix, i, j):
    h = len(submatrix)
    w = len(submatrix[0])
    H = len(matrix)
    W = len(matrix[0])
    for k in range(h):
        for l in range(w):
            if((i+k < H) & (j+l < W)):
                matrix[i+k][j+l] = submatrix[k][l]
    return matrix

# Given a submatrix (matrix)
# Return the matrix H
def createH(subH):
    w = len(subH[0])
    H = []
    for i in range(cst_n*cst_alpha):
        H.append([])
        for j in range(cst_n**2):
            H[i].append(0)

    for b in range(len(H)):
        H = placeSubmatrixInMatrix(subH, H, b, b*w)

    return H

# Return a vector of length cst_n*cst_alpha which represents a message. Its values represent bits randomly generated.
def createRandomM():
    m = []
    for i in range(cst_n*cst_alpha):
        m.append(random.randint(0,1))
    return m

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Need to be implemented !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Given [to complete]
# Return the vector y
def codeTrellis(H, x):
    return

# Given an image (matrix) and the vector x and y
# Return the stego image
def createStegoImage(image, x, y):
    stegoImage = []
    differenceVector = []
    for i in range(len(x)):
        differenceVector.append(y[i] - x[i])
    differenceMatrix = transformVectorToMatrix(differenceVector)
    for i in range(len(image)):
        stegoImage.append([])
        for j in range(len(image[0])):
            stegoImage[i].append(image[i][j] + differenceMatrix[i][j])
    return stegoImage

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Need to be implemeted !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Given an image (matrix) and his stego image (matrix)
# Return the value of the distorsion beetween those two image
def distorsion(image, stegoImage):
    return

# !!!!!!!!!!!!!!!!!!!!!!!!!!!! Need to be implemented !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Given [to complete]
# Return a visual representation of the final result
def showResult(image, stegoImage):
    return

## Initialise Data

v_image = createRandomImage()
v_subH = createSubH()
v_H = createH(v_subH)
v_m = createRandomM()

## Play

v_x = createX(v_image)
v_y = codeTrellis(v_H, v_x)
#v_stegoImage = createStegoImage(v_image, v_x, v_y)
#showResult(v_image, v_stegoImage)