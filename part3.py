
import pprint
import math
import itertools
import math
import re

def part1():
    def SortKey(val):
        return val['ProductNumber']

    # In[30]:
    products = {}
    inputFile = open("programming2019-master/2a.in")
    firstLine = inputFile.readline()
    length = int(firstLine.split(' ')[1][:-1])

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

    obstacleList = []
    for i in range(int(firstLine.split(' ')[2])):
        line = inputFile.readline().lstrip('(').rstrip(' ').rstrip(' ').rstrip(')').split(',')
        obstacleList.extend([int(line[0]), int(line[1]), int(line[2]), int(line[3])])
    return inputListofDict, obstacleList


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

def shortest_path(oldPath, pathData):
    distances = [] #debug
    for i in range(10):
        distances.append([0 for _ in range(10)])
    nodes = {}
    for i in [0] + oldPath:
        nodes[i] = {'len':200}
        for j in [0] + oldPath:
            distances[i][j] = 0 if i == j else -pathData.get((i, j))
    # distances[0][0] = 10

    visited = set()
    current = 0
    # nodes[current] = {'len':0, 'path': [0]}
    path = [0]
    while True:
        for i, node in nodes.items():
            if i in visited: continue
            if distances[current][i] + (0 if current == 0 else nodes[current]['len']) < nodes[i]['len']:
                nodes[i]['len'] = distances[current][i] + (0 if current == 0 else nodes[current]['len'])
                nodes[i]['path'] = path + [i]

        for i, node in nodes.items():
            if i not in visited:
                current = i
                break
        path.append(current)
        visited.add(current)
        if len(visited) == len(nodes): break

    return nodes[0]['path']


# def shortest(oldPath, pathData):
#     pathList =
#     for i in itertools.permutations('abcd', 4):
#         print(''.join(i))

def bag(n, m, w, v):
    res = [[0 for j in range(m + 1)] for i in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            res[i][j] = res[i - 1][j]  # 0->res[0][1]->res[1][1]
            if j >= w[i - 1] and res[i][j] < res[i - 1][j - w[i - 1]] + v[i - 1]:
                res[i][j] = res[i - 1][j - w[i - 1]] + v[i - 1]
    return res


def show(n, m, w, res):
    # print(u"maxValue: %d" % res[n][m])
    x = [False for i in range(n)]
    j = m
    for i in range(n, 0, -1):
        if res[i][j] != res[i - 1][j]:
            x[i - 1] = True
            j -= w[i - 1]
    itemList = []
    for i in range(n):
        if x[i]:
            itemList.append(i)
    return itemList

# def part2-
#     # n种物品，承重量为m，w物品的重量，v 物品的价值
#     n = 7
#     m = 100
#     w = [5,20,20,20,70,12,12]
#     v = [5,20,20,20,70,12,12]
#     res = bag(n, m, w, v)
#     #print(res)
#     itemList = show(n, m, w, res)
#     print (itemList)

test_map = []


class Node_Elem:
    def __init__(self, parent, x, y, dist):
        self.parent = parent
        self.x = x
        self.y = y
        self.dist = dist


class A_Star:
    def __init__(self, s_x, s_y, e_x, e_y, w=60, h=30):
        self.s_x = s_x
        self.s_y = s_y
        self.e_x = e_x
        self.e_y = e_y

        self.width = w
        self.height = h

        self.open = []
        self.close = []
        self.path = []

    def find_path(self):
        p = Node_Elem(None, self.s_x, self.s_y, 0.0)
        while True:
            self.extend_round(p)
            if not self.open:
                return
            idx, p = self.get_best()
            if self.is_target(p):
                self.make_path(p)
                return
            self.close.append(p)
            del self.open[idx]

    def make_path(self, p):
        while p:
            self.path.append((p.x, p.y))
            p = p.parent

    def is_target(self, i):
        return i.x == self.e_x and i.y == self.e_y

    def get_best(self):
        best = None
        bv = 1000000
        bi = -1
        for idx, i in enumerate(self.open):
            value = self.get_dist(i)
            if value < bv:
                best = i
                bv = value
                bi = idx
        return bi, best

    def get_dist(self, i):
        return i.dist + math.sqrt(
            (self.e_x - i.x) * (self.e_x - i.x)
            + (self.e_y - i.y) * (self.e_y - i.y)) * 1.2

    def extend_round(self, p):
        xs = (-1, 0, 1, -1, 1, -1, 0, 1)
        ys = (-1, -1, -1, 0, 0, 1, 1, 1)
        for x, y in zip(xs, ys):
            new_x, new_y = x + p.x, y + p.y
            if not self.is_valid_coord(new_x, new_y):
                continue
            node = Node_Elem(p, new_x, new_y, p.dist + self.get_cost(
                p.x, p.y, new_x, new_y))
            if self.node_in_close(node):
                continue
            i = self.node_in_open(node)
            if i != -1:
                if self.open[i].dist > node.dist:
                    self.open[i].parent = p
                    self.open[i].dist = node.dist
                continue
            self.open.append(node)

    def get_cost(self, x1, y1, x2, y2):
        if x1 == x2 or y1 == y2:
            return 1.0
        return 1.4

    def node_in_close(self, node):
        for i in self.close:
            if node.x == i.x and node.y == i.y:
                return True
        return False

    def node_in_open(self, node):
        for i, n in enumerate(self.open):
            if node.x == n.x and node.y == n.y:
                return i
        return -1

    def is_valid_coord(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return test_map[y][x] != '#'

    def get_searched(self):
        l = []
        for i in self.open:
            l.append((i.x, i.y))
        for i in self.close:
            l.append((i.x, i.y))
        return l


def print_test_map():
    # print (test_map)
    for line in test_map:
        print(''.join(line))


def get_start_XY():
    return get_symbol_XY('S')


def get_end_XY():
    return get_symbol_XY('E')


def get_symbol_XY(s):
    for y, line in enumerate(test_map):
        try:
            x = line.index(s)
        except:
            continue
        else:
            break
    return x, y


def mark_path(l):
    mark_symbol(l, '*')


def mark_searched(l):
    mark_symbol(l, ' ')


def mark_symbol(l, s):
    for x, y in l:
        test_map[y][x] = s


def mark_start_end(s_x, s_y, e_x, e_y):
    test_map[s_y][s_x] = 'S'
    test_map[e_y][e_x] = 'E'


def tm_to_test_map():
    for line in tm:
        test_map.append(list(line))


def find_path():
    s_x, s_y = get_start_XY()
    e_x, e_y = get_end_XY()
    a_star = A_Star(s_x, s_y, e_x, e_y)
    a_star.find_path()
    searched = a_star.get_searched()
    path = a_star.path
    mark_searched(searched)
    mark_path(path)
    # print ("path length is %d"%(len(path)))
    # print ("searched squares count is %d"%(len(searched)))
    mark_start_end(s_x, s_y, e_x, e_y)


def in_range(j, i):
    return 0 <= j and j < len(test_map) and 0 <= i and i < len(test_map[0])


def print_path():
    x, y = get_start_XY()
    path = [(x, y)]
    e_x, e_y = get_end_XY()

    # print (x,y)
    while (x, y) != (e_x, e_y):
        flag = False
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                # print ((i,j), test_map[i][j]=="*")
                if (i, j) != (x, y) and ((j, i) not in path) and in_range(j, i):
                    if test_map[j][i] == '*':
                        # print ((j,i))
                        path.append((j, i))
                        x = i
                        y = j
                        flag = True
                        break
                    if test_map[j][i] == 'E':
                        # print ((j,i))
                        path.append((j, i))
                        x = i
                        y = j
                        flag = True
                        break
            if flag: break
    return path

def setObstacle(ax,ay,bx,by):
    for i in range(ax,bx+1):
        for j in range(ay,by+2):
            withObstable[i][j] = '#'
    return withObstable

def setStartandEnd(sx,sy,ex, ey):
    copyOfList = withObstacle.copy()
    copyOfList[sx][sy] = 'S'
    copyOfList[ex][ey] = 'E'
    return copyOfList



def read(robotNum, quantity, obstacle):
    totalList = []
    file = open("programming2019-master/3a.in", 'r')
    done = 0
    count = 0
    index = 0
    while not done:
        aLine = file.readline()
        if (aLine != ''):
            if count > int(quantity):
                totalList.append(re.findall('\d+', aLine))

                index += 1
        else:
            done = 1
        count += 1
    file.close()

    return totalList


if __name__ == '__main__':
    # pprint.pprint(part1())
    raw_data, obstacleList = part1()
    path_data = part2_path(raw_data)

    tm_origin = [['#'] for i in range(102)] + [(['#'] + ['.' for i in range (100)] + ['#']) for i in range(100)] +  [['#'] for i in range(102)]

    withObstacle = tm_origin.copy()

    for i in obstacleList:
        setObstacle(i[0],i[1],i[2],i[3])



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

        n = len(productNumberList)
        w = weightList
        m = 100
        v = weightList
        res = bag(n, m, w, v)
        itemList = show(n, m, w, res)

        productList = []

        for i in itemList:
            productList.append(productNumberList[i])

        test_map = []

        for i in range(len(productList) - 1):
            copyOfList = setStartandEnd(raw_data[i]["Location"][0], raw_data[i]["Location"][1], raw_data[i+1]["Location"][0], raw_data[i+1]["Location"][1])
            tm = []
            for j in withObstacle:
                tm.append("".join(j))
            tm_to_test_map()
            find_path()
            path = print_path()
            print(path)


        tm_to_test_map()
        find_path()

        pathList = []
        for i in itemList:
            pathList.append(productNumberList[i])
        print(part2_print(pathList, raw_data), end='')
        used.extend(pathList)

        # print(shortest_path(result, path_data))
        # used.extend(result)

        # break
