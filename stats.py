#!/usr/bin/python3

import pandas as pd

df = pd.read_csv('output.csv')

# List of top 10 participants with message counts
name_totals = df.groupby(['name']).count()
name_totals = name_totals.sort_values(['message'], ascending=False)
print(name_totals.head(10))

# List of bottom 10 participants with message counts
print(name_totals.tail(10))

# Top 10 longest messages
df['msg_len'] = df['message'].str.len()
longest_messages = df.sort_values(['msg_len'], ascending=False)
print(longest_messages.head(10))

# Most media sent by someone
df['is_media'] = df['message'] == '<Media omitted>'
media_counts = df[df['is_media']].groupby(['name']).count()
media_counts = media_counts.sort_values(['message'], ascending=False)
print(media_counts.head(10))

# Word frequencies
# Ref: https://stackoverflow.com/questions/46786211/counting-the-frequency-of-words-in-a-pandas-data-frame
# TODO: optimize this
word_freqs = df.message.str.split(expand=True).stack().value_counts()
print(word_freqs.head(100))