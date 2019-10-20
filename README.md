# WhatsApp chat log parser

- if message has string matching the pattern on a new line, things break.
- Can't really detect what the intended message is then (maybe anomalous dates, but even that can be faked)
- assume name doesn't contain ':' (What could name contain?)
- assume first line is always valid message (skip lines until you encounter valid message)
- assume all years are from 2000 onwards i.e. begin with "20"
- no seconds data, unfortunately :-(
- add handling for system messages like 
    - "X changed the subject from A to B", 
    - "Messages to this chat and calls are now secured with end-to-end encryption. Tap for more info."
    - "X changed their phone number. You're currently chatting with their new number. Tap to add it to your contacts."
    - "X changed this group's icon"
    - "X added/removed Y"

# How to get Whatsapp log files

- go to the chat which you want to parse -> Menu -> More -> Export Chat (Save to drive, email, share)
- Logs are txt files. 

## TODO
- [ ] validation and checks everywhere
- [ ] better file handling of system args
- [ ] handling of multiple date formats

    `18/05/16, 7:06:22 PM: ‪username/phone number: message`

    `4/24/17, 6:30 PM - username/phone number: message`

    `[30/04/2015 20:55:13] username/phone number: message`

    `3/25/19, 17:14 - username: message`
    
- [ ] feature to ingest multiple logs into single csv
- [ ] find more system messages
- [ ] clean up stats.py, maybe convert to jupyter notebook
- [ ] add more analyses
    - [ ] messages vs date graphviz per user + group
    - [ ] sentiment analysis of conversation
    - [ ] word vector embedding - get "similarity" of conversations
