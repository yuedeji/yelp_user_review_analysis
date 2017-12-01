# Yelp User and Review Analysis

These are the source codes and result files of our Yelp fake account detection project. There are two folders, source_code and feature_file.

1. src

    There are four python files: feature_user.py, feature_review.py, feature_social.py, feature_combine.py

    (1) feature_user.py:
        Extract the feature from Yelp user file
        Output feature_user.csv

    (2) feature_review.py:
        Extract user review features from Yelp user & review &business file
        Output feature_review.csv 

    (3) feature_Social.py:
        Normalize user_id to vertex_id, extract social graph features from user & review file
        Output feature_social.csv   
        
    (4) feature_combine.py:
        Combine the three files to feature_combine.csv

2. feature_file

    This folder includes the intermedia feature files generated by the source_code, such as feature_user.csv, feature_review.csv, feature_social.csv, feature_combine.csv.
    For the left files, scc_list.txt is the extracted scc files for Yelp friendship social graph.
    feature_combine_backup.csv is the backup file for feature_combine.csv
    feature_combine_10000.csv is the first 10000 lines of feature_combine.csv

Notes: 
These scripts are based on Yelp Dataset Challenge Round 8. Minor changes may need to for recent rounds.
