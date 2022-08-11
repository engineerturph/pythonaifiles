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
        attrs = innerDict['attributes']
        fare = dict.iloc[i]['Fare']
        sex = dict.iloc[i]['Sex']
        pclass = dict.iloc[i]['Pclass']
        attrs[pclass] = 1
        # if (fare < 50):
        #     attrs['poor'] = 1
        # elif (fare < 100 and fare > 50):
        #     attrs['mid'] = 1
        # elif (fare > 100):
        #     attrs['rich'] = 1
        attrs['is ' + sex] = 1

        # if (pd.notna(age)):
        #     if (age < 10 and age > 0):
        #         innerDict['attributes']['isbaby'] = 1
        #     elif (age < 15 and age > 10):
        #         innerDict['attributes']['isyoung'] = 1
        #     elif (age < 20 and age > 15):
        #         innerDict['attributes']['isyoung2'] = 1
        #     elif (age < 40 and age > 20):
        #         innerDict['attributes']['isadult'] = 1
        #     elif (age < 100 and age > 40):
        #         innerDict['attributes']['isold'] = 1
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


stepSize = 1


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
            x = attr['attributes']
            y = attr['Survived']
            ycarpiX = {}
            y2 = 0
            for attrName in x:
                y2 += w[attrName] * x[attrName]
                ycarpiX[attrName] = -1 * y * x[attrName]
            dloss = sdF(y2, y, ycarpiX, nullVector)
            for attrName in dloss:
                w[attrName] = w[attrName] - dloss[attrName] * stepSize

    print(w)
    return w


def testFunc(attrs, w):
    dogru = 0
    yanlis = 0
    for attr in attrs:
        y = attr['Survived']
        x = attr['attributes']
        y2 = 0

        for attrName in x:
            y2 += w[attrName] * x[attrName]
        if y2 > 0:
            sign = 1
        elif y2 <= 0:
            sign = -1
        if sign == y:
            dogru += 1
        else:
            yanlis += 1
    sonuc = yanlis / (dogru + yanlis)
    print(sonuc)


w = stocasticGradientDescent(dictToAttributes(trainDict), sdF)
# stocasticGradientDescent(dictToAttributes(trainDict), sdF)
testFunc(dictToAttributes(trainDict), w)
testFunc(dictToAttributes(valDict), w)
