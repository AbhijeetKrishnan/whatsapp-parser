#!/usr/bin/python3

import sys
import re
import datetime
import pandas as pd

pat = re.compile(r'^(?P<day>\d{2})'
                  '/'
                  '(?P<month>\d{2})'
                  '/(?P<year>\d{2})'
                  ', '
                  '(?P<hour>\d{1,2})'
                  ':'
                  '(?P<minute>\d{2})'
                  ' '
                  '(?P<time_of_day>am|pm)'
                  ' - '
                  '(?P<name>[^:]+)'
                  ': '
                  '(?P<message>.+)$', re.M)

# if message has string matching this pattern on a new line, things break.
# Can't really detect what the intended message is then (maybe anomalous dates, but even that can be faked)
# assume name doesn't contain ':'
# assume first line is always valid message (skip lines until you encounter valid message)
# assume all year's are from 2000 onwards i.e. begin with "20"
# no seconds data, unfortunately :-(
# add handling for system messages like 
# "X changed the subject from A to B", 
# "Messages to this chat and calls are now secured with end-to-end encryption. Tap for more info."
# "X changed their phone number. You're currently chatting with their new number. Tap to add it to your contacts."

# TODO
# validation and checks everywhere
# better file handling of system args
# feature to combine multiple logs into single csv

datetimes = []
names = []
messages = []

def parse_line(line):
    hr = int(line['hour'])
    if line['time_of_day'] == "pm" and hr != 12:
        hr += 12
    dt = datetime.datetime(int("20" + line['year']), int(line['month']), int(line['day']), hr, int(line['minute']))
    datetimes.append(dt)
    names.append(line['name'])
    messages.append(line['message'])

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    input_file = open(input_file, 'r')
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

    dict = {'datetime': datetimes, 'name': names, 'message': messages}

    df = pd.DataFrame(dict)

    df.to_csv(output_file, index=False)