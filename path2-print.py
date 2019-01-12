
import pprint

def part1():
    def SortKey(val):
        return val['ProductNumber']

    # In[30]:
    products = {}
    inputFile = open("programming2019-master/2a.in")
    inputFile.readline()
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

def sign(x) :
    if x == 0:
        return 0
    else:
        return x // abs(x)

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

if __name__ == '__main__':
    # part1()
    print(part2_print([1,2,2,2,4,4,0,3], part1()))

