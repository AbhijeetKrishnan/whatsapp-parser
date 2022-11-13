# WhatsApp Chat Log Parser

_(Developed assuming WhatsApp Messenger Version 2.22.23.77)_

# Usage

- Export your WhatsApp chat as a `.txt` file by following the instructions [here](https://faq.whatsapp.com/1180414079177245/?helpref=uf_share).
- Ensure your system has Python v3.10 or higher installed.
- Navigate to the project root and install any missing dependencies using -

    ```bash
    python3 -m pip install -r requirements.txt
    ```

- Run the `parser.py` script to convert your exported chat logs into a CSV file.

    ```bash
    ./parser.py [INPUT] [OUTPUT]
    ```

- Change the variable `DATA` in the `stats.ipynb` file to match your CSV filename.
- Run all cells in the notebook to view the analysis and perform your own.