import argparse
import os,re,json,time,sys
sys.path.append(os.getcwd())
from files import porter
from math import log
import datetime
starttime =time.time()
# preprocess
# load stopwords into appropriate data structure
stopwords = set()
with open('files\stopwords.txt', 'r', encoding='utf-8') as f:
    for line in f:
        stopwords.add(line.rstrip())
# load the porter stemmer
stemmer = porter.PorterStemmer()


# the way to handle words of queries
def handle_words(query):
    # lowwer the letter
    query = query.casefold()
    # remove punctuation and special symbols
    query = re.sub('([^\u0030-\u0039\u0041-\u007a])', ' ', ''.join(query.replace('/', '')))
    # get terms (initial format)
    terms = query.split(" ")
    # get terms (after delete the stopwords and porter precess)
    new_term = []
    for term in terms:
        if term not in stopwords and term != '':
            # not none and not stopwords
            term = stemmer.stem(term)
            if term not in new_term:
                new_term.append(term)
    # delete the repeat word
    new_term = list(set(new_term))
    return new_term


# {documentID:{word1:times; word2:times...};...}
# used to store the words and their times for each document
dictionary = {}
# {documentID:length; documentID2:length;....}
# used to store the length of each document
dic_length = {}
# {word:[documentID1, documentID2,,...]; word2:[documentID1, documentID2,,...]; ...}
# used to store the document which including them for each word
dic_freq = {}
# user to store the different word in the document
words = {}
whole_num = 0
files = sorted(os.listdir('documents'))

# if there is dictionary.json file
if not os.path.exists('dictionary.json'):
    print("Please waiting several minutes for indexing, thank you very much!")
    for file in files[1:]:
        # get the whole num of files (sum of each folder)
        whole_num += len(os.listdir('documents/' + file))
        # get the folder
        son_files = sorted(os.listdir('documents/'+file))
        for file_per in son_files:
            # for each file
            with open(os.path.join("documents/"+file, file_per), "r",encoding='utf-8') as t:
                # get all the lines in the text and then combine them
                text = re.sub('([^\u0030-\u0039\u0041-\u007a])', ' ', ''.join(' '.join(t.readlines()).replace('\n',' ').strip().replace('/','')))
                # split to list
                terms = text.split(' ')
                # {word1:times; word2:times; ...}
                # store the number of occurrences of each word in each document
                docdict = {}
                # recore the length of this document
                length = 0
                # handle the word which is not stopword
                for term in terms:
                    # not none, not single letter, not '___________'
                    if term not in stopwords and term!= '' and len(term)!=1 and (term.find('__')!=False):
                        term = stemmer.stem(term)
                        term = term.casefold()
                        length += 1
                        if term not in docdict:
                            # if have doc_dic[term], add times
                            docdict[term] = 1
                        else:
                            # if not have doc_dic[term], create
                            docdict[term] += 1
                        if term not in words:
                            # if this word first come, add
                            words[term] = 1
                        if term not in dic_freq:
                            # if not calculate the word's documents, create
                            dic_freq[term] = [file_per]
                        else:
                            # if have calculated the word's documents
                            if file_per not in dic_freq[term]:
                                # if this doc haven't calculated, record this doc
                                dic_freq[term].append(file_per)
                dic_length[file_per] = length
                dictionary[file_per] = docdict
    # Additional stopwords
    # If the frequency of the word is higher than 90%, the word is judged to be a stop word
    extend_stopwords={}
    # The dictionary of words and their occurrence documents during the actual application
    # which is after removing the extra stop words
    actural_fre = {}
    # 计算stopwords，频率超过0.9就当做stopwords
    for key in dic_freq.keys():
        value_list = dic_freq[key]
        if len(value_list)/whole_num >=0.9:
            # if frequency >=0.9
            # add it to stopwords and remove it from the words
            extend_stopwords[key] = len(value_list)/whole_num
            words.pop(key)
        else:
            # else add to actural words
            actural_fre[key] = value_list
    # Store useful dictionaries
    with open("extend_stopwords.json", "w") as f:
        f.write(json.dumps(extend_stopwords,sort_keys=False, indent=4, separators=(',', ': ')))
    with open("actural_fre.json", "w") as f:
        f.write(json.dumps(actural_fre,sort_keys=False, indent=4, separators=(',', ': ')))
    with open("dictionary.json", "w") as f:
        f.write(json.dumps(dictionary,sort_keys=False, indent=4, separators=(',', ': ')))
    with open("dic_length.json", "w") as f:
        f.write(json.dumps(dic_length,sort_keys=False, indent=4, separators=(',', ': ')))
    with open("words.json", "w") as f:
        f.write(json.dumps(words,sort_keys=False, indent=4, separators=(',', ': ')))
    with open("fre_word.json", "w") as f:
        f.write(json.dumps(dic_freq,sort_keys=False, indent=4, separators=(',', ': ')))
    with open("whole.txt", "w") as f:
        f.write(str(whole_num))

# if there is not dictionary.json file
else:
    print("Please waiting seconds for loading files, thank you very much!")
    extend_stopwords={}
    actural_fre = {}
    # get dictionary from file
    with open("dic_length.json") as d_length:
        length = json.loads(d_length.read())
        dic_length = length
    with open("dictionary.json") as dices:
        docs = json.loads(dices.read())
        dictionary = docs
    with open("whole.txt") as dices:
        whole_num = int(dices.readline())
    with open("words.json") as d_words:
        wordes = json.loads(d_words.read())
        words = wordes
    with open("actural_fre.json") as fre:
        fre_w = json.loads(fre.read())
        actural_fre = fre_w
# average length of all documents
doc_average = sum(dic_length.values()) / len(dic_length)

# Calculate BM25
# assume：k=1，b=0.75
def bm25(word):
    # for each word, {documentID: bm25; ...}
    # calculate all bm25 in document for each word
    word_bm25 = {}
    # Iterate through each document in which the word appears and calculate bm25
    for doc_key in actural_fre[word]:
        # dictionary store word and time in document
        doc = dictionary[doc_key]
        # the times the word appears
        number_word = len(actural_fre[word])
        # bm25
        word_bm25[doc_key] = ((int(doc[word]) * 2) / (
                int(doc[word]) + 0.25 + (0.75 * int(dic_length[doc_key]) / doc_average))) * log(
            (whole_num - number_word + 0.5) / (number_word + 0.5), 2)
    return word_bm25


dic_result={}
result_all = ''
# if there is no bm25 file
# create
if not os.path.exists('bm25_of_words.json'):
    for word in words:
        dic_result[word] = bm25(word)
    with open("bm25_of_words.json", "w") as f:
        f.write(json.dumps(dic_result,sort_keys=False, indent=4, separators=(',', ': ')))
# get file store bm25
dic_bm25 = {}
with open("bm25_of_words.json") as f:
    dic_bm25 = json.loads(f.read())
endtime =time.time()
print('The Pre-processing time is',endtime-starttime)

parser = argparse.ArgumentParser()
parser.add_argument('--mode', "-m", default="automatic", help="Choose the mode of Bm25")
args = parser.parse_args()

if (args.mode == 'automatic'):
    auto_start = time.time()
    # if automatic
    # get queries
    q = open('files/queries.txt', 'r')
    queries = q.read().replace('/', '').split('\n')
    q.close()
    # process queries
    with open('files/result.txt', "w") as f:
        result_all = ''
        for query_txt in queries:
            # handle query
            query = handle_words(query_txt)
            # {'documentID': bmOfTerms; ...}
            # to store the bm25 score for each relevance document
            relevance_doc_bm25 = {}
            for term in query:
                # for each word in query
                if term in dic_bm25.keys():
                    # if it is in bm25 file
                    if len(relevance_doc_bm25.keys()) == 0:
                        # if there is no document in relevance document bm25
                        # init it based on the term
                        # after that, the relevance_doc_bm25 from {} change to {'documentID': bmOfThisTerm, ...}
                        relevance_doc_bm25 = dic_bm25[term].copy()
                    else:
                        for doc in dic_bm25[term].keys():
                            # # if there are documents in relevance document bm25
                            if doc not in relevance_doc_bm25.keys():
                                # but this doc is not in the dictionary
                                # add new doc to the dictionary
                                relevance_doc_bm25[doc] = dic_bm25[term][doc]
                            else:
                                # this doc is in the dictionary
                                # add the bm25 to the dictionary in this doc
                                relevance_doc_bm25[doc] += dic_bm25[term][doc]
            # get rank list based on bm25
            rank_list = sorted(relevance_doc_bm25.items(), key=lambda x: x[1], reverse=True)
            num = 0
            rank = 1
            # if the relevance is upper than 15, print the first 15
            # if there is lower than 15, print all them have
            while len(rank_list) > num and num < 15:
                result_all = str(rank_list[num][0]) + " " + str(
                    rank_list[num][1])
                f.write(str(query_txt.split(' ')[0]) + " " + str(rank) + " " + result_all + '\n')
                num += 1
                rank += 1
    auto_end = time.time()
    print('All result of the queries are in the result.py')
    print('The search time is', auto_end - auto_start)
else:
    # if interactive
    # keep the program doing if not exit
    isKeeping = True
    while isKeeping:
        print('Loading BM25 index from file, please wait.')
        query = input("Enter query:")
        search_start = time.time()
        if query == 'EXIT':
            # if user use 'EXIT', exit from the system
            print('You have exit from this system')
            isKeeping = False
        else:
            print('Results for query:', query)
            # handle query
            query = handle_words(query)
            # {'documentID': bmOfTerms; ...}
            # to store the bm25 score for each relevance document
            relevance_doc_bm25 = {}
            for term in query:
                # for each word in query
                if term in dic_bm25.keys():
                    # if it is in bm25 file
                    if len(relevance_doc_bm25.keys()) == 0:
                        # if there is no document in relevance document bm25
                        # init it based on the term
                        # after that, the relevance_doc_bm25 from {} change to {'documentID': bmOfThisTerm, ...}
                        relevance_doc_bm25 = dic_bm25[term].copy()
                    else:
                        for doc in dic_bm25[term].keys():
                            if doc not in relevance_doc_bm25.keys():
                                # but this doc is not in the dictionary
                                # add new doc to the dictionary
                                relevance_doc_bm25[doc] = dic_bm25[term][doc]
                            else:
                                # this doc is in the dictionary
                                # add the bm25 to the dictionary in this doc
                                relevance_doc_bm25[doc] += dic_bm25[term][doc]
            # get rank list based on bm25
            rank_list = sorted(relevance_doc_bm25.items(), key=lambda x: x[1], reverse=True)
            num = 0
            rank = 1
            # if the relevance is upper than 15, print the first 15
            # if there is lower than 15, print all them have
            while len(rank_list) > num and num < 15:
                result_all = str(rank_list[num][0]) + " " + str(
                    rank_list[num][1])
                print(rank, result_all)
                num += 1
                rank += 1
            search_end = time.time()
            print('The search time is',search_end-search_start)