# Introduction

------

In this assignment, the implemented project consists of two parts: **search and evaluation of a small corpus**, and **search and evaluation of a large corpus**. The core idea of the project is to store computable data in advance, thus reducing the time spent by the user during retrieval.

This document will introduce the projects of the two different corpora in the following sections, mainly covering the following parts:

> * How to use
> * Development strategy
> * Generating documents
> * Experimental results
> * Challenges and learning


------
# How to use

### 1. Automatic

The user can have the project automatically retrieve the query statements in the 'queries.txt' file and save the query results to 'result.txt' by executing the following command:

```python
python search_small_corpus.py -m automatic
```

### 2. Interactive

The user can have the project query specific content and the system will output the results by executing the following command:

```python
python search_small_corpus.py -m interactive
```

### 3. Evaluation

The user evaluates the retrieval system by executing the following command and the system will output the results:

```python
python search_evaluate_corpus.py
```

# Generating documents

The core idea of the project development is mainly to perform data pre-processing, i.e., to obtain and store important data to facilitate the subsequent search process to reduce the calculation time and provide a user-friendly search experience.

#### Search

1. In the process of traversing to read files, the system will do the data processing of the text information in the file, i.e., removing special symbols, and then dividing a line of text into a list by spaces
2. Traverse the list, remove the stop words, and then calculate the frequency of each word in each document, the length of each document, and the different words in all documents
3. Wite the obtained data to json files and store them in the form of dictionaries, so that it can be obtained directly next time
4. According to the obtained data, the system will calculate the bm25 value of each word in the document in which it appears, so as to obtain user input or retrieve query files to quickly calculate the bm25 value of each document based on the bm25 of words in documents
5. Print the top 15 documents with the highest similarity according to the results


#### Evaluation

1. Precision, Recall, R-precision, P@10, MAP, bpref
2. Mainly based on formulas
3. Note that for small corpora, only documents that are not in the qrels file are considered when calculating the number of non-relevant documents in bpref, but in large corpora, the number of non-relevant documents is determined by the documents with similarity 0 in qrels

# Generating documents (After indexing)

**dictionary.json**

Stores the number of occurrences of a word per file. The format is:
```python
{{document1: {word1: num; word2: num}};...}
```

**dic_length.json**

Store the length of per document. The format is:
```python
{{document1: length};{document2: length}...}
```

**extend_stopwords.json**

Store additional stop words, i.e. words that occur more frequently than or equal to 90%. The format is:
```python
{word: percentage;...}
```

**actural_fre.json** and **fre_words**

Stores the document in which each word appears. 

*actural_fre.json* is the word and its document after the additional stop words are removed, and *fre_words.json* is the word and its document before the additional stop words are removed. The formats are:
```python
{word: [document1,document2];...}
```

**words.json**

Store all the different words that appear in the document, which is used to iterate through the words and find the word's bm25 in the occurrence of the document. The format is:
```python
{word: 1;...}
```

# Experimental results

### **Interactive Search**

**Small Corpus**

![interactive search in small corpus][1]

[Figure: interactive search in small corpus]


**Large Corpus**

In a large corpus, efficiency is important.

The efficiency in my project is **relatively low in the pre-processing process for the first time**, which is explained in the challenges section. But **the efficiency is very high in the user search process** and is the strength of the project.

![interactive search in large corpus][2]

[Figure: interactive search in large corpus]

![pre-processing for the first time][3]

[Figure: pre-processing for the first time to run the program]


### **Automatic**

**Small Corpus**

![automatic search in small corpus][4]

[Figure: automatic search in small corpus]

**Large Corpus**

As with manual, the first pre-processing takes more time, but after that it is very efficient.

![automatic search in large corpus (after the first time)][5]

[Figure: automatic search in large corpus (after the first runing)]

### **Evaluation**

 **Small Corpus**

![evaluation in small corpus][6]

[Figure: evaluation in small corpus]

**Large Corpus**

![evaluation in large corpus][7]

[Figure: evaluation in large corpus]

# Challenges and learning

In my project, there is a problem in handling large corpora, which is that although the retrieval process is very efficient, the first execution of the project takes too long to pre-process.

In order to solve this problem, I tried various methods to improve the speed of reading large files, such as changing from read() to readlines() (I used this in final), trying multi-processing and multi-threading, using mmap and linecache libraries, but has no significant improvement

I will try again to further improve the speed of file preprocessing in the next learning process.


  [1]: http://m.qpic.cn/psc?/V53zHF0S0J9eia1GNvqV1ewJQ64HezyA/ruAMsa53pVQWN7FLK88i5kSSsFMx.OxJcTcn.wM84PSTrTrlm1RX6ZkpJ8fwXyo4YOhvPeJTn*0jPnRspFp.UB7mzIIoxHhOcL8zHS5sKPA!/b&bo=5APlAQAAAAADByE!&rf=viewer_4
  [2]: http://m.qpic.cn/psc?/V53zHF0S0J9eia1GNvqV1ewJQ64HezyA/ruAMsa53pVQWN7FLK88i5pV.5x5rvuVtivndz1y5VAAt096PJELoHsxRkzHTv3NTFE0HEm8b0o3XFEmPeyVrUDO.w5yuiKCIOav9MFPjreU!/b&bo=egMiAgAAAAADB3s!&rf=viewer_4
  [3]: http://m.qpic.cn/psc?/V53zHF0S0J9eia1GNvqV1ewJQ64HezyA/ruAMsa53pVQWN7FLK88i5m18K8DEgQH52sxPSv5bvtHZUIJIDEGFaBHWGGI2eBnlYo83pK6a36HBN9UZmzgVPfhA32p0Aog3zxALtDGgCj4!/b&bo=gwNZAAAAAAADF.s!&rf=viewer_4
  [4]: http://m.qpic.cn/psc?/V53zHF0S0J9eia1GNvqV1ewJQ64HezyA/ruAMsa53pVQWN7FLK88i5v.c4S61bhzcfrbUurTqb16O5oDdyXjkiquVc47B4jRoXTok96ItMt0Nx0hFuCi6ed3rKEtEWNubdOqi6fE204I!/b&bo=kAM0AAAAAAADF5U!&rf=viewer_4
  [5]: http://m.qpic.cn/psc?/V53zHF0S0J9eia1GNvqV1ewJQ64HezyA/ruAMsa53pVQWN7FLK88i5keSjzwi54wbODBR5qFUy.4PUeppu*XnH5PP.sJJ4uYjpihrfUQX57i7Rn9uePkeTfAeRsNm.Rr6BzL4ZzW51jc!/b&bo=dQNvAAAAAAADBzs!&rf=viewer_4
  [6]: http://m.qpic.cn/psc?/V53zHF0S0J9eia1GNvqV1ewJQ64HezyA/ruAMsa53pVQWN7FLK88i5ig2gsggSUq*2*3QruAe.hcsTyopC7bByT450khXtjDTDGaKtjdVLYohU.ZWv7xP28pgx8AStbF9bpNoJ.OI*Sc!/b&bo=fwO1AAAAAAADB.s!&rf=viewer_4
  [7]: http://m.qpic.cn/psc?/V53zHF0S0J9eia1GNvqV1ewJQ64HezyA/ruAMsa53pVQWN7FLK88i5m18K8DEgQH52sxPSv5bvtExoKE8if0T9QNEWJGNmCp.D..q3G2IfpAC8b6X7vTi6CMtSUt3*zAbb*1TATYFFO4!/b&bo=FwPGAAAAAAADF.A!&rf=viewer_4