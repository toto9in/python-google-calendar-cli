from datetime import datetime, timezone, timedelta
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_credentials():
   creds = None
   if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
      return creds
    # If there are no (valid) credentials available, let the user log in.
   if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
      return creds
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
      token.write(creds.to_json())
    return creds
    
  

def get_events(filter: str = "today"):
  creds = get_credentials()
  if filter == "today":
    events = list_events_today(creds)
    if not events:
      return None
    return events

  if filter == "week":
    events = list_events_week(creds)
    if not events:
      return None
    return events
    
  

def list_events_week(credentials):
  date_now = datetime.now(timezone.utc).astimezone()
  week_day = date_now.weekday()
  start_date = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
  start_date = start_date - timedelta(days=week_day)
  end_date = start_date + timedelta(days=7, seconds=-1)
  try:
    service = build("calendar", "v3", credentials=credentials)
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_date.isoformat(),
            timeMax=end_date.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    if not events:
      return None
    return events
  except HttpError as error:
    print(f"An error occurred: {error}")

def list_events_today(credentials):
  date_now = datetime.now(timezone.utc).astimezone()
  start_date = date_now.replace(hour=0, minute=0, second=0, microsecond=0)
  end_date = start_date + timedelta(days=1, seconds=-1)
  try:
    service = build("calendar", "v3", credentials=credentials)
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_date.isoformat(),
            timeMax=end_date.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])
    if not events:
      return None
    return events
  except HttpError as error:
    print(f"An error occurred: {error}")
  
def create_events(
    event_name: str,
    start_date_time: str,
    end_date_time: str,
    description: str ,
):
  creds = get_credentials()
  service = build("calendar", "v3", credentials=creds)
  time_zone = get_time_zone()
  if time_zone is None:
    print("Time zone not found.")
    return
  event = {
    "summary": event_name,
    "start": {"dateTime": start_date_time, "timeZone": get_time_zone()},
    "end": {"dateTime": end_date_time , "timeZone": get_time_zone()},
  }
  if description != "":
    event["description"] = description



  event = service.events().insert(calendarId='primary', body=event).execute()
  print(f"Event created with name: {event.get('summary')} and start date: {event.get('start').get('dateTime')}")

##preciso ver um jeito de pegar os dados do user quando ele se authenticar para pegar info como timezone etc

def get_time_zone():
  creds = get_credentials()
  service = build("calendar", "v3", credentials=creds)
  settings = service.settings().list().execute()
  for setting in settings['items']:
    if setting['id'] == 'timezone':
      return setting['value']
  return None



if __name__ == "__main__":
   print("pacote calendar_utils")
