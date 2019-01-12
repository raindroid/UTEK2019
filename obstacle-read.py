
import pprint
import re
from collections import deque

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
   # pprint.pprint(part2_path())
   inputFile = open("programming2019-master/3a.in")
   inputStr = inputFile.readline()
   command = re.findall('[0-9]', inputStr)
   print(read(command[0], command[1], command[2]))


