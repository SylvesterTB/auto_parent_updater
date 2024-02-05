import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.addons.current.action.compose", "https://www.googleapis.com/auth/gmail.compose"]


def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
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
    with open("token.json", "w") as token:
      token.write(creds.to_json())

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
      print(label["name"])

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()

#######################################################################################################
  
gmail_list = ['syltester616@gmail.com', 'sylvester.broich@gmail.com', '25sbroich@cpsd.us']

messages = []

# def auto_emailer( p_config_filename, p_gc_name, p_send_email=False,
#                                p_teachercc='', p_message='', p_scholar_guardians=''):



               
def gmail_create_draft():
  print('hello')
#   """Create and insert a draft email.
#    Print the returned draft's message and id.
#    Returns: Draft object, including draft id and message meta data.

#   Load pre-authorized user credentials from the environment.
#   TODO(developer) - See https://developers.google.com/identity
#   for guides on implementing OAuth2 for the application.
#   """
creds, _ = google.auth.default()

try:
    # create gmail api client
    service = build("gmail", "v1", credentials=creds)

    message = EmailMessage()

    message.set_content("This is automated draft mail")

    message["To"] = 'sylvester.broich@gmail.com'
    message["From"] = 'syltester616@gmail.com'
    message["Subject"] = "Automated draft"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"message": {"raw": encoded_message}}
    # pylint: disable=E1101
    draft = (
        service.users()
        .drafts()
        .create(userId="me", body=create_message)
        .execute()
    )

    print(f'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

except HttpError as error:
    print(f"An error occurred: {error}")
    draft = None

    # return draft


if __name__ == "__main__":
  gmail_create_draft()

            # Debug info here
            # if email_address in p_scholar_guardians.keys():
            #     print("Email address to send to: " + email_address + ',' +
            #           p_scholar_guardians[email_address])
            # else:
            #     print("Email address to send to: " + email_address)
            # if p_teachercc:
            #     print("teacher cc: " + str(p_teachercc))
            # else:
            #     print("no teacher cc")
            # print("This is the message that will be/would have been sent:")
            # print(message[key])
            # msg_text = message[key]

            # if p_send_email:
            #     email_message = MIMEMultipart()
            #     if email_address in p_scholar_guardians.keys():
            #         email_message['to'] = email_address + ',' + p_scholar_guardians[email_address]
            #     else:
            #         email_message['to'] = email_address
            #     if p_teachercc:
            #         email_message['cc'] = p_teachercc
            #     email_message['subject'] = p_gc_name + '  assignments report'
            #     email_message.attach(MIMEText(msg_text, 'plain'))
            #     raw_string = base64.urlsafe_b64encode(email_message.as_bytes()).decode()
            #     send_message = service_gmail.users().messages().send(userId='me', body={'raw': raw_string}).execute()
            #     print(send_message)
            # else:
            #     print("send_message was sent to 0.  Emails were not sent.\n"
            #           "To send emails, switch send_email to 1 in this file: " + str(p_config_filename) + "\n\n")
