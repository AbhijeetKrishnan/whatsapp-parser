import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Imports
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import math

    return math, np, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Load data
    """)
    return


@app.cell
def _(pd):
    DATA_FILE = 'data/test.csv'
    df = pd.read_csv(DATA_FILE)
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Preview data
    """)
    return


@app.cell
def _(df):
    print(df.head(10))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stats
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## List participants ordered by decreasing message counts
    """)
    return


@app.cell
def _(df):
    name_totals = df.groupby(['name']).count()
    name_totals = name_totals.sort_values(['message'], ascending=False)
    name_totals = name_totals.drop(columns="datetime")
    print(name_totals)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Top-n longest messages
    """)
    return


@app.cell
def _(df):
    _n = 10
    longest_messages = df.sort_values(['message'], ascending=False, key=lambda x: x.str.len())
    print(longest_messages.head(_n))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Most media sent by someone
    """)
    return


@app.cell
def _(df):
    _n = 10
    media_counts = df[df['message_type'] == 'media_omitted'].groupby(['name']).count().drop(columns=['datetime', 'message'])
    print(media_counts.head(_n))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Various statistics

    - Most group name changes
    - Number of birthdays
    - Number of group exits
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Most group name changes
    """)
    return


@app.cell
def _(df):
    _n = 10
    name_change_counts = df[df['message_type'] == 'subject_name_change'].groupby(['name']).count().drop(columns=['datetime', 'message']).sort_values(by=['message_type'], ascending=False)
    print(name_change_counts.head(_n))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Number of birthdays
    """)
    return


@app.function
def is_birthday_message(message):
    word_list = ['birthday', 'hbd', 'happy birthday']
    for word in word_list:
        if word in str(message):
            return True
    return False


@app.cell
def _(df):
    birthday_messages = df[(df['message_type'] == 'subject_name_change') & (df['message'].apply(is_birthday_message))]
    birthday_messages
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Number of group exits
    """)
    return


@app.cell
def _(df):
    group_exits = df[(df['message_type'] == 'left') | (df['message_type'] == 'you_left')]
    num_group_exits = len(group_exits)
    print(num_group_exits)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Word frequencies
    Ref: https://stackoverflow.com/questions/46786211/counting-the-frequency-of-words-in-a-pandas-data-frame
    """)
    return


@app.cell
def _(df):
    _n = 100
    word_freqs = df[df['message_type'] == 'message']['message'].str.split(expand=True).stack().value_counts()
    print(word_freqs.head(_n))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Word Cloud

    Ref: https://www.kaggle.com/code/olgaberezovsky/word-cloud-using-python-pandas/notebook
    """)
    return


@app.cell
def _(plt):
    from wordcloud import WordCloud, STOPWORDS
    import re

    plt.style.use('bmh')
    return STOPWORDS, WordCloud, re


@app.cell
def _(STOPWORDS, df, re):
    all_messages = " ".join(df[df['message_type'] == 'message']['message'].dropna().astype(str))
    all_messages = re.sub(r'http\S+', '<LINK>', all_messages)
    stopwords = STOPWORDS.add('LINK')
    return all_messages, stopwords


@app.cell
def _(WordCloud, all_messages, plt, stopwords):
    plt.figure(figsize=(10, 8))
    wc = WordCloud(background_color='white', stopwords=stopwords, max_words=100, width=800, height=600)
    wc.generate(all_messages)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.gca()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Activity graph
    Plot message frequency with respect to time, to analyze when each individual is most active
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Get number of hours of activity
    """)
    return


@app.cell
def _(df, math, np, pd):
    first_message_datetime = df.at[0, 'datetime']
    last_message_datetime = df.at[df.index[-1], 'datetime']
    print(last_message_datetime)

    time_delta = (pd.Timestamp(last_message_datetime) - pd.Timestamp(first_message_datetime)) / np.timedelta64(1, 'h')
    time_delta = math.ceil(time_delta)
    print(time_delta)
    return first_message_datetime, time_delta


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Create timeseries of required period
    """)
    return


@app.cell
def _(first_message_datetime, pd, time_delta):
    dti = pd.date_range(first_message_datetime, periods=time_delta+1, freq='h')
    dti
    return (dti,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Digitize datetime using timeseries
    """)
    return


@app.cell
def _(dti, pd):
    bins = pd.IntervalIndex.from_arrays(dti[:-1], dti[1:], closed='left')
    bins
    return (bins,)


@app.cell
def _(bins, df, pd):
    timestamps = pd.to_datetime(df['datetime'].values)
    cat_obj = pd.cut(timestamps, bins)
    vals = pd.Series(cat_obj).value_counts(sort=False)
    vals
    return (vals,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Create graph
    - [] Check if you can use bins argument to value_counts() by converting df['datetime']
    """)
    return


@app.cell
def _(dti, plt, vals):
    plt.figure()
    plt.xlabel('Date')
    plt.ylabel('Message frequency per hour')
    plt.suptitle('Group Activity Graph')
    plt.plot(dti[:-1], vals.values)
    plt.xticks(rotation=90)
    plt.gca()
    return


if __name__ == "__main__":
    app.run()
