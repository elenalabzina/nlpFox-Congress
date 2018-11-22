import os,string
from time import strptime
import re ,glob,csv

output_path = '/home/romina/Documents/work/Speeches_mining/outputs'
input_path = '/home/romina/Documents/work/transcripts_mining/transcripts/ABC'


def preprocess():
    translator = str.maketrans('', '', string.punctuation)
    os.chdir(input_path)
    date_text=dict()
    for txt_file in glob.glob("*.txt"):
        file = open(txt_file, 'r')
        print(file.name)
        content = file.read()
        segments = re.split(r'\d+ of \d+ DOCUMENTS', content)[1:]
        for text in segments:
            start = text.index('LENGTH') + 6 + 12
            end = text.index('LOAD-DATE')
            main_text = text[start:end]
            date_line = text.split('\n')[5]
            dates = re.findall(r'[\w]+', date_line)
            year=int(dates[2])
            if year < 2005 or year > 2012:
                continue
            month = dates[0]
            month_num = strptime(month[:3], '%b').tm_mon
            final_date = dates[2] + "-" + str(month_num) + "-" + dates[1]
            lines = main_text.split('\n')
            clean_lines = ""
            for l in lines:
                if '(ABC NEWS)' in l or 'GRAPHICS:' in l:
                    continue
                else:
                    clean_lines += l
            clean_text = clean_lines.translate(translator)
            if final_date not in date_text.keys():
                date_text[final_date] = clean_text
            else:
                date_text[final_date] += clean_text
    return date_text

def write(to_write):
    os.chdir(output_path)
    f = open('ABC_transcripts_2005_12.csv', 'w')
    w = csv.writer(f)
    w.writerow(['date', 'text'])
    for date,text in to_write.items():
        print(date)
        w.writerow([date,text])

date_text=preprocess()
write(date_text)