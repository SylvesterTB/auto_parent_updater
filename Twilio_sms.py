from twilio.rest import Client

account_sid = 'ACe3a7440701bd6a3bdff8a5df9aa8afc5'
auth_token = 'ba728f474ed29dbff1a3c48450934cc8'
client = Client(account_sid, auth_token)

contact_list = ["+18572851771", "+16174178395"]

len(contact_list)

for i in range(len(contact_list)):

    message = client.messages.create(
      from_='+18882048606',
      body='Hello from Twilio',
      to = contact_list[i]
    )
    print(message.sid)