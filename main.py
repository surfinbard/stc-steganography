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

randomImg = True
path = "Path to complete"

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

def fillH(H, subH):
    matrixHeight = len(H)
    matrixWidth = len(H[0])
    subHeight = len(subH)
    subWidth = len(subH[0])
    # all height indexes will be used but not all width indexes, hence j on the outside (easier)
    for i in range(matrixHeight):
        for j in range(matrixWidth):
            if ((i == j / subWidth) & (j % subWidth == 0)):
                # placing subH inside H, item by item
                for x in range(subHeight):
                    for y in range(subWidth):
                        if((i + x < matrixHeight) & (j + y < matrixWidth)):
                            H[i + x][j + y] = subH[x][y]

def createH(subH):
    H = generateH()
    fillH(H, subH)
    return H

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

# Converts pixels to LSB vector
def pixelsToLSBVector(pixels):
    return LSBVector(matrixToVector(pixels))

# Returns optimal y after trellis construction
def syndromeTrellis(H, subH, x):


    return

def getColumnForTrellis(H):
    return np.transpose(H)

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
                newState = state ^ getColumnForTrellis(H)
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
def getStegoPixels(pixels, x, y):
    stegoPixels = []
    differenceVector = []

    for i in range(len(x)):
        differenceVector.append(y[i] - x[i])
    differenceMatrix = vectorToMatrix(differenceVector)

    for i in range(len(pixels)):
        stegoPixels.append([])
        for j in range(len(pixels[0])):
            stegoPixels[i].append(pixels[i][j] + differenceMatrix[i][j])
    return stegoPixels

def totalDistortionFromMatrix(pixels, stegoPixels):
    sum = 0
    for i in range(len(pixels)):
        for j in range(len(pixels[0])):
            if (pixels[i][j] != stegoPixels[i][j]):
                sum += 1
    return sum

def totalDistortionFromVector(x, y):
    sum = 0
    for i in range(len(x)):
        if (x[i] != y[i]):
            sum += 1
    return sum

# Outputs visual representation of the final result
def showResult(image, stegoImage):
    showImage(image)
    showImage(stegoImage)
    return

### Ugly trellis

import math

def uglyTrellis(H, subH, x, message):
    trellisMatrix = []
    for i in range(subHeight ** 2):
        trellisMatrix.append([])
        for j in range(len(H[0]) + 1):
            trellisMatrix[i].append(None)
    forwardTrellis(H, subH, x, message, trellisMatrix)
    y = backwardTrellis(trellisMatrix)
    return y

def forwardTrellis(H, subH, x, message, trellisMatrix):
    trellisMatrix[0][0] = [None, None, 0, True] # [previousState, bitValue, weightSum, continuePath]
    for j in range(len(H[0])):
        columnH = getColumnH(j)
        forwardTrellisStep(trellisMatrix, H, subH, x, message, j, columnH)
        if(((j+1)%subWidth == 0) | (j == len(H[0])-1)):
            endBlock(trellisMatrix, H, subH, x, message, j+1)
    return trellisMatrix

def getColumnH(j):
    columnH = []
    for i in range(subHeight):
        if(j//subWidth + i < len(H)):
            columnH.append(H[j//subWidth + i][j])
        else:
            columnH.append(0)
    return columnH


def forwardTrellisStep(trellisMatrix, H, currentSubH, x, message, j, columnH):
    yProduct = []
    yProduct.append(bitToNumber(np.dot(columnH, 0)))
    yProduct.append(bitToNumber(np.dot(columnH, 1)))
    weight = [abs(x[j] - 0), abs(x[j] - 1)]
    for i in range(subHeight ** 2):
        if(trellisMatrix[i][j] != None):
            if(trellisMatrix[i][j][3]):
                for k in range(2):
                    if(trellisMatrix[i ^ yProduct[k]][j+1] != None):
                        if(trellisMatrix[i ^ yProduct[k]][j+1][2] > trellisMatrix[i][j][2] + weight[k]):
                            trellisMatrix[i ^ yProduct[k]][j+1] = [i, k, trellisMatrix[i][j][2] + weight[k], True]
                    else:
                        trellisMatrix[i ^ yProduct[k]][j+1] = [i, k, trellisMatrix[i][j][2] + weight[k], True]
    return trellisMatrix

def endBlock(trellisMatrix, H, subH, x, message, j):
    for i in range(subHeight ** 2):
        if(trellisMatrix[i][j] != None):
            if(j//subWidth - 1 < len(message)):
                if(i%2 != message[j//subWidth - 1]):
                    trellisMatrix[i][j][3] = False
                else:
                    trellisMatrix[i//2][j] = trellisMatrix[i][j]
                    if(i//2 != i):
                        trellisMatrix[i][j] = None
    return

def backwardTrellis(trellisMatrix):
    pathEnds = []
    for i in range(subHeight ** 2):
        if(trellisMatrix[i][len(H[0])] != None):
            if(trellisMatrix[i][len(H[0])][3]):
                pathEnds.append(i)
    optimalPathEnd = pathEnds[0]
    for i in pathEnds:
        if(trellisMatrix[optimalPathEnd][len(H[0])][2] > trellisMatrix[i][len(H[0])][2]):
            optimalPathEnd = i
    y = []
    previousState = optimalPathEnd
    for j in range(len(H[0]), 0, -1):
        y.append(trellisMatrix[previousState][j][1])
        previousState = trellisMatrix[previousState][j][0]
    y.reverse()
    return y

def bitToNumber(bitList):
    sum = 0
    for i in range(len(bitList)):
        sum += bitList[i] * (2 ** i)
    return sum

def testUglyTrellis(H, subH, x, message):
    y = uglyTrellis(H, subH, x, message)
    print("x =", x)
    print("y =", y)
    replaceNoneByZero(H)
    print("H =", H)
    print("message =", message)
    print("H*y =", np.mod(np.dot(H, y), 2))
    return

def replaceNoneByZero(H):
    for i in range(len(H)):
        for j in range(len(H[0])):
            if(H[i][j] == None):
                H[i][j] = 0
    return

### end ugly trellis

## Image

from PIL import Image

def openImage(path):
    return Image.open(path).convert('L')

def getPixels(image):
    return np.asarray(image)

def showImage(image):
    image.show()

def createImageFromPixels(pixels):
    return Image.fromarray(pixels, 'L')

def generateRandomImg():
    pixels = np.random.randint(0, pixelRange, (edgeSize, edgeSize), "uint8")
    return Image.fromarray(pixels)

## Best H seeker

def foundBestH():
    return

def generateRandomSubH(subHeight, subWidth):
    subH = np.random.randint(0, 2, (subHeight, subWidth), "uint8")
    if(not np.isin(1, subH[0])):
        subH[0][np.random.randint(subWidth)] = 1
    if(not np.isin(1, subH[subHeight - 1])):
        subH[subHeight - 1][np.random.randint(subWidth)] = 1
    return subH

def calculateEfficiency(pixelsNumber, alpha, distortion):
    return pixelsNumber * alpha / distortion

def generateMultipleRandomMsg(pixelsNumber, alpha, messagesNumber):
    messageLength = pixelsNumber * alpha
    messages = np.empty((messagesNumber, messageLength), 'uint8')
    for i in range(messagesNumber):
        messages[i] = generateRandomMsg()
    return messages

def getAverageEfficiency(x, H, subH, messages, edgeSize):
    efficiencies = np.zeros(iterationNumber)
    iterationNumber = len(messages)
    for i in range(iterationNumber):
        message = messages[i]
        y = uglyTrellis(H, subH, x, message)
        distortion = totalDistortionFromVector(x, y)
        efficiencies[i] = calculateEfficiency(edgeSize ** 2, alpha, distortion)
    averageEfficiency = np.mean(efficiencies)
    return averageEfficiency

if __name__ == '__main__':

    ## Initialize data
    if(not randomImg):
        image = openImage(path)
    else :
        image = generateRandomImg()
    pixels = getPixels(image)
    subH = generateSubH()
    H = generateH()
    fillH(H, subH)
    message = generateRandomMsg()

    ## Run
    x = pixelsToLSBVector(pixels)
    optimalY = syndromeTrellis(H, subH, x)
    # stegoPixels = getStegoPixels(pixels, x, optimalY)
    # stegoImage = createImageFromPixels(stegoPixels)
    # showResult(image, stegoImage)
    # testUglyTrellis(H, subH, x, message)
