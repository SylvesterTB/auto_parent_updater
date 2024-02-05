from twilio.rest import Client

account_sid = 'ACe3a7440701bd6a3bdff8a5df9aa8afc5'
auth_token = '8da33ca5088bca20316f480d19d106f0'
client = Client(account_sid, auth_token)

contact_list = ["+18572851771", "+16174178395"]

len(contact_list)
number = 0

for i in range(len(contact_list)):

    message = client.messages.create(
      from_='+18882048606',
      body='Hello from Twilio',
      to = contact_list[i]
    )
    number += 1 
    print(message.sid)