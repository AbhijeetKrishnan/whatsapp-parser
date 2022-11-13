#!/usr/bin/env python3

import argparse
import datetime
import re
import sys

import pandas as pd

DT_PREFIX = (
    r"^(?P<month>\d{1,2})"
    r"/"
    r"(?P<day>\d{1,2})"
    r"/"
    r"(?P<year>\d{1,2})"
    r", "
    r"(?P<hour>\d{1,2})"
    r":"
    r"(?P<minute>\d{2})"
    r" "
    r"(?P<time_of_day>am|pm|AM|PM)"
    r" - "
    r"(?P<message>.+)$"
)
pat = re.compile(DT_PREFIX, re.DOTALL)

SUBJECT_NAME_CHANGE = (
    r"^(?P<name>.+) changed the subject from \"(?P<old>.+)\" to \"(?P<new>.+)\"$"
)

PHONE_NUM_CHANGE = (
    r"^(?P<name>.+) changed their phone number to a new number\. Tap to message or add the new number\.$"
)

PHONE_NUM_CHANGE_FULL = (
    r"^(?P<old>.+) changed to (?P<new>.+)$"
)

GROUP_ICON_CHANGE = r"^(?P<name>.+) changed this group's icon$"
GROUP_ICON_DELETE = r"^(?P<name>.+) deleted this group's icon$"
ADDED = r"^(?P<adder>.+) added (?P<addee>.+)$"
LEFT = r"^(?P<name>.+) left$"
YOU_LEFT = r"^You left$"
REMOVED = r"^(?P<remover>.+) removed (?P<removed>.+)$"
SECURITY_CODE_CHANGE = r"^Your security code with (?P<name>.+) changed\. Tap to learn more\.$"
SECURITY_CODE_CHANGE_ALL = r"^Your security code with all participants changed\. Tap to learn more\.$"
MESSAGE = r"^(?P<name>.+): (?P<contents>.+)$"
DISAPPEARING_ENABLE = r"^(?P<name>.+) turned on disappearing messages\. All new messages will disappear from this chat (?P<num>\d+) (?P<period>days|hours) after they're sent\.$"
DISAPPEARING_DISABLE = r"^(?P<name>.+) turned off disappearing messages\.$"
CALL_START = r"^(?P<name>.+) started a call$"

SYSTEM_MESSAGES = {
    "subject_name_change": re.compile(SUBJECT_NAME_CHANGE),
    "phone_num_change": re.compile(PHONE_NUM_CHANGE),
    "phone_num_change_full": re.compile(PHONE_NUM_CHANGE_FULL),
    "group_icon_change": re.compile(GROUP_ICON_CHANGE),
    "group_icon_delete": re.compile(GROUP_ICON_DELETE),
    "added": re.compile(ADDED),
    "left": re.compile(LEFT),
    "you_left": re.compile(YOU_LEFT),
    "removed": re.compile(REMOVED),
    "security_code_change": re.compile(SECURITY_CODE_CHANGE),
    "security_code_change_all": re.compile(SECURITY_CODE_CHANGE_ALL),
    "disappearing_enable": re.compile(DISAPPEARING_ENABLE),
    "disappearing_disable": re.compile(DISAPPEARING_DISABLE),
    "message": re.compile(MESSAGE, re.DOTALL),
    "call_start": re.compile(CALL_START),
}


def detect_message_type(message):
    for msg_type, pat in SYSTEM_MESSAGES.items():
        m = pat.fullmatch(message)
        if m:
            return msg_type, m
    print("Unknown message type: {}. Please file an issue!".format(message), file=sys.stderr)
    return "unknown", None

def parse_match(m):
    yyyy = int("20" + m["year"]) # assume yy is always 20yy
    mm = int(m["month"])
    dd = int(m["day"])
    hh = int(m["hour"])
    if m["time_of_day"] in ["pm", "PM"] and hh < 12:
        hh += 12
    mins = int(m["minute"])

    msg = m["message"]
    msg_type, match = detect_message_type(msg)

    dt = datetime.datetime(yyyy, mm, dd, hh, mins)
    if msg_type == "message":
        name = match["name"]
        contents = match["contents"]
    else:
        name = "N/A"
        contents = msg
    return dt, name, contents, msg_type

def parse_file(input_file):
    input = input_file.read()
    input_lines = input.splitlines()

    datetimes = []
    names = []
    messages = []
    message_types = []

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
            date, name, msg, msg_type = parse_match(prev_m)
            datetimes.append(date)
            names.append(name)
            messages.append(msg)
            message_types.append(msg_type)

            prev_m = m.groupdict()
        else:
            prev_m['message'] += "\n" + line

    date, name, msg, msg_type = parse_match(prev_m)
    datetimes.append(date)
    names.append(name)
    messages.append(msg)
    message_types.append(msg_type)

    csvdict = {'datetime': datetimes, 'name': names, 'message': messages, 'message_type': message_types}
    return csvdict

def write_csv(csvdict, output_filename):
    df = pd.DataFrame(csvdict)
    df.sort_values(by=['datetime'])
    df.to_csv(output_filename, index=False, escapechar='\\')

def parse_args():
    parser = argparse.ArgumentParser(
        prog="WhatsApp Chat Log Parser",
        description="Converts an exported WhatsApp chat log into a CSV file for data analysis.",
    )
    parser.add_argument('input', action='store', help="Input filename to read WhatsApp chat records from")
    parser.add_argument('output', action='store', help="Output filename to write CSV file to")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    with open(args.input, 'r') as input_file:
        csvdict = parse_file(input_file)
        write_csv(csvdict, args.output)
