from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1Pb7mpFLBfpRQo7eOHWnSyq_62Pc5sJPsn3wnuc76vwQ"
SAMPLE_RANGE_NAME = "CS2!A2:E"


def sheet():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token1.json"):
        creds = Credentials.from_authorized_user_file("token1.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token1.json", "w") as token:
            token.write(creds.to_json())
    assignment_list = []
    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        for i in range(1, 4):
            assignment_list.append(values[i][3])

        return assignment_list

    except HttpError as err:
        print(err)
    # print (potential_message)


def assignment_filter(remove_list, replace_dict, assignment_list):
    txt_string = ' '
    new_list = []

    for i in assignment_list:
        # finds index of i
        index_numbers = assignment_list.index(i)
        txt_string = assignment_list[index_numbers]
        txt_list = txt_string.split("and")

        for txt in txt_list:
            strip_txt = txt.strip(" ")
            delete_flag = False
            new_txt = strip_txt
            for item in remove_list:
                if item in txt:
                    delete_flag = True
                    break
            replace_flag = True
            if not delete_flag:
                for key in replace_dict.keys():
                    if key in txt:
                        new_txt = replace_dict[key]
                        replace_flag = True
            if not delete_flag:
                new_list.append(new_txt)
            # print(f"New list in progress {new_list}")
    new_list = "Hello parents and caregivers, this an update relating to your students Computer Science 2 course. In the past 2 weeks we did: " + (', '.join(new_list))
    return new_list

remove_list = ["Headers", "Paragraphs", "Ordered lists", "Unordered lists", "Google classroom setup",
               "CS2 Schedule + Calendar", "CRLS Bell Schedule + Year in review", "Lunch times", "Course contract",
               "Day 1 survey", "Course contract Acknowledgement", "HTML2", "Line break",
               "Story of self + I want my teacher to know", "Go over autograding HTML1", "Section break", "strong",
               "em", "How to look something up", "Boilerplate", "Emojis", "Background color", "Font size", "Font color",
               "Font family", "CSS1"]

replace_dict = {"Go over autograding HTML1": "Learning how to autograde!", "HTML1": "we learned hmtl!",
                "Introductions (names)": "Introductions, Icebreakers, Logistics",
                "blockquote": "Learned How to Autograde and Expanded on the Basics of HTML",
                "Show Jack Fede's site with/without CSS https://replit.com/@ericwu/2022jfedeCS2#index.html (uncomment the css link)": "Analyzed an Example Website"}
assignment_filter(remove_list, replace_dict, sheet())
if __name__ == "__main__":
    sheet()
