#!/usr/bin/env python3

import argparse
import csv
import datetime
import re
import sys
from enum import Enum, unique

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
record_pat = re.compile(DT_PREFIX, re.DOTALL)

MESSAGE = r"^(?P<name>[^:]+): (?P<contents>.+)$"
msg_pat = re.compile(MESSAGE, re.DOTALL)

@unique
class MessageType(Enum):
    SUBJECT_NAME_CHANGE = r"^(?P<name>[^:]+) changed the subject from \"(?P<old>.+)\" to \"(?P<new>.+)\"$"
    PHONE_NUM_CHANGE = r"^(?P<name>[^:]+) changed their phone number to a new number\. Tap to message or add the new number\.$"
    PHONE_NUM_CHANGE_FULL = r"^(?P<name>[^:]+) changed to (?P<target>.+)$"
    GROUP_ICON_CHANGE = r"^(?P<name>[^:]+) changed this group's icon$"
    GROUP_ICON_DELETE = r"^(?P<name>[^:]+) deleted this group's icon$"
    ADDED = r"^(?P<name>[^:]+) added (?P<target>.+)$"
    LEFT = r"^(?P<name>[^:]+) left$"
    YOU_LEFT = r"^You left$"
    REMOVED = r"^(?P<name>[^:]+) removed (?P<target>[^:]+)$"
    SECURITY_CODE_CHANGE = r"^Your security code with (?P<name>.+) changed\. Tap to learn more\.$"
    SECURITY_CODE_CHANGE_ALL = r"^Your security code with all participants changed\. Tap to learn more\.$"
    DISAPPEARING_ENABLE = r"^(?P<name>[^:]+) turned on disappearing messages\. All new messages will disappear from this chat (?P<num>\d+) (?P<period>days|hours) after they're sent\.$"
    DISAPPEARING_DISABLE = r"^(?P<name>[^:]+) turned off disappearing messages\.$"
    CALL_START = r"^(?P<name>[^:]+) started a call$"
    MISSED_VIDEO_CALL = r"^(?P<name>[^:]+): Missed video call$"
    MEDIA_OMITTED = r"^(?P<name>[^:]+): <Media omitted>$"

    def __str__(self):
        return self._name_.lower()

    def get_regex_pat(self):
        return re.compile(self._value_)

MESSAGE_PATTERNS = [(str(msg_type), msg_type.get_regex_pat()) for msg_type in MessageType]

def detect_message_type(message):
    global msg_pat
    for msg_type, pat in MESSAGE_PATTERNS:
        m = pat.fullmatch(message)
        if m:
            return msg_type, m
    if m := msg_pat.fullmatch(message):
        return 'message', m
    else:
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
    name = match.groupdict().get("name", "N/A")
    contents = match.groupdict().get("contents", msg)
    return dt, name, contents, msg_type

def get_records(input):
    input_lines = input.splitlines()
    m_prev = {}
    i = 0

    # skip lines until we find the first matching record
    while i < len(input_lines):
        m_prev = record_pat.fullmatch(input_lines[i])
        if m_prev:
            m_prev = m_prev.groupdict()
            break
        i += 1

    for line in input_lines[i + 1:]:
        m = record_pat.fullmatch(line)
        if m:
            date, name, msg, msg_type = parse_match(m_prev)
            record = {
                'datetime': date,
                'name': name,
                'message': msg,
                'message_type': msg_type,
            }
            yield record
            m_prev = m.groupdict()
        else:
            m_prev['message'] += "\n" + line

    date, name, msg, msg_type = parse_match(m_prev)
    record = {
        'datetime': date,
        'name': name,
        'message': msg,
        'message_type': msg_type,
    }
    yield record

def parse_args():
    parser = argparse.ArgumentParser(
        prog="WhatsApp Chat Log Parser",
        description="Converts an exported WhatsApp chat log into a CSV file for data analysis.",
    )
    parser.add_argument('input', action='store', help="input filename to read WhatsApp chat records from")
    parser.add_argument('output', action='store', help="output filename to write CSV file to")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    with open(args.input, 'r') as input_file:
        input = input_file.read() # needs file to be loadable in memory
    records = get_records(input)

    with open(args.output, 'w', newline='') as output_file:
        fieldnames = ['datetime', 'name', 'message', 'message_type']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames, escapechar='\\')
        writer.writeheader()
        num_rows = 0
        for record in records:
            writer.writerow(record)
            num_rows += 1
    print("Wrote {} rows to {}".format(num_rows, args.output))
