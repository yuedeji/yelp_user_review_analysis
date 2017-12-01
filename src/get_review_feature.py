#! encode = utf-8
import os
import os.path
import json
import csv


def write_head(fileName):
    log = open(fileName, 'w')
    line = "label,review_id,# words,# unique words,# votes cool,# votes funny,# votes useful,user_id"
    log.writelines(line + "\n")
    log.close()

def write_to_csv(result, output_file):
#    write_head(output_file)

    head = "label,review_id,stars,# words,# unique words,# votes cool,# votes funny,# votes useful,since,elite,friends,fans,rating,compli_type,compli_num,vote_type,vote_num,num_review,num_reviewed_business,date_first,date_last,date_avg,num_avg_review,var_review_date,avg_review_star,frequent_star,range_star,var_star,avg_star_subtract_busi_star,avg_words_of_review,cc_size,cc_avg_star,cc_var_star,cc_avg_date,cc_avg_elite"
    with open(output_file, "w") as csvfile:
        csv_write = csv.writer(csvfile)
        csv_write.writerow(head.split(','))
        for line in result:
            csv_write.writerow(line)

    print "result written to", output_file

def analyze_line(line, user_feature):
    user_id = line['user_id']
    review_id = line['review_id']

    result = []
    vote_funny = int(line['funny'])
    vote_useful = int(line['useful'])
    vote_cool = int(line['cool'])
    vote_num = vote_funny + vote_useful + vote_cool
    label = -1
    if vote_num > 0:
        label = 1

    words = line['text'].split()
    word_set = set()
    for one in words:
        if one not in word_set:
            word_set.add(one)

    if user_id in user_feature:
        result = [label, review_id, line['stars'], len(words), len(word_set), vote_funny, vote_useful, vote_cool] + user_feature[user_id]
    return result


def analyze_line_date(line, user_feature, result_year):
    user_id = line['user_id']
    review_id = line['review_id']

    result = []
    vote_funny = int(line['funny'])
    vote_useful = int(line['useful'])
    vote_cool = int(line['cool'])
    vote_num = vote_funny + vote_useful + vote_cool
    label = -1
    if vote_num > 0:
        label = 1

    words = line['text'].split()
    word_set = set()
    for one in words:
        if one not in word_set:
            word_set.add(one)

    if user_id in user_feature:
        result = [label, review_id, line['stars'], len(words), len(word_set), vote_funny, vote_useful, vote_cool] + user_feature[user_id]

        year = line['date'].split('-')[0]

        if year not in result_year:
            result_year[year] = [result]
        else:
            result_year[year].append(result)

    return result

#def get_review_feature(file_path, user_feature):
#
#    print file_path + '\n'
#    i = 0
#
#    result = []
#    result_year = {}
#    with open(file_path) as data_file:
#        for line in data_file:
#            data = json.loads(line)
#            #result_line = (analyze_line(data, user_feature))
#            result_line = (analyze_line_date(data, user_feature, result_year))
#            if len(result_line) > 0:
#                result.append(result_line)
#            i += 1
#            if i % 100000 == 0:
#                print i
#
#    print result_year
#    return result

def get_review_feature_year(file_path, user_feature):

    print file_path + '\n'
    i = 0

    result_year = {}
    with open(file_path) as data_file:
        for line in data_file:
            data = json.loads(line)
            #result_line = (analyze_line(data, user_feature))
            analyze_line_date(data, user_feature, result_year)
            i += 1
            if i % 100000 == 0:
                print i

    print len(result_year)
    return result_year

def get_user_feature(file_user_feature):

    user_feature = {}
    is_head = True
    with open(file_user_feature, "r") as csv_file:
        for line in csv.reader(csv_file):
            if is_head:
                is_head = False
                continue
            user_feature[line[1]] = line[2:]

    return user_feature


if __name__ == "__main__":

    file_review = "/home/yuedeji/dataset/yelp/dataset/review.json"

    file_user_feature = "/home/yuedeji/dataset/yelp/feature_combine.csv"

    user_feature = get_user_feature(file_user_feature)

    result = get_review_feature_year(file_review, user_feature)

    output_folder = "/home/yuedeji/dataset/yelp/"

    for year in result:
        output_file = os.path.join(output_folder, "feature_review_label_" + str(year) + ".csv")
        write_to_csv(result[year], output_file)

    print "\nReview features are successfully extracted!"

