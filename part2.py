
import pprint
import math

def part1():
    def SortKey(val):
        return val['ProductNumber']

    # In[30]:
    products = {}
    inputFile = open("programming2019-master/2a.in")
    length = int(inputFile.readline().split(' ')[1][:-1])
    inputStr = inputFile.read()
    inputStrList = inputStr.split('\n')
    inputList = []
    for i in inputStrList[:length]:
        inputList.append(i.lstrip('(').rstrip(')').split(','))
    inputListofDict = []
    for i in inputList:
        inputListofDict.append \
            ({'Location': (int(i[0]), int(i[1])), 'ProductNumber': int(i[2]), "Weight": float(i[3]), "Qty": 1})
    # pprint.pprint(inputListofDict)
    # In[31]:
    inputListofDict.sort(key=SortKey)
    i = 1
    while i < len(inputListofDict):
        if inputListofDict[i]["ProductNumber"] == inputListofDict[i - 1]["ProductNumber"]:
            del inputListofDict[i]
            inputListofDict[i - 1]["Qty"] += 1
        else:
            i += 1
    return inputListofDict


def part2_path(productList):
    itemMap = {}
    for productEntryA in productList:
        locationA = productEntryA.get('Location')
        productNumberA = productEntryA.get('ProductNumber')
        itemMap[(productNumberA, 0)] = \
            -max(abs(0 - locationA[0]), abs(0 - locationA[1]))
        itemMap[(0, productNumberA)] = \
            -max(abs(0 - locationA[0]), abs(0 - locationA[1]))
        for productEntryB in productList:
            locationB = productEntryB.get('Location')
            productNumberB = productEntryB.get('ProductNumber')
            itemMap[(productNumberA, productNumberB)] = \
                -max(abs(locationA[0] - locationB[0]), abs(locationA[1] - locationB[1]))
    return itemMap


def part2_bag(productNumberList, weightList, distanceDict, totalWeight):
    res = [[[] for j in range(totalWeight + 1)] for i in range(len(productNumberList) + 1)]
    # print (res)
    for i in range(len(productNumberList) + 1):
        for j in range(totalWeight + 1):
            res[i][j].append(-1)
            res[i][j].append(0)
            res[i][j].append(0)

    for j in range(totalWeight + 1):
        res[0][j][0] = 0
    for i in range(1, len(productNumberList) + 1):
        # print (i)
        for j in range(1, totalWeight + 1):
            res[i][j][0] = res[i - 1][j][0]
            if j >= weightList[i - 1] and res[i][j][0] < res[i - 1][(j - weightList[i - 1])][0] + 100 + distanceDict[
                (productNumberList[i - 1], productNumberList[i - 2])]:
                res[i][j][0] = res[i - 1][(j - weightList[i - 1])][0] + 100 + distanceDict[
                    (productNumberList[i - 1], productNumberList[i - 2])]
                if (i - 2) >= 0:
                    res[i][j][1] = productNumberList[i - 2]
                res[i][j][2] = productNumberList[i - 1]
    return res


def part2_outputBag(productNumberList, totalWeight, weightList, res):
    # print('max value:', res[len(productNumberList)][totalWeight])
    x = [False for i in range(len(productNumberList))]
    j = totalWeight
    movelist = []
    for i in range(1, len(productNumberList) + 1):
        if res[i][j][0] > res[i - 1][j][0]:
            x[i - 1] = True
            movelist.append((res[i][j][1], res[i][j][2]))
            j -= weightList[i - 1]
    # print('items chosen:')
    itemChosen = []
    for i in range(len(productNumberList)):
        if x[i]:
            # print(i, 'th item,', end='')
            itemChosen.append(productNumberList[i])
    # print('')
    return itemChosen #, movelist

def part2_print(pathList, pathDictList):
    loc = [0, 0]
    pathDict = {}
    pickList = []
    result = ['']
    entry = None
    for entry in pathDictList:
        pathDict[entry.get('ProductNumber')] = entry

    pathList.append(0)
    for des in pathList:
        entry = desEntry = {'Location': (0, 0), 'ProductNumber': 0} if des == 0 else pathDict[des]
        desLoc = desEntry.get('Location')
        part2_move(desEntry, loc, desLoc, pickList, result)

    # part2_move(entry, loc, [0, 0], pickList, result)
    return result[0]

def part2_move(desEntry, loc, desLoc, pickList, result):
    while True:
        if loc[0] == 0 and loc[1] == 0 and len(pickList) > 0:
            pickList.sort()
            # print(pickList)
            for i in pickList:
                result[0] += 'drop {}\n'.format(i)
            pickList.clear()
            break
        elif loc[0] == desLoc[0] and loc[1] == desLoc[1]:
            result[0] += 'pick {}\n'.format(desEntry.get('ProductNumber'))
            pickList.append(desEntry.get('ProductNumber'))
            if loc[0] != 0 or loc[1] != 0: break
        else:
            dirX = sign(desLoc[0] - loc[0])
            dirY = sign(desLoc[1] - loc[1])
            loc[0] += dirX
            loc[1] += dirY
            result[0] += 'move {} {}\n'.format(loc[0], loc[1])

def sign(x) :
    if x == 0:
        return 0
    else:
        return x // abs(x)



if __name__ == '__main__':
    # pprint.pprint(part1())
    raw_data = part1()
    path_data = part2_path(raw_data)
    used = []
    while True:
        productNumberList = []
        weightList = []
        for entry in raw_data:
            for _ in range(entry.get('Qty') - used.count(entry.get('ProductNumber'))):
                productNumberList.append(entry.get('ProductNumber'))
                weightList.append(math.ceil(entry.get('Weight')))
        # print(weightList)
        if len(productNumberList) == 0: break
        totalWeight = 100
        result = part2_outputBag(productNumberList, totalWeight, weightList,
                                  part2_bag(productNumberList, weightList, path_data, totalWeight))
        print(part2_print(result, raw_data), end='')
        used.extend(result)

        # break
