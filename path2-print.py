
import pprint

def part1():
    def SortKey(val):
        return val['ProductNumber']

    # In[30]:
    products = {}
    inputFile = open("programming2019-master/1a.in")
    inputStr = inputFile.read()
    inputStrList = inputStr.split('\n')
    inputList = []
    for i in inputStrList:
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


def part2_path():
    productList = part1()
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
            if productNumberA != productNumberB:
                itemMap[(productNumberA, productNumberB)] = \
                    -max(abs(locationA[0] - locationB[0]), abs(locationA[1] - locationB[1]))
    return itemMap

def sign(x) :
    if x == 0:
        return 0
    else:
        return x / abs(x)

def part2_print(pathList, pathDictList):
    loc = (0,0)
    pathDict = {}
    result = ''
    for entry in pathDictList:
        pathDict[entry.get('ProductNumber')] = entry
    for des in pathList:
        desEntry = pathDict[des]
        desLoc = desEntry.get('Location')
        if loc == desLoc:
            result += 'pick' + desEntry.get('ProductNumber')
        else:
            dirX = 0 if loc[0] == desLoc[0] else abs(loc[0] - desLoc[0]) /  loc[0] - desLoc[0]


if __name__ == '__main__':
    part2_print([1,2,3,4,8,9], part1())

