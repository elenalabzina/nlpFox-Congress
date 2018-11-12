import csv, sys
import os, glob
import string
import pandas as pd

output_path = '/home/romina/Documents/work/Speeches_mining/outputs'
input_path = '/home/romina/Documents/work/speeches-segmented/greg-tables'


def preprocess_files():
    csv.field_size_limit(sys.maxsize)
    os.chdir(output_path)
    f = open('output.csv', 'w')
    os.chdir(input_path)
    w = csv.writer(f)
    w.writerow(['senator code', 'date', 'text'])
    to_be_removed=string.punctuation+"\n\t\r"
    translator = str.maketrans('', '', to_be_removed)
    senator_date=dict()
    for file in glob.glob("*.csv"):
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            file_year = int(csv_file.name.split('-')[0])
            if file_year < 2005 or file_year > 2012:
                continue
            for row in csv_reader:
                temp=str(row[0]).split('_')
                senator_code=temp[0]+"_"+temp[1]+"_"+temp[2]
                date = row[2]
                text = row[3].translate(translator)
                if (senator_code,date) not in senator_date.keys():
                    senator_date[(senator_code,date)]=text
                else:
                    senator_date[(senator_code, date)] += " "+text

    for key,value in senator_date.items():
        w.writerow([key[0], key[1], value])



preprocess_files()


