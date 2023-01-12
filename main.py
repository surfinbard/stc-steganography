## Constant

n = 256
grayLength = 256
alpha = 0.1
h = 4
w = 10

## Function

def createRandomImage():
    return

def transformMatrixToVector():
    return

def leastSignificantBitOfNumber(number):
    return

def leastSignificantBitForVector():
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