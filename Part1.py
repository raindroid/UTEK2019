
# coding: utf-8

# In[29]:


import pprint


# In[30]:


products = {}

inputFile = open("programming2019-master/SubmissionTests/1c.in")

inputStr = inputFile.read()

inputStrList = inputStr.split('\n')

inputList = []
for i in inputStrList:
    inputList.append(i.lstrip('(').rstrip(' ').rstrip(')').split(','))
    
inputListofDict = []
for i in inputList:
    # print(i)
    inputListofDict.append({'Location': (int(i[0]),int(i[1])), 'ProductNumber': int(i[2]), "Weight": float(i[3]), "Qty": 1})

#pprint.pprint(inputListofDict)


# In[31]:


def SortKey(val):
    return val['ProductNumber']

inputListofDict.sort(key = SortKey)

i = 1
while i < len(inputListofDict):
    if inputListofDict[i]["ProductNumber"] == inputListofDict[i-1]["ProductNumber"]:
        del inputListofDict[i]
        inputListofDict[i-1]["Qty"] += 1
    else:
        i += 1
        
pprint.pprint(inputListofDict)


# In[36]:


outputFile = open("outputFile.txt", "w")
for i in inputListofDict:
    outputFile.write("Product Number: {}; Weight: {}; Qty: {}; Location: {}\n".format(i["ProductNumber"], i["Weight"], i["Qty"], i["Location"]))

outputFile.close()

