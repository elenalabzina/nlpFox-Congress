import csv
import os
from string import ascii_lowercase, digits
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
import nltk
import pandas as pd
from nltk.probability import FreqDist
from statistics import mean, pstdev,median

output_path = '/cluster/work/lawecon/Projects/Fox-CongressSpeeches/Output/transcripts'

os.chdir(output_path)

output = open('FNC_transcripts_by_year_2005_12.csv', 'r')
data = pd.read_csv(output, encoding='utf-8')
text = pd.DataFrame(data[['text']])
data = list()
for index, content in text.iterrows():
    data.append(content['text'])

stemmer = SnowballStemmer("english", ignore_stopwords=True)
##setting up and extending stopwords
stop = stopwords.words('english')
stop.extend(
    ['nevertheless', 'would', 'nether''the', 'in', 'may', 'also', 'zero', 'one', 'two', 'three', 'four', 'five',
     'six', 'seven', 'eight', 'nine', 'ten', 'quot', 'across', 'among', 'beside', 'however', 'yet',
     'within', 'et'] + list(ascii_lowercase))

# for removing digits
translator = str.maketrans('', '', digits)

tokens = []
for statement in data:
    statement_removed_digits = statement.translate(translator)
    words = word_tokenize(statement_removed_digits.lower())
    words_clean = []
    for word in words:
        if word not in stop:
            words_clean.append(stemmer.stem(word))
    tokens.append(words_clean)

n = 3
all_trigrams = list()
text_trigram = list()
for token_group in tokens:
    trigram_group = list(nltk.ngrams(token_group, n))
    text_trigram.append(trigram_group)
    for trigram in trigram_group:
        all_trigrams.append(trigram)

total = len(all_trigrams)
cutoff = 0.00001 * total
fdist = FreqDist(all_trigrams)
selected_trigrams = {k: v for k, v in fdist.items() if v > cutoff}
selected_trigrams_count = list(selected_trigrams.values())
selected_trigrams = list(selected_trigrams.keys())

binary_matrix = np.zeros(shape=(len(text_trigram), len(selected_trigrams)))
frequency_matrix = np.zeros(shape=(len(text_trigram), len(selected_trigrams)))

for index in range(0, len(text_trigram)):
    for token in text_trigram[index]:
        if token in selected_trigrams:
            binary_matrix[index, selected_trigrams.index(token)] = 1
            frequency_matrix[index, selected_trigrams.index(token)] = text_trigram[index].count(token)

np.savetxt("FNC_transcripts_by_year_2005_12_binary.csv", binary_matrix.astype(int), fmt='%i', delimiter=",")
np.savetxt("FNC_transcripts_by_year_2005_12_frequency.csv", frequency_matrix.astype(int), fmt='%i', delimiter=",")

mu = mean(selected_trigrams_count)
st = pstdev(selected_trigrams_count, mu)
med=median(selected_trigrams_count)
maxium=max(selected_trigrams_count)
f = open('FNC_transcripts_by_year_2005_12_trigrams_position.csv', 'w')
w = csv.writer(f)
w.writerow(['mean , stdev', mu, st])
w.wrtierow(['median, max ',med,maxium])
w.writerow(['position', 'trigrams', 'count'])
for index in range(len(selected_trigrams)):
    w.writerow([index, selected_trigrams[index], selected_trigrams_count[index]])
