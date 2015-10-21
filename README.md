# gpush: script to text data from Google Sheets

To use:
 1. Clones this repo
 1. Create a virtualenv
 1. Create a config.py with:
    * Variables that use curl to send texts using the textbelt.com free SMS API
        * i.e. `msg_me = 'curl http://textbelt.com/text -d number=5555555555 -d "message='`
    * Variables for your Google Developer Account and a PK12 key.
 1. Install dependencies by: `pip install -r requirements.txt`
 1. Run it manually `python gpush.py` or setup a crontab.
