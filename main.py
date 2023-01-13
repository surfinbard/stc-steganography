import random
import array as arr
import numpy as np

# size of edges of x image
edgeSize = 3
# 8bit grayscale pixel range
pixelRange = 256
# alpha = messageLength / edgeSize
alpha = 1  # 0.1
# size of the subMatrix
subHeight = 2
subWidth = 2

# todo: set .data instead of directly into array cells

# Returns empty matrix H
def generateH():
    H = []
    for i in range(edgeSize * alpha):
        H.append([])
        for j in range(edgeSize ** 2):
            H[i].append(None)
    return H

# Returns subMatrix
def generateSubH():
    subH = [[1, 0], [1, 1]]
    return subH

# Generates message
def generateRandomMsg():
    message = []
    for i in range(edgeSize * alpha):
        message.append(random.randint(0, 1))
    return message

def generateRandomImg():
    randomImage = []
    for i in range(edgeSize):
        randomImage.append([])
        for j in range(edgeSize):
            randomImage[i].append((random.randint(0, pixelRange - 1)))
    return randomImage

def fillH(H, subH):
    matrixHeight = len(H)
    matrixWidth = len(H[0])
    # all height indexes will be used but not all width indexes, hence j on the outside (easier)
    for i in range(matrixHeight):
        for j in range(matrixWidth):
            if ((i == j / subWidth) & (j % subWidth == 0)):
                # placing subH inside H, item by item
                for x in range(subWidth):
                    for y in range(subHeight):
                        if((i + x < matrixHeight) & (j + y < matrixWidth)):
                            H[i + x][j + y] = subH[x][y]

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
    # todo: check if direction is supposed to be inversed at every x bit
    transposedH = np.transpose(H)
    if index % 2 == 0:
        return transposedH[index]
    else:
        return arr.reversed(transposedH[index])

# todo: set states instead of returning ints
# 0 in, LSB out (LSB = mi)
def moveBetweenBlocks(i):
    if (i == (0 or 1)):
        return 0
    if (i == (10 or 11)):
        return 1

def moveInsideBlocks(trellis, H):
    for i in range(subWidth):
        for j in range(len(trellis[i])):
            if (node.data):
                if (not node.weight):
                    node.weight = 0
                state = bin(j)
                node = trellis[i][j]
                newState = state ^ getColumnForTrellis(i, H)
                # 1 = horizontal edge
                # 2 = different state
                nextNode1 = trellis[i+1][j]
                nextNode2 = trellis[i][int(newState)]

                node.next1 = nextNode1
                nextNode1.prev1 = node
                setWeight(nextNode1, i+1)

                node.next2 = nextNode2
                nextNode2.prev2 = node
                setWeight(nextNode2, i+1)

def removeEdge(node, prev, prevNext):
    node[prev] = None
    node[prev][prevNext] = None

def setWeight(node, index):
    if(x[index + 1] == 0):
        if(node.prev1 and node.prev2):
            node.weight = min(node.prev1.weight, node.prev2.weight + 1)
            # removing heavier edge:
            if (node.prev1.weight == node.weight):
                removeEdge(node, 'prev2', 'next2')
            if (node.prev2.weight == node.weight):
                removeEdge(node, 'prev1', 'next1')
            return
        if(node.prev1):
            node.weight = node.prev1.weight
            return
        if(node.prev2):
            node.weight = node.prev2.weight + 1
            return
    if(x[index + 1] == 1):
        if(node.prev1 and node.prev2):
            node.weight = min(node.prev1.weight + 1, node.prev2.weight)
            # removing heavier edge:
            if (node.prev1.weight == node.weight):
                removeEdge(node, 'prev2', 'next2')
            if (node.prev2.weight == node.weight):
                removeEdge(node, 'prev1', 'next1')
            return
        if(node.prev1):
            node.weight = node.prev1.weight + 1
            return
        if(node.prev2):
            node.weight = node.prev2.weight
            return

def setState():
    return

def viterbi(trellis):
    transposedTrellis = np.transpose(trellis)
    lastColumn = transposedTrellis[-1,:]
    optimalEdge = min(lastColumn)

    # walk through trellis backwards, skip bridges between blocks, node.prev1 => node.y = 0 | node.prev2 => node.y = 1 (all newfound bits appended at index 0)
    for column in range(len(trellis[0])):
        return

    return

# todo: check
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
    x = imgToLSBVector(randomImg)
    optimalY = syndromeTrellis(H, x)
    # v_stegoImage = getStegoImage(randomImg, x, optimalY)
    # showResult(randomImg, v_stegoImage)
