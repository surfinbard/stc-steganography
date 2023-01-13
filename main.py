import random
import array as arr
import numpy as np

# size of edges of cover image
edgeSize = 3  
# 8bit grayscale pixel range
pixelRange = 256
# alpha = messageLength / edgeSize
alpha = 1  # 0.1
# size of the subMatrix
subHeight = 2
subWidth = 2

# Returns empty matrix H
def generateH():
    H = []
    for i in range(edgeSize * alpha):
        H.append([])
        for j in range(edgeSize ** 2):
            H[i][j] = None
    return H

# Returns subMatrix
def generateSubH():
    subH = [[1, 0], [1, 1]]
    return subH

# Generates message
def generateRandomMsg():
    return random.randint(range(edgeSize * alpha))

def generateRandomImg():
    randomImage = []
    for i in range(edgeSize):
        for j in range(edgeSize):
            randomImage[i].append((random.randint(0, pixelRange - 1)))
    return randomImage

def fillH(H, subH):
    matrixHeight = len(H[0])
    # all height indexes will be used but not all width indexes, hence j on the outside (easier)
    for j in matrixHeight:
        for i in range(len(H)):
            if (i % subWidth == 0):
                # placing subH inside H, item by item
                for x in subWidth:
                    for y in subHeight:
                        H[i][j] = subH[x][y]

# Outputs matrix in vector format
def matrixToVector(matrix):
    vector = []
    for i in range(edgeSize):
        for j in range(edgeSize):
            vector.append(matrix[i][j])
    return vector

# Builds matrix out of vector
def vectorToMatrix(vector):
    matrix = []
    for i in range(edgeSize):
        matrix.append([])
        for j in range(edgeSize):
            matrix[i].append(vector[i * edgeSize + j])
    return matrix

# Gets LSB of binary number
def getLSB(number):
    return number % 2

# Converts vector of binary numbers to LSBs only
def LSBVector(vector):
    result = []
    for i in range(len(vector)):
        result.append(getLSB(vector[i]))
    return result

# Converts image to LSB vector
def imgToLSBVector(image):
    return LSBVector(matrixToVector(image))

# Returns optimal y after trellis construction
def syndromeTrellis(H, subH, x):
    return

def getColumnForTrellis(index, H):
    transposedH = np.transpose(H)
    if index % 2 == 0:
        return transposedH[index]
    else:
        return arr.reversed(transposedH[index])

def moveBetweenBlocks(i):
    if (i == (0 or 1)):
        return 0
    if (i == (10 or 11)):
        return 1

def moveInsideBlocks(trellis, H):
    for i in range(subWidth):
        for j in range(len(trellis[i])):
            if (node.data):  
                state = bin(j)    
                node = trellis[i][j]
                nextNode1 = trellis[i+1][j]
                
                node.next1 = nextNode1
                nextNode1.prev1 = node

                node.next2 = state ^ getColumnForTrellis(i, H)

def getWeight(anything):
    return

def viterbi(trellis):
    return

def getStegoImage(image, x, y):
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

def totalDistortion(image, stegoImage):
    sum = 0
    for i in range(len(image)):
        for j in range(image[j]):
            if (image[i][j] != stegoImage[i][j]):
                sum += 1
    return sum

# Outputs visual representation of the final result
def showResult(image, stegoImage):
    return


if __name__ == '__main__':

    ## Initialize data
    randomImg = generateRandomImg()
    subH = generateSubH()
    H = generateH()
    fillH(H, subH)
    message = generateRandomMsg()

    ## Run
    cover = imgToLSBVector(randomImg)
    optimalY = syndromeTrellis(H, cover)
    # v_stegoImage = getStegoImage(randomImg, cover, optimalY)
    # showResult(randomImg, v_stegoImage)
