#! encode = utf-8
import os
import os.path
import json

#file_review = "yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json"
#
#file_business = "yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json"

file_review = "/home/yuedeji/dataset/yelp/dataset/review.json"

file_business = "/home/yuedeji/dataset/yelp/dataset/business.json"


file_output = "feature_review.csv"

def writeLog(fileName, content):
    log = open(fileName, 'a')
    log.writelines(content + "\n")
    log.close()

def write_head(fileName):
    log = open(fileName, 'w')
    line = "user_id" + ',' + "num_review" + ',' + "num_reviewed_business" + ',' + "date_first" + ',' + "date_last" + ',' + "date_avg" + ',' + "num_avg_review" + ',' + "var_review_date" + ',' + "avg_review_star" + ',' + "frequent_star" + ',' + "range_star" + ',' + "var_star" + ',' + "avg_star_subtract_busi_star" + ',' + "avg_words_of_review"

    log.writelines(line + "\n")
    log.close()

class user_feature:
    def __init__(self):
#        self.user_id = ''
        self.num_review = 0
        self.num_reviewed_business = 0
        self.date_first = 0
        self.date_last = 0
        self.date_avg = 0
        self.num_avg_review = 0
        self.var_review_date = 0
        self.avg_review_star = 0
        self.frequent_star = 0
        self.range_star = 0
        self.var_star = 0
        self.avg_star_subtract_busi_star = 0
        self.avg_words_of_review = 0
        self.star_list = []
        self.review_date_list = []
        self.busi_list = []
    def write_file(self):
        line = str(self.user_id) + ',' + str(self.num_review) + ','+ str(self.num_reviewed_business) + ',' + str(self.date_first) + ',' + str(self.date_last) + ',' + str(self.date_avg) + ',' + str(self.num_avg_review) + ',' + str(self.var_review_date) + ',' + str(self.avg_review_star) + ',' + str(self.frequent_star) + ',' + str(self.range_star) + ',' + str(self.var_star) + ',' + str(self.avg_star_subtract_busi_star) + ',' + str(self.avg_words_of_review)
        writeLog(file_output, line)

def analyze_line(line, index, user_review):
    key = line['user_id']
    review_date = line['date'].split('-')[0]
    review_star = line['stars']
    review_words = len(line['text'].split(' '))
    busi_id = line['business_id']

    if key in user_review:
        user_review[key].review_date_list.append(review_date)
        user_review[key].star_list.append(review_star)
        user_review[key].busi_list.append(busi_id)
        user_review[key].avg_words_of_review = (user_review[key].avg_words_of_review + review_words) / 2.0
#        print 'occur before'
    else:
        temp_user = user_feature()
        temp_user.user_id = key
        temp_user.review_date_list.append(review_date)
        temp_user.star_list.append(review_star)
        temp_user.avg_words_of_review = review_words
        temp_user.busi_list.append(busi_id)
        user_review[key] = temp_user

def extract_review_feature(file_path, user_review):
    print file_path + '\n'
    i = 0
    write_head(file_output)

    with open(file_path) as data_file:
        for line in data_file:
            data = json.loads(line)
            analyze_line(data, i, user_review)
            i += 1
            if i % 100000 == 0:
                print i
#            if i > 30:
#                break
#    print user_review

def extract_business_feature(file_path, busi_star):
    print file_path + '\n'
    i = 0
    with open(file_path) as data_file:
        for line in data_file:
            data = json.loads(line)
            busi_id = data['business_id']
            star = data['stars']
            busi_star[busi_id] = star
            i += 1
            if i % 10000 == 0:
                print i
#            if i > 30:
#                break
#    print busi_star

def calc_review_feature(user_review, busi_star):
    #traverse the dict
    #print user_review
    for key, value in user_review.iteritems():
        #print key
        value.user_id = key
        value.num_review = len(value.review_date_list)
        value.num_reviewed_business = len(value.busi_list)
        value.review_date_list.sort()
        value.date_first = int(value.review_date_list[0])
        value.date_last = int(value.review_date_list[-1])

        sum_date = 0
        for one_date in value.review_date_list:
            sum_date += int(one_date)
        value.date_avg = sum_date  / value.num_review
        value.num_avg_review = value.num_review * 1.0 / (value.date_last - value.date_first + 1)

        var_date = 0
        for one_date in value.review_date_list:
            var_date += 1.0 * (int(one_date) - value.date_avg) * (int(one_date) - value.date_avg)
        value.var_review_date = var_date

#star features
        value.star_list.sort()
        value.range_star = value.star_list[-1] - value.star_list[0]
        sum_star = 0
        star_frequency = {}

        for one_star in value.star_list:
            sum_star += one_star
            if one_star not in star_frequency:
                temp_freq = 1
                star_frequency[one_star] = temp_freq
            else:
                star_frequency[one_star] += 1
        freq_star = 0
        freq_time = 0
        for star, time in star_frequency.iteritems():
            if time > freq_time:
                freq_time = time
                freq_star = star
        value.frequent_star = freq_star
        value.avg_review_star = sum_star * 1.0 / len(value.star_list)

        var_star = 0
        for one_star in value.star_list:
            var_star += 1.0 * (one_star - value.avg_review_star) * (one_star - value.avg_review_star)
        value.var_star = var_star

#avg_star_subtract_busi_star
        sum_busi_star = 0
        for busi in value.busi_list:
            sum_busi_star += busi_star[busi]
        value.avg_star_subtrac_busi_star = value.avg_review_star - sum_busi_star * 1.0 / value.num_review
#        print sum_busi_star
        value.write_file()
if __name__ == "__main__":
    user_review = {}
    busi_star = {}
    extract_review_feature(file_review, user_review)
    extract_business_feature(file_business, busi_star)
    calc_review_feature(user_review, busi_star)

    print "\nReview features are successfully extracted!"

