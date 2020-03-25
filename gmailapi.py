from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
import csv
import sys

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text,'html')
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service, user_id, to, name):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=create_message("Ankit Gupta", to, "Python and Web Development Workshop", u'Dear '+name+', <p>Thank you for registering for my workshop! I can\'t wait for it to start and I\'m sure you can\'t either!</p><p> Join me on whatsapp for all further announcements and to decide the schedule. I will also be sharing reference material for the workshop on this group. Reply back to this email if you are unable to use the link or do not have whatsapp. </p><p><a href="https://chat.whatsapp.com/Du5zp5LX692Gdo3pmyxHZj">https://chat.whatsapp.com/Du5zp5LX692Gdo3pmyxHZj</a></p><p>Regards,<br>Ankit Gupta<br>+919833482539</p>'))
               .execute())
    print('Message Id: %s sent from %s to %s' % (message['id'], user_id, to))
    return message
  except Exception as error:
    print('An error occurred: %s' % error)

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    data = []
    if not len(sys.argv)>1:
      fname = "workshop.csv"
    else:
      fname = sys.argv[1]
    with open(fname) as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)[1:]

    for row in data:
      send_message(service, "argankit@gmail.com", row[1], row[2].split()[0])



    # Call the Gmail API
    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])

    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels:')
    #     for label in labels:
    #         print(label['name'])

if __name__ == '__main__':
    main()