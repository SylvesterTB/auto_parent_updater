import smtplib
from email.mime.multipart import MIMEMultipart
import csv



message = MIMEMultipart("word") 

words = 'these are words'
my_email = '25sbroich@cpsd.us'
password_key = 'sbandvb912'

# SMTP Server and port no for GMAIL.com
gmail_server = "smtp.gmail.com"
gmail_port = 587

# Starting connection
my_server = smtplib.SMTP(gmail_server, gmail_port)
my_server.ehlo()
my_server.starttls()

# Login with your email and password
my_server.login(my_email, password_key)

message.attach(MIMEText(words))


gmail_list = ['syltester616@gmail.com', 'sylvester.broich@gmail.com']

my_server.sendmail(from_addr=my_email,
                   to_addrs = gmail_list,
                   msg=words)

my_server.quit()
