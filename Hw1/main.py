from optparse import OptionParser
from utils import *

if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='inputFile',
                         help='CSV filename',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minSup',
                         help='Min support (float)',
                         default=0.5,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minConf',
                         help='Min confidence (float)',
                         default=0.66,
                         type='float')

    (options, args) = optparser.parse_args()
    clear_output("output.txt")

    # part 1 & part 2
    simpData = loadSimpDat(options.inputFile)  # load data
    initSet = createInitSet(simpData)
    # print(initSet)

    # part 3
    minSup = len(simpData)*options.minSup
    myFPtree, myHeaderTab = createTree(initSet, minSup)

    # part 4 & part 5
    freqItemList = []
    mineTree(myFPtree, myHeaderTab, minSup, set([]), freqItemList)
    # print("freqItemList: \n", freqItemList)
    rules = associationRule(freqItemList, simpData, options.minConf)
