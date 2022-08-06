trainFile = open('train.csv', "r")
testFile = open('test.csv', "r")


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
trainFile = makeFileDict(trainFile, 1)
###Modeling
modelDictArray = []
