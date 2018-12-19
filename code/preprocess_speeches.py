import csv, sys
import os, glob
import string
import re

output_path = '/cluster/work/lawecon/Projects/Fox-CongressSpeeches/Output/congressional_speeches'
input_path = '/cluster/work/lawecon/Projects/Fox-CongressSpeeches/Data/speeches-segmented/greg-tables'


def preprocess_files():
    csv.field_size_limit(sys.maxsize)
    os.chdir(output_path)
    f = open('output.csv', 'w')
    os.chdir(input_path)
    w = csv.writer(f)
    w.writerow(['senator_code', 'date', 'senator_term', 'speech_number', 'text'])
    translator = str.maketrans('', '', string.punctuation)
    senator_date = dict()
    for file in glob.glob("*.csv"):
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            file_year = int(csv_file.name.split('-')[0])
            if file_year < 2005 or file_year > 2012:
                continue
            print(csv_file.name)
            for row in csv_reader:
                temp = str(row[0]).split('_')
                term = temp[3] + "_" + temp[4]
                speech_number = temp[5]
                senator_code = temp[0] + "_" + temp[1] + "_" + temp[2]
                date = row[2]
                text = row[3].translate(translator)
                text = re.sub(r'\s', ' ', text)
                if (senator_code, date) not in senator_date.keys():
                    senator_date[(senator_code, date)] = {'text': text, 'term': term,
                                                          'speech_number': speech_number}
                else:
                    senator_date[(senator_code, date)]['text'] += " " + text
                    senator_date[(senator_code, date)]['term'] += "; " + term
                    senator_date[(senator_code, date)]['speech_number'] += '; ' + speech_number

    for key, value in senator_date.items():
        text = re.sub(' +', ' ', value['text'])
        w.writerow([key[0], key[1], value['term'], value['speech_number'], text])


preprocess_files()