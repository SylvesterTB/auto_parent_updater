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

    # If there are no (valid) credentials available, let the user log in.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run

    with open("token.json", "w") as token:
        token.write(creds.to_json())
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])


    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

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




account_sid = ''
auth_token = ''


# gets emails in CS2_emails.txt


def call_function(p_course):
    RANGE_NAME = ""
    remove_list = []
    replace_dict = {}

    if p_course == "CS2":
        RANGE_NAME = "CS2!A2:E"
        remove_list = ["Headers", "Paragraphs", "Ordered lists", "Unordered lists", "Google classroom setup",
               "CS2 Schedule + Calendar", "CRLS Bell Schedule + Year in review", "Lunch times", "Course contract",
               "Day 1 survey", "Course contract Acknowledgement", "HTML2", "Line break",
               "Story of self + I want my teacher to know", "Go over autograding HTML1", "Section break", "strong",
               "em", "How to look something up", "Boilerplate", "Emojis", "Background color", "Font size", "Font color",
               "Font family", "CSS1"]
        replace_dict = {"Go over autograding HTML1": "Learning how to autograde!", "HTML1": "we learned hmtl!",
                "Introductions (names)": "Introductions, Icebreakers, Logistics",
                "blockquote": "Learned How to Autograde and Expanded on the Basics of HTML",
                "Show Jack Fede's site with/without CSS https://replit.com/@ericwu/2022jfedeCS2#index.html (uncomment the css link)": "Analyzed an Example Website", "work day": "project work"}
    elif p_course == "CS3":
        RANGE_NAME = "CS3!A2:E"
        remove_list = []
        replace_dict = {}
    return RANGE_NAME, remove_list, replace_dict

def reFormat_email(course):
    with open(course + "_emails.txt") as file:
        lines = file.readlines()
        num_lines = len(lines) - 1
        for i in range(num_lines):
            lines[i] = lines[i].strip()
            # lines.replace(i, i.strip())
        return lines


def reFormat_phone(course):
    with open(course + "_phone_numbers.txt") as file:
        lines = file.readlines()
        num_lines = len(lines) - 1
        for i in range(num_lines):
            lines[i] = lines[i].strip()
            # lines.replace(i, i.strip())
        return lines
current_courses = ["CS2", "CS3"]

for course in current_courses:


    RANGE_NAME = call_function(course)[0]
    remove_list = call_function(course)[1]
    replace_dict = call_function(course)[2]
    message_content = assignment_filter(remove_list, replace_dict, sheet(sheet_date(RANGE_NAME), RANGE_NAME),course)
    gmail_list = reFormat_email(course)
    print(message_content)
    phone_list = reFormat_phone(course)
    if __name__ == "__main__":
        gmail_send_message(main(), gmail_list, message_content)
        Twilio(account_sid, auth_token, phone_list, message_content)


