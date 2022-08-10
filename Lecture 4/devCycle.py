import pandas as pd

trainDict = pd.read_csv('train.csv')
testDict = pd.read_csv('test.csv')
valDict = pd.read_csv('validation.csv')


###Modeling
def dictToAttributes(dict):
    attributesArray = []
    for i in range(len(dict)):
        innerDict = {}

        innerDict['Id'] = dict.iloc[i]['PassengerId']
        innerDict['Survived'] = dict.iloc[i]['Survived'] if dict.iloc[i]['Survived'] == 1 else -1
        innerDict['attributes'] = {}
        innerDict['attributes']['is ' + dict.iloc[i]['Sex']] = 1
        age = dict.iloc[i]['Age']
        if (pd.notna(age)):
            if (age < 10 and age > 0):
                innerDict['attributes']['isbaby'] = 1
            elif (age < 15 and age > 10):
                innerDict['attributes']['isyoung'] = 1
            elif (age < 20 and age > 15):
                innerDict['attributes']['isyoung2'] = 1
            elif (age < 40 and age > 20):
                innerDict['attributes']['isadult'] = 1
            elif (age < 100 and age > 40):
                innerDict['attributes']['isold'] = 1
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


stepSize = 0.01


def stocasticGradientDescent(attrs, sdF):
    w = {}
    nullVector = {}
    totaldLoss = {}

    for attr in attrs:
        for attrName in attr['attributes']:
            w[attrName] = 0
            nullVector[attrName] = 0
            totaldLoss[attrName] = 0
    for i in range(1000):
        for attr in attrs:
            y = attr['Survived']
            ycarpiX = {}
            y2 = 0
            for attrName in attr['attributes']:
                y2 += w[attrName] * attr['attributes'][attrName]
                ycarpiX[attrName] = -1 * y * attr['attributes'][attrName]
            dloss = sdF(y2, y, ycarpiX, nullVector)
            for attrName in dloss:
                totaldLoss[attrName] = totaldLoss[attrName] + dloss[attrName] / 750
        for _ in attrs:
            for attrName in totaldLoss:
                w[attrName] = w[attrName] - 0.000001 * totaldLoss[attrName]
        print(w['is female'])


stocasticGradientDescent(dictToAttributes(trainDict), sdF)
