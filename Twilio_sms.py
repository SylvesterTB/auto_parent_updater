from twilio.rest import Client
from sheets import assignment_filter, sheet


account_sid = 'ACe3a7440701bd6a3bdff8a5df9aa8afc5'
auth_token = 'ba728f474ed29dbff1a3c48450934cc8'
client = Client(account_sid, auth_token)

contact_list = ["+18572851771", "+16174178395"]

len(contact_list)
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


message_content = assignment_filter(remove_list, replace_dict, sheet())
for i in range(len(contact_list)):

    message = client.messages.create(
      from_='+18882048606',
      body= message_content,
      to = contact_list[i]
    )
    print(message.sid)

    # commit fix? a