trainFile = open('train.csv', "r")
testFile = open('test.csv', "r")
valFile = open('validation.csv', 'r')


def makeFileDict(file, trainBool):
    trainArray = file.read().split('\n')
    trainDictArray = []
    elArr = []
    for i in range(len(trainArray)):
        elArr.append(trainArray[i].split(','))
    for i in range(len(trainArray) - 1):
        dict = {}
        if (i == 0):
            i = i + 1
        for j in range(12 if trainBool else 11):
            dict[elArr[0][j]] = elArr[i][j]
        trainDictArray.append(dict)
    return trainDictArray


testDict = makeFileDict(testFile, 0)
trainDict = makeFileDict(trainFile, 1)
valDict = makeFileDict(valFile, 1)


###Modeling
def dictToAttributes(dict):
    attributesArray = []
    for data in dict:
        innerDict = {}
        innerDict['Id'] = data['PassengerId']
        innerDict['Survived'] = data['Survived']
        innerDict['attributes'] = {}
        innerDict['attributes']['is ' + data['Sex']] = 1
        attributesArray.append(innerDict)
    return attributesArray


def printAttributes(attrs):
    for attr in attrs:
        i = 0
        for attrName in attr:
            if i < 2:
                print(str(attr[attrName]) + '/', end='')
                i = i + 1
                continue
            print(attrName + '->' + str(attr[attrName]) + '/', end="")
        print('\n')


printAttributes(dictToAttributes(trainDict))


def sF(y2, y):
    margin = y2 * y
    return 1 - margin if 1 - margin > 0 else 0


def sdF(y2, y, ycarpiX, nullVector):
    margin = y2 * y
    return ycarpiX if 1 - margin > 0 else nullVector


def stocasticGradientDescent(attrs, sF, sdF):
    w = {}
    nullVector = {}
    for attr in attrs:
        for attrName in attr['attributes']:
            w[attrName] = 0
            nullVector[attrName] = 0
    for attr in attrs:
        y = attr['Survived']
        ycarpiX = {}
        y2 = 0
        for attrName in attr['attributes']:
            y2 += w[attrName] * attr['attributes'][attrName]
            ycarpiX[attrName] = -1 * y * attr['attributes'][attrName]
