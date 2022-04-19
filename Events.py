from __future__ import print_function
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#Colors to use
red = '\033[38;5;196m'
green = '\033[38;5;40m'
blue = '\033[34m'
gold = '\033[38;5;220m'
white = '\33[37m'
magenta = '\033[35m'
bold = '\033[01m'
reset = '\033[0m'

def make_event(contest):
    # event body to use
    event = {
        'summary': contest['name'],
        'description': f"Registration Link: {contest['url']}",
        "id": contest['ID'],
        'start': {
            'dateTime': contest['start_time'],
            'timeZone': 'Africa/Cairo',
        },
        'end': {
            'dateTime': contest['end_time'],
            'timeZone': 'Africa/Cairo',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30},
                {'method': 'popup', 'minutes': 60 * 24},
            ],
        },
    }
    return event


def make_events(contests):
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/calendar', 
          'https://www.googleapis.com/auth/calendar.events', 
          'https://www.googleapis.com/auth/calendar.events.readonly',  
          'https://www.googleapis.com/auth/calendar.readonly'
    ]
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    for contest in contests:
        event = make_event(contest)
        try:
            service = build('calendar', 'v3', credentials=creds)
            # Call the Calendar API
            service.events().insert(calendarId='primary', body=event).execute()
            print(f"{green}Event created: {contest['name']} at {contest['start_time']} ✅{reset}")
        except HttpError as error:
            # if the event already created just update it
            if  error.resp.status == 409:
                service.events().update(calendarId='primary', eventId=contest['ID'], body=event).execute()
                print(f"{gold}Event updated: {contest['name']} ✅{reset}")
                