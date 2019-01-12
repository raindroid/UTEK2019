def bag(n, m, w, v):
    res = [[0 for j in range(m + 1)] for i in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            res[i][j] = res[i - 1][j]  # 0->res[0][1]->res[1][1]
            if j >= w[i - 1] and res[i][j] < res[i - 1][j - w[i - 1]] + v[i - 1]:
                res[i][j] = res[i - 1][j - w[i - 1]] + v[i - 1]
    return res


def show(n, m, w, res):
    print(u"maxValue: %d" % res[n][m])
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

if __name__ == "__main__":
    # n种物品，承重量为m，w物品的重量，v 物品的价值
    n = 7
    m = 100
    w = [5,20,20,20,70,12,12]
    v = [5,20,20,20,70,12,12]
    res = bag(n, m, w, v)
    #print(res)
    itemList = show(n, m, w, res)
    print (itemList)

