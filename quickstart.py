import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from sheets import sheet, assignment_filter, sheet_date
from Twilio_sms import Twilio
import datetime


# If modifying these scopes, delete the file credentials.json.

SCOPES = ['https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.labels',
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.addons.current.action.compose']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None

    # The file credentials.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # if os.path.exists("token.pickle"):
    #   with open('token.pickle', 'rb') as token:
    #     creds = pickle.load(token)
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
        # with open("token.pickle", "w") as token:
        #   token.write(creds)

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])

        if not labels:
            print("No labels found.")
            return
        print("Labels:")
        for label in labels:
            print(f'This is label hooray! {label["name"]}')
        print("I'm done kind person!")
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")
    msg = 'word'
    return creds


#######################################################################################################

def send_message(service, user_id, message):
    try:
        message = service.users().drafts().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as e:
        print('An error occurred: %s' % e)
        return None


def gmail_send_message(creds, contact_list, p_message_content):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    # creds, _ = google.auth.default()

    try:
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        message.set_content(
            p_message_content)

        # message["To"] = "syltester616@gmail.com"
        message["Bcc"] = contact_list
        message["From"] = "syltester616@gmail.com"
        message["Subject"] = "Bi-weekly CS2 update"

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None
    return send_message


# gets emails in emails.txt
def reFormat():
    with open("emails.txt") as file:
        lines = file.readlines()
        for i in range(3):
            lines[i] = lines[i].strip()
            # lines.replace(i, i.strip())
        return lines


# list of emails that are recieving notifications
gmail_list = reFormat()


# this list currently contains a set of example filters
# Every item in remove_list is removed form the message
remove_list = ["Headers", "Paragraphs", "Ordered lists", "Unordered lists", "Google classroom setup",
               "CS2 Schedule + Calendar", "CRLS Bell Schedule + Year in review", "Lunch times", "Course contract",
               "Day 1 survey", "Course contract Acknowledgement", "HTML2", "Line break",
               "Story of self + I want my teacher to know", "Go over autograding HTML1", "Section break", "strong",
               "em", "How to look something up", "Boilerplate", "Emojis", "Background color", "Font size", "Font color",
               "Font family", "CSS1", "Embedded PE"]

# Every key in replaced_dict is replaced with its value
replace_dict = {"Go over autograding HTML1": "Learning how to autograde!", "HTML1": "we learned hmtl!",
                "Introductions (names)": "Introductions, Icebreakers, Logistics",
                "blockquote": "Learned How to Autograde and Expanded on the Basics of HTML",
                "Show Jack Fede's site with/without CSS https://replit.com/@ericwu/2022jfedeCS2#index.html (uncomment the css link)": "Analyzed an Example Website", "Gym": "embedded gym class"}

messages = []
message_content = assignment_filter(remove_list, replace_dict, sheet(sheet_date()))
print(message_content)

#Remove before making repository public
account_sid = 'ACe3a7440701bd6a3bdff8a5df9aa8afc5'
auth_token = 'ba728f474ed29dbff1a3c48450934cc8'

def reFormat_phone():
    with open("phone_numbers.txt") as file:
        lines = file.readlines()
        for i in range(2):
            lines[i] = lines[i].strip()
            # lines.replace(i, i.strip())
        return lines


# list of emails that are recieving notifications
phone_list = reFormat_phone()


if __name__ == "__main__":
    gmail_send_message(main(), gmail_list, message_content)
    Twilio(account_sid, auth_token, phone_list, message_content)
