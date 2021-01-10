# Handles reading and writing of .CSV files.
# This was made into a class to better handle race conditions or I/O conflicts.
import pandas as pd
import csv
import os
import datetime

class CsvHandler:
    def __init__(self):
        if not os.path.exists("outputs"):
            os.makedirs('outputs')
        self.write_header_to_csv('outputs/output.csv', 'w')

    def write_header_to_csv(self, path, write_mode):
        header = ['UserScreenName', 'UserName', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Likes', 'Retweets',
                    'Image link', 'Tweet URL', 'Hashtags', 'Fooji link']
        with open(path, write_mode, newline='', encoding='utf-8') as f: 
            writer = csv.writer(f)
            writer.writerow(header)

    def get_last_date_from_csv(self, path):
        df = pd.read_csv(path, header=[0])
        df.columns= ['UserScreenName', 'UserName', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Likes', 'Retweets',
                    'Image link', 'Tweet URL', 'Hashtags', 'fooji_link']
        return datetime.datetime.strftime(max(pd.to_datetime(df["Timestamp"])), '%Y-%m-%dT%H:%M:%S.000Z')