from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime
from date import date

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = "1Pb7mpFLBfpRQo7eOHWnSyq_62Pc5sJPsn3wnuc76vwQ"



def sheet(p_start_date, range_name):
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
            .get(spreadsheetId=SPREADSHEET_ID, range=range_name)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return

        p_start_date -= 10
        for i in range(10):

            assignment_list.append(values[p_start_date][3])
            p_start_date += 1

        return assignment_list

    except HttpError as err:
        print(err)
    # print (potential_message)

def sheet_date(range_name):
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
            .get(spreadsheetId= SPREADSHEET_ID, range=range_name)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return
        dates = []
        for i in range(180):
            dates.append(values[i][1])
        new_date = date()
        start_date = 0
        for day in dates:
            if day == new_date:
                start_date = dates.index(day)
        return start_date

    except HttpError as err:
        print(err)

# Checks through both the list containing assignments to be removed and the dictionary with assignments to be replaces, and
def assignment_filter(remove_list, replace_dict, assignment_list, course):
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
    # Prevents duplicates
    new_list = list(set(new_list))
    new_list = "Hello parents and caregivers, this an update relating to your students "+ course + " course. In the past 2 weeks we did: " + (', '.join(new_list))
    return new_list
