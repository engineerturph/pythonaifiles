file1 = open('train.csv', "r")
file2 = open('test.csv', "r")


def makeFileDict(file):
    trainArray = file.read().split('\n')
    trainDictArray = []
    elArr = []
    for i in range(len(trainArray)):
        elArr.append(trainArray[i].split(','))
    for i in range(len(trainArray) - 1):
        dict = {}
        if (i == 0):
            i = i + 1
        for j in range(12):
            dict[elArr[0][j]] = elArr[i][j]
        trainDictArray.append(dict)
    return trainDictArray


###Modeling
modelDictArray = []
