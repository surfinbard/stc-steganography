## Import

import random

## Constant

cst_n = 3
cst_grayLength = 256
cst_alpha = 0.1
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
    return

def leastSignificantBitOfNumber(number):
    return

def leastSignificantBitForVector(vector):
    return

def createX(image):
    return leastSignificantBitForVector(transformMatrixToVector(image))

def createSubH():
    return

def createH(subH):
    return

def createRandomM():
    return

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