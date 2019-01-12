
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
    itemMap = []
    for productEntryA in productList:
        locationA = productEntryA.get('Location')
        productNumberA = productEntryA.get('ProductNumber')
        for productEntryB in productList:
            locationB = productEntryB.get('Location')
            productNumberB = productEntryB.get('ProductNumber')
            if productNumberA != productNumberB:
                itemMap.append({'itemA': productEntryA, 'itemB' : productEntryB,
                                'dis' : max(abs(locationA[0] - locationB[0]), abs(locationA[1] - locationB[1]))})
            else:
                break
    return itemMap

if __name__ == '__main__':
    pprint.pprint(part2_path())

