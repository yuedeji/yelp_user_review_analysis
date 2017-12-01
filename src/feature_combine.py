#! encode = utf-8
import os
import os.path
import json
import csv

file_user = "feature_user.csv"
file_review = "feature_review.csv"
#file_social = "feature_social.csv"

file_output = "feature_combine.csv"

def empty_file(file_path):
    log = open(file_path, 'w')
    log.close()

def writeLog(fileName, content):
    log = open(fileName, 'a')
    log.writelines(content + "\n")
    log.close()

def write_head(file_path):

    line = "label" + ',' + "user_id" + ',' + "since" + ',' + "elite" + ',' + "friends" + ',' + "fans" + ',' + "rating" + ',' + "compli_type" + ',' + "compli_num" + ',' + "vote_type" + ',' + "vote_num"
    line += ',' + "num_review" + ',' + "num_reviewed_business" + ',' + "date_first" + ',' + "date_last" + ',' + "date_avg" + ',' + "num_avg_review" + ',' + "var_review_date" + ',' + "avg_review_star" + ',' + "frequent_star" + ',' + "range_star" + ',' + "var_star" + ',' + "avg_star_subtract_busi_star" + ',' + "avg_words_of_review"
#    line += ',' + "cc_size" + ',' + "cc_avg_star" + ',' + "cc_var_star" + ',' + "cc_avg_date" + ',' + "cc_avg_elite"
    writeLog(file_output, line)

def combine():
    combine_dict = {}

    read_user = csv.reader(open(file_user))
    i = 0
    for line in read_user:
        if i == 0:
            i += 1
            continue
        temp_list = []
        if i % 10 == 0:
            temp_list.append('0')
        else:
            temp_list.append('1')
        temp_list += line[0:1] + line[2:]
        combine_dict[line[0]] = temp_list
        i += 1
        while len(combine_dict[line[0]]) < 11:
            combine_dict[line[0]].append(str(0))


    read_review = csv.reader(open(file_review))
    i = 0
    for line in read_review:
        if i == 0:
            i += 1
            continue
        combine_dict[line[0]] += line[1:]

        while len(combine_dict[line[0]]) < 24:
            combine_dict[line[0]].append(str(0))

#    read_social = csv.reader(open(file_social))
#    i = 0
#    for line in read_social:
##        if i == 0:
##            i += 1
##            continue
#        combine_dict[line[0]] += line[1:]
#
#        while len(combine_dict[line[0]]) < 29:
#            combine_dict[line[0]].append(str(0))
#
    write_combine = csv.writer(open(file_output, 'a'))
    for key, value in combine_dict.iteritems():
#        if len(value) != 29:
#            continue
        write_combine.writerow(value)


if __name__ == "__main__":
    empty_file(file_output)
    write_head(file_output)
    combine()

    print "Features are successfully combined!\n"
