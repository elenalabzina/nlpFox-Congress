import os, string
import re, glob, csv,sys
from time import strptime

from nltk import sent_tokenize

output_path = '/home/romina/Documents/work/Speeches_mining/outputs'
input_path = '/home/romina/Documents/work/transcripts_mining/transcripts/MSNBC'
input_directory = ['All In with Chris Hayes', 'Ashleigh Banfield On Location', 'Buchanan & Press', 'Countdown with Keith Olbermann', 'Donahue'
    , 'Hardball with Chris Matthews', 'Live with Dan Abrams', 'Morning Joe', 'Politics Nation',
                   'Race for the White House and 1600 Pennsylvania Ave', 'Rita Cosby Live and Direct',
                   'Scarborough Country','The Ed Show','The Last Word with Lawrence O\'Donnell','The News with Brian Williams',
                   'The Rachel Maddow Show','The Savage Nation','Tucker']


def preprocess():
    csv.field_size_limit(sys.maxsize)
    date_text=dict()
    translator = str.maketrans('', '', string.punctuation)
    for i in range(len(input_directory)):
        os.chdir(input_path + '/' + input_directory[i])
        for txt_file in glob.glob("*.txt"):
            file = open(txt_file, 'r')
            # find year by file name to avoid useless processing
            year = int(re.findall(r'\d+', file.name)[0])
            if year < 2005 or year > 2012:
                continue
            print(file.name)
            content = file.read()
            # to split each document : they have this pattern in the first line 1 of 415 DOCUMENTS
            segments = re.split(r'\d+ of \d+ DOCUMENTS', content)[1:]
            for text in segments:
                # first line which the main text starts
                start = text.index('LENGTH') + 6 + 13
                # end of the main text
                end = text.index('LOAD-DATE')
                main_text = text[start:end]
                date_line = text.split('\n')[5]
                dates = re.findall(r'[\w]+', date_line)
                month = dates[0]
                month_num = strptime(month[:3], '%b').tm_mon
                final_date = dates[2] + "-" + str(month_num) + "-" + dates[1]
                enter_seperated_line = main_text.split('\n')
                #without_speaker = re.sub(r'([A-Z]+\s*(\((\w|\s)+\))?\s*)+:', ' ', main_text_clean)
                line_without_capital = ''
                for lines in enter_seperated_line:
                    # redundant_details = re.search(r'\(([A-Z]+|\s*)+\)', l)
                    # line= re.sub(' +', ' ', l)
                    if lines.isupper():
                        continue
                    all_lines = sent_tokenize(lines)
                    for line in all_lines:

                        speakers = line.split(':')
                        is_speaker = False
                        if len(speakers) > 1:
                            speaker = speakers[0]
                            if speaker.isupper():
                                is_speaker = True
                            else:
                                details_start = speaker.split('(')
                                if (len(details_start) > 1):
                                    details_end = details_start[1].split(')')
                                    if len(details_end) > 1:
                                        speaker = details_start[0] + details_end[1]
                                        if speaker.isupper() or speaker == '':
                                            is_speaker = True
                        if is_speaker:
                            line_without_capital += ''.join(speakers[1:])
                        else:
                            line_without_capital += ' ' + line
                no_punc_text = line_without_capital.translate(translator)
                clean_text = ' '.join(no_punc_text.split())
                # for each date, merge all observations
                if final_date not in date_text.keys():
                    date_text[final_date] = clean_text
                else:
                    date_text[final_date] += clean_text
    return date_text


def write(to_write):
    os.chdir(output_path)
    f = open('MSNBC_transcripts_by_day_2005_12.csv', 'w')
    w = csv.writer(f)
    w.writerow(['date', 'text'])
    for date, text in to_write.items():
        print(date)
        w.writerow([date, text])

date_text = preprocess()
write(date_text)