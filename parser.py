#!/usr/bin/env python3

import datetime
import re
import sys

import pandas as pd

pat = re.compile(r'^(?P<month>\d{1,2})'
                  '/'
                  '(?P<day>\d{1,2})'
                  '/'
                  '(?P<year>\d{1,2})'
                  ', '
                  '(?P<hour>\d{1,2})'
                  ':'
                  '(?P<minute>\d{2})'
                  ' '
                  '(?P<time_of_day>am|pm|AM|PM)'
                  ' - '
                  '(?P<name>[^:]+)'
                  ': '
                  '(?P<message>.+)$', re.M)

datetimes = []
names = []
messages = []

def parse_line(line):
    hr = int(line['hour'])
    if line['time_of_day'] in ["pm", "PM"] and hr != 12:
        hr += 12
    dt = datetime.datetime(int("20" + line['year']), int(line['month']), int(line['day']), hr, int(line['minute']))
    datetimes.append(dt)
    names.append(line['name'])
    messages.append(line['message'])

def parse_file(input_file):
    input = input_file.read()
    input_lines = input.splitlines()

    prev_m = {}
    i = 0
    while i < len(input_lines):
        prev_m = pat.fullmatch(input_lines[i])
        if prev_m:
            prev_m = prev_m.groupdict()
            break
        i += 1
    for line in input_lines[i + 1:]:
        m = pat.fullmatch(line)
        if m:
            parse_line(prev_m)
            prev_m = m.groupdict()
        else:
            prev_m['message'] += "\n" + line
    parse_line(prev_m)

def build_csv(output_file_name):
    dict = {'datetime': datetimes, 'name': names, 'message': messages}

    df = pd.DataFrame(dict)
    df.sort_values(by=['datetime'])
    df.to_csv(output_file_name, index=False)

if __name__ == "__main__":
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    input_file = open(input_file_name, 'r')
    
    parse_file(input_file)
    build_csv(output_file_name)
