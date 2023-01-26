import random
import array as arr
import numpy as np

# size of edges of x image
edge_size = 3
# 8bit grayscale pixel range
pixelRange = 256
# alpha = message_length / edge_size
alpha = 1  # 0.1
# size of the subMatrix
sub_height = 2
sub_width = 2

randomImg = True
path = "Path to complete"

# todo: set .data instead of directly into array cells

# Returns empty matrix H
def generateH():
    H = []
    for i in range(edge_size * alpha):
        H.append([])
        for j in range(edge_size ** 2):
            H[i].append(None)
    return H

# Returns subMatrix
def generateSub_h():
    sub_h = [[1, 0], [1, 1]]
    return sub_h

# Generates message
def generateRandomMsg(message_length):
    message = []
    for i in range(message_length):
        message.append(random.randint(0, 1))
    return message

def fillH(H, sub_h):
    matrixHeight = len(H)
    matrixWidth = len(H[0])
    sub_height = len(sub_h)
    sub_width = len(sub_h[0])
    # all height indexes will be used but not all width indexes, hence j on the outside (easier)
    for i in range(matrixHeight):
        for j in range(matrixWidth):
            if ((i == j / sub_width) & (j % sub_width == 0)):
                # placing sub_h inside H, item by item
                for x in range(sub_height):
                    for y in range(sub_width):
                        if((i + x < matrixHeight) & (j + y < matrixWidth)):
                            H[i + x][j + y] = sub_h[x][y]

def createH(sub_h):
    H = generateH()
    fillH(H, sub_h)
    return H

# Outputs matrix in vector format
def matrixToVector(matrix):
    vector = []
    for i in range(edge_size):
        for j in range(edge_size):
            vector.append(matrix[i][j])
    return vector

# Builds matrix out of vector
def vector_to_matrix(vector):
    matrix = []
    for i in range(edge_size):
        matrix.append([])
        for j in range(edge_size):
            matrix[i].append(vector[i * edge_size + j])
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
def pixels_to_LSB(pixels):
    return LSBVector(matrixToVector(pixels))

# Returns optimal y after trellis construction
def syndromeTrellis(H, sub_h, x):


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
    for i in range(sub_width):
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
def get_stego_pixels(pixels, x, y):
    stego_pixels = []
    difference = []

    for i in range(len(x)):
        difference.append(y[i] - x[i])
    difference_matrix = vector_to_matrix(difference)

    for i in range(len(pixels)):
        stego_pixels.append([])
        for j in range(len(pixels[0])):
            stego_pixels[i].append(pixels[i][j] + difference_matrix[i][j])
    return stego_pixels

def totalDistortionFromMatrix(pixels, stego_pixels):
    sum = 0
    for i in range(len(pixels)):
        for j in range(len(pixels[0])):
            if (pixels[i][j] != stego_pixels[i][j]):
                sum += 1
    return sum

def get_distortion(x, y):
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

def ugly_trellis(H, sub_h, x, message):
    trellisMatrix = []
    for i in range(sub_height ** 2):
        trellisMatrix.append([])
        for j in range(len(H[0]) + 1):
            trellisMatrix[i].append(None)
    forwardTrellis(H, sub_h, x, message, trellisMatrix)
    y = backwardTrellis(trellisMatrix)
    return y

def forwardTrellis(H, sub_h, x, message, trellisMatrix):
    trellisMatrix[0][0] = [None, None, 0, True] # [previousState, bitValue, weightSum, continuePath]
    for j in range(len(H[0])):
        columnH = getColumnH(H, j)
        forwardTrellisStep(trellisMatrix, H, sub_h, x, message, j, columnH)
        if(((j+1)%sub_width == 0) | (j == len(H[0])-1)):
            endBlock(trellisMatrix, H, sub_h, x, message, j+1)
    return trellisMatrix

def getColumnH(H, j):
    columnH = []
    for i in range(sub_height):
        if(j//sub_width + i < len(H)):
            columnH.append(H[j//sub_width + i][j])
        else:
            columnH.append(0)
    return columnH


def forwardTrellisStep(trellisMatrix, H, currentSub_h, x, message, j, columnH):
    yProduct = []
    yProduct.append(bitToNumber(np.dot(columnH, 0)))
    yProduct.append(bitToNumber(np.dot(columnH, 1)))
    weight = [abs(x[j] - 0), abs(x[j] - 1)]
    for i in range(sub_height ** 2):
        if(trellisMatrix[i][j] != None):
            if(trellisMatrix[i][j][3]):
                for k in range(2):
                    if(trellisMatrix[i ^ yProduct[k]][j+1] != None):
                        if(trellisMatrix[i ^ yProduct[k]][j+1][2] > trellisMatrix[i][j][2] + weight[k]):
                            trellisMatrix[i ^ yProduct[k]][j+1] = [i, k, trellisMatrix[i][j][2] + weight[k], True]
                    else:
                        trellisMatrix[i ^ yProduct[k]][j+1] = [i, k, trellisMatrix[i][j][2] + weight[k], True]
    return trellisMatrix

def endBlock(trellisMatrix, H, sub_h, x, message, j):
    for i in range(sub_height ** 2):
        if(trellisMatrix[i][j] != None):
            if(j//sub_width - 1 < len(message)):
                if(i%2 != message[j//sub_width - 1]):
                    trellisMatrix[i][j][3] = False
                else:
                    trellisMatrix[i//2][j] = trellisMatrix[i][j]
                    if(i//2 != i):
                        trellisMatrix[i][j] = None
    return

def backwardTrellis(trellisMatrix):
    pathEnds = []
    for i in range(sub_height ** 2):
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

def testUgly_trellis(H, sub_h, x, message):
    y = ugly_trellis(H, sub_h, x, message)
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

def open_image(path):
    return Image.open(path).convert('L')

def get_pixels(image):
    return np.asarray(image)

def showImage(image):
    image.show()

def createImageFromPixels(pixels):
    return Image.fromarray(pixels, 'L')

def generate_random_img():
    pixels = np.random.randint(0, pixelRange, (edge_size, edge_size), "uint8")
    return Image.fromarray(pixels)

## Best H seeker

def get_optimal_sub_h(edge_size, alpha, sub_height, sub_width, iteration_number, messages_number, path = ()):
    if(path):
        image = open_image(path)
    else:
        image = generate_random_img()
    pixels = get_pixels(image)
    x = pixels_to_LSB(pixels)
    message_length = len(pixels) * alpha
    messages = get_random_msg(message_length, messages_number)
    submatrixes = np.empty((iteration_number, sub_height, sub_width), "uint8")
    avg_efficiencies = np.empty(iteration_number)
    for i in range(iteration_number):
        sub_h = get_random_sub_h(sub_height, sub_width)
        submatrixes[i] = sub_h
        H = createH(sub_h)
        avg_efficiencies[i] = get_avg_efficiency(x, H, sub_h, messages, edge_size)
    return submatrixes[np.argmax(avg_efficiencies)]

def get_random_sub_h(sub_height, sub_width):
    sub_h = np.random.randint(0, 2, (sub_height, sub_width), "uint8")
    if(not np.isin(1, sub_h[0])):
        sub_h[0][np.random.randint(sub_width)] = 1
    if(not np.isin(1, sub_h[sub_height - 1])):
        sub_h[sub_height - 1][np.random.randint(sub_width)] = 1
    return sub_h

def get_efficiency(pixels, alpha, distortion):
    return pixels * alpha / (distortion + 1)

def get_random_msg(message_length, messages_number):
    messages = np.empty((messages_number, message_length), 'uint8')
    for i in range(messages_number):
        messages[i] = generateRandomMsg(message_length)
    return messages

def get_avg_efficiency(x, H, sub_h, messages, edge_size):
    messages_number = len(messages)
    efficiencies = np.zeros(messages_number)
    for i in range(messages_number):
        message = messages[i]
        y = ugly_trellis(H, sub_h, x, message)
        distortion = get_distortion(x, y)
        efficiencies[i] = get_efficiency(edge_size ** 2, alpha, distortion)
    avg_efficiency = np.mean(efficiencies)
    return avg_efficiency

## Message

def txt_to_bin(str):
    txt_bits = []
    dico = {}
    for i in range(256):
        dico[chr(i)] = i
    w = ""
    for c in str:
        p = w + c
        if(dico.get(p) != None):
            w = p
        else:
            dico[p] = len(dico)
            txt_bits.append(dico[w])
            w = c
    txt_bits.append(dico[w])
    message = np.empty(len(txt_bits) * 12, 'uint8')
    for i in range(len(txt_bits)):
        str_bits = format(txt_bits[i], '012b')
        for j in range(len(str_bits)):
            message[i * 12 + j] = str_bits[j]
    return message

def bin_to_txt(message):
    str = ""
    dico = {}
    for i in range(256):
        dico[i] = chr(i)
    txt_bits = packed(message)
    v = txt_bits[0]
    w = dico[v]
    str += w
    for i in range(1, len(txt_bits)):
        v = txt_bits[i]
        if(dico.get(v) != None):
            entry = dico[v]
        else:
            entry = w + w[0]
        str += entry
        dico[len(dico)] = w + entry[0]
        w = entry
    return str

def packed(message):
    txt_bits = []
    for i in range(0, len(message), 12):
        txt_bits.append(int(''.join(np.array(message, '<U1')[i:i+12]), 2))
    return txt_bits

if __name__ == '__main__':

    ## Initialize data
    if(not randomImg):
        image = open_image(path)
    else :
        image = generate_random_img()
    pixels = get_pixels(image)
    sub_h = generateSub_h()
    H = generateH()
    fillH(H, sub_h)
    message = generateRandomMsg(edge_size * alpha)

    ## Run
    x = pixels_to_LSB(pixels)
    optimalY = syndromeTrellis(H, sub_h, x)
    # stego_pixels = get_stego_pixels(pixels, x, optimalY)
    # stegoImage = createImageFromPixels(stego_pixels)
    # showResult(image, stegoImage)
    # testUgly_trellis(H, sub_h, x, message)
