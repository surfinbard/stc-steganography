import random

## Constants

# cst_n x cst_n is the size of the image
cst_n = 3  # 256

# 8-bits of gray
cst_grayLength = 256

# cst_alpha = messageLength / cst_n
cst_alpha = 1  # 0.1

# size of the submatrix
cst_h = 4
cst_w = 10

## Functions

# "matrix" refers to a list of list
# "vector" refers to a list

# Returns matrix of size cst_n x cst_n with values being a random value between 0 and cst_grayLength - 1
def createRandomImage():
    randomImage = []
    for i in range(cst_n):
        line = []
        for j in range(cst_n):
            line.append(random.randint(0, cst_grayLength - 1))
        randomImage.append(line)
    return randomImage


# Returns a vector of length cst_n * cst_n that contains all the values of given matrix of size cst_n x cst_n
def matrixToVector(matrix):
    vector = []
    for i in range(cst_n):
        for j in range(cst_n):
            vector.append(matrix[i][j])
    return vector


# Returns a matrix of size cst_n x cst_n that contains all the values of vector of size cst_n * cst_n
# The i-th cst_n values are ranged in the i-th row.
def vectorToMatrix(vector):
    matrix = []
    for i in range(cst_n):
        matrix.append([])
        for j in range(cst_n):
            matrix[i].append(vector[i * cst_n + j])
    return matrix


# Returns the value of the least significant bit of a given binary number
def binaryNumberLSB(number):
    return number % 2


# Returns a vector of least significant bits of another vector
def vectorLSB(vector):
    result = []
    for i in range(len(vector)):
        result.append(binaryNumberLSB(vector[i]))
    return result


# Returns vector x of given image
def createX(image):
    return vectorLSB(matrixToVector(image))


# Returns the submatrix used to create matrix H
def createSubH():
    subH = [[1, 0], [1, 1]]
    return subH


# Returns the matrix with adequately placed submatrix
# Note : Affects matrix
def placeSubmatrixInMatrix(submatrix, matrix, i, j):
    h = len(submatrix)
    w = len(submatrix[0])
    H = len(matrix)
    W = len(matrix[0])
    for k in range(h):
        for l in range(w):
            if (i + k < H) & (j + l < W):
                matrix[i + k][j + l] = submatrix[k][l]
    return matrix


# Returns the matrix H, given submatrix
def createH(subH):
    w = len(subH[0])
    H = []
    for i in range(cst_n * cst_alpha):
        H.append([])
        for j in range(cst_n**2):
            H[i].append(0)

    for b in range(len(H)):
        H = placeSubmatrixInMatrix(subH, H, b, b * w)

    return H


# Returns a vector of length cst_n * cst_alpha, which represents a message
# Its values represent randomly generated bits
def createRandomM():
    m = []
    for i in range(cst_n * cst_alpha):
        m.append(random.randint(0, 1))
    return m


# todo
# Returns optimal y after trellis construction
def syndromeTrellis(H, subH, x):
    return


# Returns the stego image, given image matrix, vectors x and y
def createStegoImage(image, x, y):
    stegoImage = []
    differenceVector = []
    for i in range(len(x)):
        differenceVector.append(y[i] - x[i])
    differenceMatrix = vectorToMatrix(differenceVector)
    for i in range(len(image)):
        stegoImage.append([])
        for j in range(len(image[0])):
            stegoImage[i].append(image[i][j] + differenceMatrix[i][j])
    return stegoImage


# todo
# Returns distortion between image and stego image
def totalDistortion(image, stegoImage):
    return


# todo
# Returns a visual representation of the final result
def showResult(image, stegoImage):
    return


## Initialize Data

v_image = createRandomImage()
v_subH = createSubH()
v_H = createH(v_subH)
v_m = createRandomM()

## Run

v_x = createX(v_image)
v_y = syndromeTrellis(v_H, v_x)
# v_stegoImage = createStegoImage(v_image, v_x, v_y)
# showResult(v_image, v_stegoImage)
