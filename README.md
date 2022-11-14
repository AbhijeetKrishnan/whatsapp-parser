# WhatsApp Chat Log Parser

_(Developed assuming WhatsApp Messenger Version 2.22.23.77)_

## Usage

- Export your WhatsApp chat as a `.txt` file by following the instructions
  [here](https://faq.whatsapp.com/1180414079177245/?helpref=uf_share).
- Ensure your system has Python v3.10 or higher installed.
- Navigate to the project root and install any missing dependencies using the command below. These are only for running
the IPython notebook, and not for running the parser.

    ```bash
    python3 -m pip install -r requirements.txt
    ```

- Run the `parser.py` script to convert your exported chat logs into a CSV file.

    ```bash
    ./parser.py [INPUT] [OUTPUT]
    ```

- Change the variable `DATA` in the `stats.ipynb` file to match your CSV filename.
- Run all cells in the notebook to view the analysis and perform your own.
- I **highly recommend** you install the `pre-commit` script as a pre-commit hook for git. It clears the output cells in
the `stats.ipynb` notebook before committing any changes. This will prevent accidentally leaking sensitive chat info
present in these output cells by committing them to GitHub.

    ```bash
    cp pre-commit .git/hooks/
    ```

## Assumption regarding start of records

Since WhatsApp Messenger doesn't export files using proper delimiters, it is impossible to differentiate a new message
from the previous message's contents.

For example, let's say person "Ashok Kumar" sent the following message at 1:00 PM on 2022/11/12.

![WhatsApp chat demonstrating ambiguity in parsing logs](/assets/whatsapp_chat.png)

WhatsApp would export a record for this message as -

```
11/12/12, 1:00 PM - Ashok Kumar: 11/12/22, 1:01 PM - ABC: Message 1
11/12/22, 1:02 PM - Ashok Kumar: Message 2
```

There is no way to tell that the second line is actually part of the previous record's message, since WhatsApp does not
include any delimiter to identify when a message for a particular record is over. Thus, I've made the assumption that
any line that begins with `[mm]/[dd]/[yy], [h]:[mm] AM|PM - ` is the beginning of a new record. Errors of the kind I
mentioned will arise, but they are unavoidable.