def bag(productNumberList, weightList, distanceDict, totalWeight):
    res=[[[] for j in range(totalWeight+1)] for i in range(len(productNumberList)+1)]
    #print (res)
    for i in range(len(productNumberList)+1):
        for j in range(totalWeight+1):
            res[i][j].append(-1)
            res[i][j].append(0)
            res[i][j].append(0)

    for j in range(totalWeight+1):
        res[0][j][0]=0                 
    for i in range(1,len(productNumberList)+1):
        #print (i)
        for j in range(1,totalWeight+1):
            res[i][j][0] = res[i-1][j][0]
            if j>=weightList[i-1] and res[i][j][0]<res[i-1][(j-weightList[i-1])][0] + 100 + distanceDict[(productNumberList[i-1],productNumberList[i-2])]:
                res[i][j][0]=res[i-1][(j-weightList[i-1])][0] + 100 + distanceDict[(productNumberList[i-1],productNumberList[i-2])]
                if (i-2)>= 0:
                    res[i][j][1] = productNumberList[i-2]
                res[i][j][2] = productNumberList[i-1]
    return res
    

def outputBag(productNumberList,totalWeight,weightList,res):
    print('max value:',res[len(productNumberList)][totalWeight])
    x=[False for i in range(len(productNumberList))]
    j=totalWeight
    movelist = []
    for i in range(1,len(productNumberList)+1):
        if res[i][j][0]>res[i-1][j][0]:
            x[i-1]=True
            movelist.append((res[i][j][1],res[i][j][2]))
            j-=weightList[i-1]
    print('items chosen:')
    itemChosen = []
    for i in range(len(productNumberList)):
        if x[i]:
            print(i,'th item,',end='')
            itemChosen.append(productNumberList[i])
    print('')
    return itemChosen, movelist


# test case
'''
    productNumberList = [1,2,2,3,4,8,9]
    weightList = [5,2,2,3,79,1,5]
    totalWeight = 150
    distanceDict = {(1,2): -5, (1,3): -4, (1,4): -7, (1,8): -12, (1,9): -3,(1,1):0,
                   (2,1): -5, (2,3): -4, (2,4): -7, (2,8): -12, (2,9): -3,(2,2):0,
                   (3,2): -32, (3,1): -4, (3,4): -7, (3,8): -12, (3,9): -3,(3,3):0,
                   (4,2): -34, (4,3): -4, (4,1): -7, (4,8): -12, (4,9): -3,(4,4):0,
                   (8,2): -12, (8,3): -4, (8,4): -7, (8,1): -12, (8,9): -3,(8,8):0,
                   (9,2): -6, (9,3): -4, (9,4): -7, (9,8): -12, (9,1): -3, (9,9):0}
'''


# productNumberList:        a list containing any remaining objects' product number
# weightList:               a list containing weights of objects in the same order as productNumberList
# totalWight:               100
# distanceDict:             a distance dictionary containing distance between any  2 objects


res = bag(productNumberList, weightList, distanceDict, totalWeight)

itemChosen, movelist = outputBag(productNumberList,totalWeight,weightList,res)

print (itemChosen)
print (movelist)

