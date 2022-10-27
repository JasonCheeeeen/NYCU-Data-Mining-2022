import sys
import time

from collections import defaultdict
from optparse import OptionParser

def dataFromFile(fname):
    """Function which reads from the file and yields a generator"""
    with open(fname, "r") as file_iter:
        for line in file_iter:
            line = line.strip().rstrip(",")  # Remove trailing comma
            record = frozenset(line.split(","))
            yield record

# Construct FP-growth Tree
class Tree():
    def __init__(self, _val):
        # Node Value
        self.val = _val
        # Node Count
        self.count = 1
        # Node Children, Record Tree Structure
        self.child = {}
        # Record All Parents Node Value
        self.subset = []

    # Construct Tree
    # _TransList -> Each Frequency Transaction Itemsets
    # _index To Record Currret Value Of _TransList
    def parseTree(self, _TransList, _index, _times):
        if _index >= len(_TransList):
            return
        # Current Node Exist Current Children List
        if _TransList[_index][0] in self.child:
            self.child[_TransList[_index][0]].count += _times
        else:
            _newnode = Tree(_TransList[_index][0])
            _newnode.count = _times
            # Prevent Append From The Tree Root
            if self.val != "-1":
                _newnode.subset.extend(self.subset)
                _newnode.subset.append(self.val)
            self.child[_TransList[_index][0]] = _newnode

        self.child[_TransList[_index][0]].parseTree(_TransList, _index+1, _times)

    # Check Tree Construct Successfully, Use Recursion To Achieve
    def checkTree(self):
        if len(self.child) == 0:
            return
        for item, value in self.child.items():
            print(item, value.count, value.subset)
            value.checkTree()

def GetFrequencyItemsets(data_iter, mins):
    SingleDict = defaultdict(int)
    TransactionlistFZ = list()
    for line in data_iter:
        transaction = frozenset(line)
        TransactionlistFZ.append(transaction)
        for item in line:
            SingleDict[item] += 1
    # Frequency Single Item
    FreqSingleList = list(item for item, support in SingleDict.items() if support / len(TransactionlistFZ) >= mins)
    TransactionFreqItemset = list()
    for line in TransactionlistFZ:
        TransFI = list()
        for _item in line:
            if _item in FreqSingleList:
                TransFI.append((_item, SingleDict[_item]))
        if len(TransFI) != 0:
            TransFI.sort(reverse = True, key=lambda x: x[1])
            TransactionFreqItemset.append(TransFI)
    return FreqSingleList, TransactionlistFZ, TransactionFreqItemset

# Cover The Single Frequency Item's Possible Candidate Value and Count 
def GetCandSubset(_root, _SingleCandidate, _SingleCandidateTime):
    if len(_root.child) == 0:
        return
    for item, value in _root.child.items():
        # Record Total Item's appeared times
        if item in FinalFreqItemSet.keys():
            FinalFreqItemSet[item] += value.count
        else:
            FinalFreqItemSet[item] = value.count
        # Record Each Single Item's Candidate Value And Count
        _SingleCandidate[item].append([value.subset, value.count])
        for _item in value.subset:
            if _item in _SingleCandidateTime[item].keys():
                _SingleCandidateTime[item][_item] += value.count
            else:
                _SingleCandidateTime[item][_item] = value.count
        GetCandSubset(value, _SingleCandidate, _SingleCandidateTime)

# Get Subset From A List -> Use Recursion !
def Getsubset(_SingleItemTotalSubset, _OriginalList, _CurrentList, _index, _Minnumber):
    if _index == len(_OriginalList):
        if len(_CurrentList) != 0:
            if frozenset(_CurrentList) in _SingleItemTotalSubset.keys():
                _SingleItemTotalSubset[frozenset(_CurrentList)] += _Minnumber
            else:
                _SingleItemTotalSubset[frozenset(_CurrentList)] = _Minnumber
            #_SingleItemTotalSubset[frozenset(_CurrentList)] = _Minnumber
        return
    _CurrentList.append(_OriginalList[_index])
    #_Minnumber = min(_Minnumber, _OriginalList[_index][1])
    Getsubset(_SingleItemTotalSubset, _OriginalList, _CurrentList, _index+1, _Minnumber)
    _CurrentList.pop()
    Getsubset(_SingleItemTotalSubset, _OriginalList, _CurrentList, _index+1, _Minnumber)

# Remove Candidate List Which Is not Frequency
def RemoveNotFreqiteminSubset(_SingleCandidateListFinal, _SingleCandidate, _SingleCandidateTime, _minSupport, _TransLeng):
    for item, value in _SingleCandidate.items():
        for _item in value:
            RemainList = []
            for items in _item[0]:
                if _SingleCandidateTime[item][items] >= _minSupport * _TransLeng:
                    RemainList.append(items)
            if len(RemainList) != 0:
                if frozenset(RemainList) in _SingleCandidateListFinal[item].keys():
                    _SingleCandidateListFinal[item][frozenset(RemainList)] += _item[1]
                else:
                    _SingleCandidateListFinal[item][frozenset(RemainList)] = _item[1]

# Construct Subset And Combine With Single Item
def ConstructFinalSubset(_SingleCandidateListFinal, _FinalFreqItemSetList, _TransLeng):
    # Construct Subset And Combine With Single Item
    for item, value in _SingleCandidateListFinal.items():
        # No Subset Item
        if len(value) == 0:
            continue

        # Record Total Subset And Count
        FinalFreqItemSubset = dict()
        for _items, _values in value.items():
            Getsubset(FinalFreqItemSubset, list(_items), [], 0, _values)
        _list = []
        for _item, _value in FinalFreqItemSubset.items():
            # Current Node's Value Is The Minimum Count, So It Need Modify The Subset Item's Count
            if _value < minSupport * TransLeng:
                # Record Item Which Need To Delete
                _list.append(_item)
        # Delete Items In Subset
        for _item in _list:
            del FinalFreqItemSubset[_item]

        _ItemSetTMP = []
        # Combine Subset and Single Item
        for _item, _value in FinalFreqItemSubset.items():
            if len(_item) == 0:
                continue
            _ItemSetTMP.extend(list(_item))
            _ItemSetTMP.append(item)
            _FinalFreqItemSetList.append([_ItemSetTMP, _value / _TransLeng])
            _ItemSetTMP = []

def printResults(items, fname, mins):
    """prints the generated itemsets sorted by support """
    file = open('step3_task1_{}_{:.1f}%_result1.txt'.format(fname, 100*mins),'w')
    for item, support in items:
        file.write("{:.1f}%\t{{{}}}\n".format(100*support, str(item)[1:-1]))
    file.close()
    file = open('step3_task1_{}_{:.1f}%_result2.txt'.format(fname, 100*mins),'w')
    file.write(str(len(items)))
    file.close()

if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option(
        "-f", "--inputFile", dest="input", help="filename containing csv", default='A.csv'
    )
    optparser.add_option(
        "-s",
        "--minSupport",
        dest="minS",
        help="minimum support value",
        default=0.1,
        type="float",
    )
    
    (options, args) = optparser.parse_args()

    inFile = None
    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = dataFromFile(options.input)
    else:
        print("No dataset filename specified, system with exit\n")
        sys.exit("System will exit")

    minSupport = options.minS
    filename = str(options.input)[0:str(options.input).find('.')]

    # TIME START
    start = time.time()

    # FSItem -> Frequency Single Item --- TransactionList -> Total Itemsets --- TransactionFreqItemsets -> Total Frequency Itemsets
    FSItem, TransactionList, TransactionFreqItemsets = GetFrequencyItemsets(inFile, minSupport)

    # TransactionList Length
    TransLeng = len(TransactionList)

    root = Tree("-1")
    # Construct Tree By Every Transaction List
    for line in TransactionFreqItemsets:
        root.parseTree(line, 0, 1)
    # root.checkTree()

    # Final Frequency ItemSet
    FinalFreqItemSet = {}

    # Dictionary Store Each Single Frequency Item's Candidate Items To Make Subsets
    SingleCandidate = {}
    SingleCandidateTime = {}
    SingleCandidateListFinal = {}
    # Create Space For Each Single Frequency Items
    for item in FSItem:
        SingleCandidate[item] = []
        SingleCandidateTime[item] = {}
        SingleCandidateListFinal[item] = {}

    # Get Each Single Frequency Item's Candidate Items
    GetCandSubset(root, SingleCandidate, SingleCandidateTime)

    # Remove Candidate List Which Is not Frequency
    RemoveNotFreqiteminSubset(SingleCandidateListFinal, SingleCandidate, SingleCandidateTime, minSupport, TransLeng)

    # Record The Final Total Frequency Itemsets -> List
    FinalFreqItemSetList = []

    # Push Single Frequency Item Into FinalFreqItemSetList
    for item, value in FinalFreqItemSet.items():
        tmplist = []
        tmplist.append(item)
        FinalFreqItemSetList.append([tmplist, value / TransLeng])

    # Construct Subset And Combine With Single Item
    ConstructFinalSubset(SingleCandidateListFinal, FinalFreqItemSetList, TransLeng)

    FinalFreqItemSetList.sort(reverse = True, key = lambda x:x[1])

    printResults(FinalFreqItemSetList, filename, minSupport)
    
    # TIME END
    end = time.time()

    print('Time for run step3 task1 data={} minsupport={:.1f}%'.format(filename, minSupport*100), '=', end-start, 's')