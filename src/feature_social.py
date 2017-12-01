#! encode = utf-8
import os
import os.path
import json
import operator

#file_user = "yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_user.json"

file_user = "/home/yuedeji/dataset/yelp/dataset/user.json"

# edge list
file_scc_list = "scc_list.txt"
file_id_map = "yelp_user_id_to_id.txt"
feature_social = "feature_social.csv"
file_user_id_to_id = "yelp_user_id_to_id.txt"

index = 0

class user_basic_feature:
    def __init__(self):
        self.star = 0
        self.since = 0
        self.elite = 0

class user_feature:
    def __init__(self):
        self.user_id = ''
        self.cc_size = 0
        self.avg_star = 0
        self.var_star = 0
        self.avg_date = 0
        self.avg_elite = 0
    def write_file(self):
        line = str(self.user_id) + ',' + str(self.cc_size) + ',' + str(self.avg_star) + ','+str(self.var_star) + ',' + str(self.avg_date) + ',' + str(self.avg_elite)
        writeLog(feature_social, line)

def writeLog(fileName, content):
    log = open(fileName, 'a')
    log.writelines(content + "\n")
    log.close()

def empty_file(fileName):
    log = open(fileName, 'w')
    log.close()

def extract_scc(file_path, scc_dict):
    fp = open(file_path, 'r')
    i = 0
    for line in fp:
        one = line.split()
        v_id = one[0]
        scc_id = one[1]
        if scc_id in scc_dict:
            scc_dict[scc_id].append(v_id)
        else:
            temp_list = []
            temp_list.append(v_id)
            scc_dict[scc_id] = temp_list
        i += 1
        if i % 10000 == 0:
            print i

def extract_id_to_user_id(file_path, id_dict):
    fp = open(file_path, "r")
    i = 0
    for line in fp:
        one = line.split()
        v_id = one[0]
        user_id = one[1]
        id_dict[v_id] = user_id
        i += 1
        if i % 10000 == 0:
            print i

def analyze_line(line, user_basic_dict):
    user_one = user_feature()
    user_id = line['user_id']
    user_one.star = line['average_stars']
    user_one.since = line['yelping_since'].split('-')[0]
    user_one.elite = len(line['elite'])
    user_basic_dict[user_id] = user_one

def extract_user_basic_feature(file_path, user_basic_dict):
    i = 0
    with open(file_path) as data_file:
        for line in data_file:
            data = json.loads(line)
            analyze_line(data, user_basic_dict)
            i += 1
            if i % 10000 == 0:
                print i
#    print user_basic_dict

def extract_social_feature(scc_dict, id_dict, user_basic_dict, feature_dict):
    i = 0
    user_one = user_feature()
    for key, value in scc_dict.iteritems():
#        print value
#        i += 1
#        if i > 100:
#            break
        user_one.cc_size = len(value)
        sum_star = 0
        sum_date = 0
        sum_elite = 0
        for v_id in value:
            user_id = id_dict[v_id]
            sum_star += float(user_basic_dict[user_id].star)
            sum_date += int(user_basic_dict[user_id].since)
            sum_elite += int(user_basic_dict[user_id].elite)
        user_one.avg_star = sum_star / user_one.cc_size
        user_one.avg_date = sum_date / user_one.cc_size
        user_one.avg_elite = sum_elite / user_one.cc_size
        for v_id in value:
            user_id = id_dict[v_id]
            feature_dict[user_id] = user_one
#            print user_id
#        print '\n'
#        i += 1
#        if i > 100:
#            break
def print_feature_dict(feature_dict):
    i = 0
    for key, value in feature_dict.iteritems():
#        print key, value.user_id
        i += 1
#        if i > 100:
#            break
        line = str(key) + ',' + str(value.cc_size) + ',' + str(value.avg_star) + ','+str(value.var_star) + ',' + str(value.avg_date) + ',' + str(value.avg_elite)
        writeLog(feature_social, line)

if __name__ == "__main__":
    scc_dict = {}
    id_dict = {}
    user_basic_dict = {}
    feature_dict = {}

    empty_file(feature_social)
    extract_scc(file_scc_list, scc_dict)
    extract_id_to_user_id(file_user_id_to_id, id_dict)
    extract_user_basic_feature(file_user, user_basic_dict)

    extract_social_feature(scc_dict, id_dict, user_basic_dict, feature_dict)

    print_feature_dict(feature_dict)
#    print id_dict
#
#    print scc_dict
    print "\nUser features are successfully extracted!"

