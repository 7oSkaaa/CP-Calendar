from __future__ import print_function
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from helpers.colors import bcolors

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

def get_credentials():
    creds = None
    SCOPES = [
          'https://www.googleapis.com/auth/calendar', 
          'https://www.googleapis.com/auth/calendar.events', 
          'https://www.googleapis.com/auth/calendar.events.readonly',  
          'https://www.googleapis.com/auth/calendar.readonly'
    ]
    
    #Get the directory of current folder
    directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(directory)
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid or creds.expired:
        if not creds or creds.expired or not creds.refresh_token:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def make_events(contests):
    
    creds = get_credentials()
        
    for contest in contests:
        event = make_event(contest)
        try:
            service = build('calendar', 'v3', credentials=creds)
            # Call the Calendar API
            service.events().insert(calendarId='primary', body=event).execute()
            print(f"{bcolors.green}Event created: {contest['name']} ???{bcolors.reset}")
        except HttpError as error:
            if  error.resp.status == 409:
                # if the event already created just update it
                service.events().update(calendarId='primary', eventId=contest['ID'], body=event).execute()
                print(f"{bcolors.gold}Event updated: {contest['name']} ???{bcolors.reset}")
            else:
                # Print error messages
                for e in error.error_details:  
                    print(f"{bcolors.red}{e['message']} at {contest['name']} ???{bcolors.reset}")