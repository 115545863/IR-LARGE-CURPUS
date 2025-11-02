import time

start_time = time.time()

# get the result from experts (qrels.txt)
# open the result from experts
file_qrels = open('files/qrels.txt', encoding="UTF_8")
# {queryID:[dictionaryID, dictionaryID2, ...];...}
# store the result from experts (qrels.txt)
list_qrels = {}
list_non_rel_qrels = {}
for line in file_qrels:
    text = line.replace("\n", "").split(' ')
    if (text[0] not in list_qrels.keys()) and text[3]!='0':
        # If the queryID is not already stored in the dictionary,
        # and it is relevance(>0)
        # then the value is created
        list_qrels[text[0]] = [text[2]]
    elif (text[0] in list_qrels.keys()) and text[3]!='0':
        # If the queryID is already stored in the dictionary,
        # and it is revelance(>0)
        # just add a new document to the stored list
        list_qrels[text[0]].append(text[2])
    if text[0] not in list_non_rel_qrels.keys() and text[3]== '0':
        # If the queryID is not already stored in the dictionary,
        # and it is not relevance(=0)
        # then the value is created
        list_non_rel_qrels[text[0]] = [text[2]]
    elif text[0] in list_non_rel_qrels.keys() and text[3]== '0':
        # If the queryID is already stored in the dictionary,
        # and it is not revelance(=0)
        # just add a new document to the stored list
        list_non_rel_qrels[text[0]].append(text[2])
file_qrels.close()

# get the result from system (result.txt)
# similar operatation with get result from experts
file_result = open('files/result.txt', encoding="UTF_8")
list_result = {}
for line in file_result:
    text = line.replace("\n", "").split(' ')
    if text[0] not in list_result.keys():
        list_result[text[0]] = [text[2]]
    else:
        list_result[text[0]].append(text[2])
file_result.close()

# get the same between experts and system
# {queryID:[documentID,...];...}
list_equal = {}
for queryID in list_qrels.keys():
    # take the intersection
    equal =list(set(list_result[queryID]) & set(list_qrels[queryID]))
    list_equal[queryID] = equal

# Variable initialization
precision = 0
recall = 0
pre_10 = 0
r_precision = 0
map = 0
bpref = 0
for key in list_qrels.keys():
    # precision for per query
    precision = precision + len(list_equal[key])/len(list_result[key])
    # recall for per query
    recall = recall+len(list_equal[key])/len(list_qrels[key])
    # precision@10 for per query
    pre_10 = pre_10+ len(list(set(list_result[key][:10]) & set(list_qrels[key])))/10
    # r-precision for per query
    length = len(list_qrels[key])
    if length!=0 and length<=len(list_result[key]):
        # relevant <= 15
        r_precision = r_precision+ len(list(set(list_result[key][:length]) & set(list_qrels[key])))/length
    elif length==0:
        # relevant = 0
        r_precision = r_precision + 0
    else:
        # relevant > 15
        r_precision = r_precision + len(list(set(list_result[key]) & set(list_qrels[key]))) / length
    # map for per query
    map_pre = 0
    for element in list_equal[key]:
        # for each element in equal, calculate precision
        position = list_result[key].index(element)+1
        map_pre = map_pre+ len(list(set(list_result[key][:position]) & set(list_qrels[key])))/position
    map = map+map_pre/len(list_qrels[key])
    # bpref for per query
    bpref_per = 0
    for element in list_equal[key]:
        # For each identical element
        # 1 - (number of unrelated files / number of related files)
        rele_num = len(list_qrels[key])
        # position is the (index+1)
        position = list_result[key].index(element)+1
        non_num = 0
        for doc in list_result[key][:position]:
            if doc in list_non_rel_qrels[key]:
                # get the number of non relevant documents
                non_num+=1
        if non_num<=rele_num:
            # If the number of unrelated files is less than the number of related files
            # 1 - unrelated/related
            bpref_per = bpref_per+(1-non_num/rele_num)
        else:
            # If the number of unrelated files exceeds the number of related files, take 0
            bpref_per = bpref_per+0
    bpref = bpref + bpref_per/len(list_qrels[key])

# get the evaluation
average_length = len(list_qrels.keys())
precision = precision/average_length
recall = recall/average_length
pre_10 = pre_10/average_length
r_precision = r_precision/average_length
map = map/average_length
bpref = bpref/average_length

print('Evaluation results:')
print('Precision: ',precision)
print('Recall: ',recall)
print('R-precision: ',r_precision)
print('P@10: ',pre_10)
print('MAP: ',map)
print('bpref: ',bpref)
end_time = time.time()
print('The evaluation time is,',end_time-start_time)