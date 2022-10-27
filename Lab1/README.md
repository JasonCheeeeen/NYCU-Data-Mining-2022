# Data Mining Lab1 Report

## Run Code Command
```
# transform .data to .csv
python3 data2csv.py [data name].data 

# run apriori
python3 apriori_fixed -f [data name].csv -s [minimum support]

# run fp-growth
python3 fpgrowth_revised -f [data name].csv -s [minimum support]
```

## STEP II

### Modification Of Code In Task I And Task II

#### Task I

##### (A) Find Frequency Itemsets
- No change of code, just modify the output format due to make the output from large to small by ***Support***

    ![](https://imgur.com/f5U2hlJ.png)

##### (B) The Number Of Candidates Generated Before And After Pruning

- Modify returnItemWithSupport Function

    ![](https://imgur.com/6KmFmrq.png)
    
    - Add new data structure _notfreqset = set() to store not frequency itemset to be used for pruning function after.

- Add Pruning Function
    
    ![](https://imgur.com/qN0S7hd.png)
    
    - beforeprunset : The set of Itemset before Pruning
      ex: A = { (1,2,3), {2,3,4}, {3,4,5} ... }
    - lowfreqset : The set of Itemset which not frequency
      ex: B = { (1,2) ... }
    - afterprunset : output of beforeprunset which itemset are not union of lowfreqset.
      ex: C = { (2,3,4), (3,4,5) ... }
    - Algorithm: Suppose ***a in A*** and ***b in B***, since ***b*** is ***not*** the frequency itemset, so by the pruning algorithm, if ***b*** is the ***subset*** of ***a***, ***a must not a frequency itemset***, then ***a*** will not be included in ***afterprunset***.
      
- Use Pruning Function After Union And Before Next returnItemWithSupport(Next Iteration Of Apriori)

    ![](https://imgur.com/rwihkok.png)
    
- Screenshot Of The Computation Time
It will show the computation time of partII task I & II in the end of this chapter.

#### Task II

-  Add closed_frequency_items Function
    
    ![](https://imgur.com/ILchqjw.png)
     
    - CFI is the list which will store all the closed frequency itemsets. Since we have computed the all frequency itemsets which stored in ***largeSet*** which data structure is ***dict()*** like ***largeSet = { 1:[ ], 2:[ ], 3:[ ]... }***, we can examine an itemset is a closed frequency itemset between the i & i+1 which means ***length of largeSet[i+1]'s itemset - length of largeSet[i]'s itemset equal to 1***. 
    - For example: A = { {1,2}, {2,3}... } and B = { {1,2,3}, {3,4,5}... }, after check each item between ***a in A*** & ***b in B***. If ***a*** is subset of ***b*** and ***support of a equal to support of b***, then a is not the closeed frequency itemset, otherwise it is the closed frequency itemset. In addition, there is a ***case of i == _len***, the items in largeSet[i] are all the longest frequency items, then all of them must are closed frequency itemset.

- Screenshot Of The Computation Time
It will show the computation time of partII task I & II in the end of this chapter.

### Restrictions Of Code In Task I And Task II

In fact, I tried this code on datasetC for minSupport equal to 0.001.
Though it cost about ***36000 seconds (about 10 hours)***, it also output the correct result.
Hence, I think this code's scalability is great ! ***(Just I think ...)***

### Problems Encounted In Task I And Task II

Same as above of restriction, though it can output the correct result, but it ***cost a lot of time !!!***

### Discover Of Task II
Originally, I think if use closed frequency itemset will cost lots of time, but i tried many example to test, it only increase little time of no using. So i think this happen in the original data is almost little, and cause running time is almost same as no use.

### Screenshot Of The Computation Time Of Part II

#### datasetA.csv - 5%, 7.5% and 10%

![](https://imgur.com/Ftfhwqk.png)

#### datasetB.csv - 2.5%, 5% and 7.5%

![](https://imgur.com/rsIOEd1.png)

#### datasetC.csv - 2.5%, 5% and 7.5%

![](https://imgur.com/zVwVKPH.png)

## STEP III (BASED ON FP-GROWTH AND REVISED, NOT CANDIDATE BASED)

***NO REFERENCE FROM OPEN SOURCE, All CODE WRITTEN BY MYSELF WITHOUT OPTION PARSER (BY 助教 感謝助教讓我學到一招)***

### Code And Algorithm (Code Below will Step By Step)

-  GetFrequencyItemsets(data_iter, mins)

    ![](https://imgur.com/s4OvyPN.png)
    
    - This function first will cover all transactions in ***TransactionlistFZ***, and ***SingleDict*** is the ***dict()*** to record the frequency of each item. After, ***FreqSingleList*** will make the ***list*** to transform the ***SingleDict's items*** to list from their support with high to low.
    - The last part will modify each transaction with ***removing*** the item which in each transaction is ***not the frequency item*** and ***sort*** the transaction with their frequency from high to low. Finally, store the result into ***TransactionFreqItemset*** which is a ***list***.

- Construct FP-growth Tree (Used by class)

    ![](https://imgur.com/5S9ILMw.png)
    
    ![](https://imgur.com/TOzfyPm.png)
    
    - The class initial value has four parts, self.val is the name of item, self.count is appear times of item, self.child is the child root of item and self.subset is the total parent root of item.
    - ***parseTree*** function has ***three*** parameters, ***_TransList*** is the ***list*** which items in list has ***two*** value, ***first is the value of item*** and ***second is the value of frequency in total transaction***. ***_index*** is used to specify the ***current item*** in ***_TransList*** and ***_times*** is equal to ***1*** (each time plus one). It will construct tree from root to leaf, if ***current root.child*** has child which ***.val*** equal to ***_TransList[_index][0]*** which is the item value, then the ***count of child will increase 1 (specify it appeared before)***. Finally, use ***recursion*** continually to construct tree. This Algorithm is based on ***FP-growth algorithm***.
    - ***checkTree*** just used to check the tree is constructed correctly or not by using ***recursion*** of ***VLR***.

- Initial Some Data Structure
    
    ![](https://imgur.com/hJGFLCt.png)
    
    - ***FinalFreqItemSet*** will cover the ***total*** frequency itemsets.
    - ***SingleCandidate*** will cover the ***total probable subset*** and subset's appear ***times***.
    - ***SingleCandidateTime*** will cover the ***total single item appear times*** in ***total probable subset***.

- GetCandSubset(root, SingleCandidate, SingleCandidateTime)

    ![](https://imgur.com/rvZKLPL.png)
    - It will compute ***single item's times*** to store in the ***FinalFreqItemSet*** to be the ***frequency itemset with length 1***.
    - Store the ***probable subset and subset's appear times*** to ***SingleCandidate***
    - compute ***each single item appear times*** for ***each probable subset*** of ***each single item (which will append to the subset finally)***.
    - Finally, use ***recursion*** to parse the total ***child root*** and ***get probable subsets***.
- Remove the item in each probable subset which support is lower than minSupport

    ![](https://imgur.com/8V05DfU.png)
    - ***Remove the item*** in each probable subset which ***support is lower than minSupport*** and store to the ***SingleCandidateListFinal***.
    - This way's goal is to ***save the running time***.

- Construct each ***single item's probable subset*** and ***append single item*** to be the ***final frequency itemset***

    ![](https://imgur.com/AN1V6mN.png)
    - ItemSetTMP is used to store ***each single item's subset which has append the single item*** to be the ***final frequency itemset*** which data structure is the ***list***.
    
- In above function, there has another function called ***GetSubset***, it use ***recursion*** to ***make total subset*** by a ***single list***.

    ![](https://imgur.com/dyNmslC.png)
    - ***_Minnumber*** is the ***minimum value of the single item*** because the list which will be made to the subset are the ***total parent node*** of this single item, so the ***value of single item*** must the ***smallest***.

- Finally, Print The Final Result !

    ![](https://imgur.com/60eRAxj.png)
    
- Draw Algorithm To Understand Clearly
    - You can see it ignore the ***single frequency itemset***, because i had ***append total frequency itemset which length equal to 1*** to the ***FinalFreqItemSetList***, i just need to its probable subsets.
    
    ![](https://imgur.com/nAaZfsi.png)
    
### Screenshot Of The Computation Time Of Part III

#### datasetA.csv - 5%, 7.5% and 10%

![](https://imgur.com/6EtmLsb.png)

##### Ratio
- ***5% = 74.89%***
- ***7.5% = 90.56%***
- ***10% = 84.92%***

#### datasetB.csv - 2.5%, 5% and 7.5%

![](https://imgur.com/OeNFq7b.png)

##### Ratio
- ***2.5% = 94.02%***
- ***5% = 93.04%***
- ***7.5% = 93.46%***

#### datasetC.csv - 2.5%, 5% and 7.5%

![](https://imgur.com/xmxSzCx.png)

##### Ratio
- ***2.5% = 92.7%***
- ***5% = 91.27%***
- ***7.5% = 92.82%***

#### Bonus - datasetC.csv - 0.1%
![](https://imgur.com/dbdfOze.png)

##### Ratio
- ***0.1% = 99.72***
