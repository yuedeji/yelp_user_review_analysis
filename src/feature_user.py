#! encode = utf-8
import os
import os.path
import json

'''yelping_since,compliments.plain,review_count,friends,compliments.cute,compliments.writer,fans,compliments.note,type,compliments.hot,compliments.cool,compliments.profile,average_stars,compliments.more,elite,name,user_id,votes.cool,compliments.list,votes.funny,compliments.photos,compliments.funny,votes.useful'''

file_user = "/home/yuedeji/dataset/yelp/dataset/user.json"

file_output = "feature_user.csv"

def writeLog(fileName, content):
    log = open(fileName, 'a')
    log.writelines(content + "\n")
    log.close()

def write_head(fileName):
    log = open(fileName, 'w')
    line = "user_id" + ',' + "virtual_id" + ',' + "since" + ',' + "elite" + ',' + "friends" + ',' + "fans" + ',' + "rating" + ',' + "compli_type" + ',' + "compli_num" + ',' + "vote_type" + ',' + "vote_num"
    log.writelines(line + "\n")
    log.close()

class user_feature:
    def __init__(self):
        self.user_id = ''
        self.virtual_id = 0
        self.since = 0
        self.elite = 0
        self.friends = 0
        self.fans = 0
        self.rating = 0
        self.compli_type = 0
        self.compli_num = 0
        self.vote_type = 0
        self.vote_num = 0
    def write_file(self):
        line = str(self.user_id) + ',' + str(self.virtual_id) + ','+ str(self.since) + ',' + str(self.elite) + ',' + str(self.friends) + ',' + str(self.fans) + ',' + str(self.rating) + ',' + str(self.compli_type) + ',' + str(self.compli_num) + ',' + str(self.vote_type) + ',' + str(self.vote_num)
        writeLog(file_output, line)

def analyze_line(line, index):
    user_one = user_feature()
    user_one.user_id = line['user_id']
    user_one.virtual_id = index
    user_one.since = line['yelping_since'].split('-')[0]
    user_one.elite = len(line['elite'])
    user_one.friends = len(line['friends'])
    user_one.fans = line['fans']
    user_one.rating = line['average_stars']
    user_one.compli_type = 0
    #user_one.compli_type = len(line['compliments'])
    user_one.vote_type = 0#len(line['votes'])


    compliment_list = ["compliment_hot", "compliment_more", "compliment_profile", "compliment_cute", "compliment_list", "compliment_note", "compliment_plain", "compliment_cool", "compliment_funny", "compliment_writer", "compliment_photos"]

# for round 8
#    for compliment in line['compliments']:
#        user_one.compli_num += line['compliments'][compliment]
#
#    for vote in line['votes']:
#        user_one.vote_num += line['votes'][vote]

    for compliment in compliment_list:
        user_one.compli_num += int(line[compliment])

    for vote in ['useful', 'funny', 'cool']:
        user_one.vote_num += line[vote]
#    print user_one.compli_num, user_one.vote_num, '\n'
#    print user_one.user_id, user_one.since, user_one.elite, user_one.friends, user_one.fans, user_one.rating, user_one.compli_type, user_one.vote_type
    user_one.write_file()

def extract_user_feature(file_path):
    print file_path + '\n'
#    fp_input = open(file_path, "r");
#    original_data = json.loads(fp_input);
    i = 0
    write_head(file_output)
    with open(file_path) as data_file:
        for line in data_file:
            data = json.loads(line)
            analyze_line(data, i)
            i += 1
#            print data['user_id']
            if i % 100000 == 0:
                print i, '\n'
#                break

if __name__ == "__main__":
    extract_user_feature(file_user)

    print "User features are successfully extracted!\n"
