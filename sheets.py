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
    sheet_info = {}
    dates = []
    values = []
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

        print("Name, Major:")
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            dates.append({row[0]})
            values.append({row[3]})
            # sheet_info = {f"{row[0]}, {row[3]}"}
        for date in dates:
            for value in values:
                sheet_info[date] = value
                values.remove(value)
                break
    except HttpError as err:
        print(err)
    print(sheet_info)

if __name__ == "__main__":
    sheet()
