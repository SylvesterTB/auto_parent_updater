# Auto Parent Updater 
## Description
- **Product**:
  - Program that regularly updates parents on class content
  - Uses Google Sheets API to retrieve schedule information
  - Utilizes Gmail and Twilio API to send messages
  - Runs on a regular interval using Kron
![Alt text](readme2.png)

## User Guide

- fill in remove_list and replace_dict and classcode for each class (quickstart.py 118)
- input account_sid and auth_token (quickstart.py 166)
- every slot in the assignments column of the spreadsheet  needs to be filled in. (say work day instead of blank space, etc.)
- aspen username and password  (quickstart.py 179)
- program must run (on kron) every two weeks on the last Friday, and must be restarted every semester. 
- keep Twilio account loaded with credit
- each semester, input current list of courses you want to run the project for (quickstart.py 164) note: courses must be named how they appear in the schedule spreadsheet
- install requirements.txt