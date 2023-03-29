import pandas as pd
import numpy as np
import csv

with open(r'data\raw\album-lineup.csv', 'r', newline='',
          encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='\"')
    for row in csv_reader:
        print(row[1].replace('\ufeff', ''))
        break


df = pd.read_csv(r'data\transformed\album-lineup-transformed.csv',
                 na_filter=False)
measurer = np.vectorize(len)
print(measurer(df.values.astype(str)).max(axis=0))
