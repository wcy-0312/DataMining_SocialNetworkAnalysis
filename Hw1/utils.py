from itertools import chain, combinations


# part 1 : create node class
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print('  ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)


# part 2 : data prepare and preprocessing
from collections import OrderedDict

def loadSimpDat(file_path):
    # simpData = [['A', 'C', 'D'], ['B', 'C', 'E'], ['A', 'B', 'C', 'E'], ['B', 'E'], ['A', 'C', 'E'], ['B', 'C', 'D']]
    # simpData = [['A', 'C', 'D'], ['B', 'C', 'E'], ['A', 'B', 'C', 'E'], ['B', 'E']]
    simpData = []
    with open(file_path) as f:
        data = f.read().splitlines()
        for tran in data:
            simpData.append(list(filter(None, tran.split(' '))))
    # print(simpData)
    return simpData


def createInitSet(dataSet):
    retDict = OrderedDict()
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict


# part 3 : create FP tree
def createTree(dataSet, minSup=1):
    headerTable = {}  # dict{item: occurrences} that (support >= minSup)
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    for k in list(headerTable.keys()):
        if headerTable[k] < minSup:
            del (headerTable[k])

    freqItemSet = set(headerTable.keys())

    if len(freqItemSet) == 0:
        return None, None

    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null Set', 1, None)  # create tree

    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:  # if item node exist, count +1
        inTree.children[items[0]].inc(count)
    else:  # if item node not exist, create node
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] is None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):
    while nodeToTest.nodeLink is not None:
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


# part 4 ：mining frequent items
def ascendTree(leafNode, prefixPath):
    if leafNode.parent is not None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode is not None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


# part 5 : recursion
def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: str(p[1]))]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)

        condPathBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPathBases, minSup)
        if myHead is not None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


def clear_output(file):
    open(file, 'w').close()


def write_output(file, content):
    with open(file, 'a') as f:
        f.write(content)
        f.write("\n")


def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))


def getSupport(testSet, itemSetList):
    count = 0
    for itemSet in itemSetList:
        if(set(testSet).issubset(itemSet)):
            count += 1
    return count


def associationRule(freqItemSet, itemSetList, minConf):
    rules = []
    for itemSet in freqItemSet:
        subsets = powerset(itemSet)
        itemSetSup = getSupport(itemSet, itemSetList)
        for s in subsets:
            confidence = float(itemSetSup / getSupport(s, itemSetList))
            if(confidence > minConf):
                rule = "{} -> {} ({})".format(set(s), set(itemSet.difference(s)), round(confidence, 2))
                print(rule)
                rules.append([set(s), set(itemSet.difference(s)), round(confidence, 2)])
                write_output("output.txt", rule)
    return rules



