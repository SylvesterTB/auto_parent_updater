from twilio.rest import Client
from sheets import assignment_filter, sheet

def Twilio(p_account_sid, p_auth_token, p_contact_list, p_message_content):
    client = Client(p_account_sid, p_auth_token)
    for i in range(len(p_contact_list)):

        message = client.messages.create(
          from_='+18882048606',
          body= p_message_content,
          to = p_contact_list[i]
        )
        print(message.sid)




