from twilio.rest import Client

# Authorization for the Twilio account in Sylvesters possesion 
account_sid = 'ACe3a7440701bd6a3bdff8a5df9aa8afc5'
auth_token = '8da33ca5088bca20316f480d19d106f0'
client = Client(account_sid, auth_token)

# Example contact list, substitute in actual phone number when using  
contact_list = ["+18572851771", "+16174178395"]

# prepping to loop through each contact in contact_list
len(contact_list)

# Loops through all contacts in contact_list
for i in range(len(contact_list)):


    message = client.messages.create(
      # number sending the message, provided by Twilio 
      from_='+18882048606',
      # message content
      body='Hello from Twilio',
      to = contact_list[i]
    )
  
    print(message.sid)