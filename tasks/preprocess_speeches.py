import csv, sys
import os, glob
import string
import pandas as pd

output_path = '/home/romina/Documents/work/speeches/outputs'
input_path = '/home/romina/Documents/work/speeches-segmented/greg-tables'


def preprocess_files():
    csv.field_size_limit(sys.maxsize)
    os.chdir(output_path)
    f = open('output.csv', 'w')
    os.chdir(input_path)
    w = csv.writer(f)
    w.writerow(['senator code', 'date', 'text'])
    translator = str.maketrans('', '', string.punctuation)
    for file in glob.glob("*.csv"):
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            file_year = int(csv_file.name.split('-')[0])
            if file_year < 2005 or file_year > 2012:
                continue
            for row in csv_reader:
                senator_code = row[0]
                date = row[2]
                text = row[3].translate(translator)
                w.writerow([senator_code, date, text])


preprocess_files()
# os.chdir(output_path)
# output = open('output.csv', 'r')
# data = pd.read_csv(output, encoding='utf-8')
# text = pd.DataFrame(data[['text']])