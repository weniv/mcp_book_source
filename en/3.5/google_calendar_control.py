import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

TOKEN_PATH = "c:\\test\\token.json"
CREDS_PATH = "c:\\test\\credentials.json"


def get_credentials():
    """Handle Google Calendar API authentication"""
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return creds


def print_upcoming_events():
    """Print the upcoming 10 events"""
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        print("Getting the upcoming 10 events")
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            print("No upcoming events found.")
            return

        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            print(start, event["summary"])

    except HttpError as error:
        print(f"An error occurred: {error}")


def add_vacation_event(title: str, start_date: str, end_date: str):
    """
    Add vacation event to Google Calendar
    - start_date, end_date in 'YYYY-MM-DD' format
    """
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": title,
            "start": {"date": start_date},
            "end": {"date": end_date},  # Last day +1 is automatically interpreted
        }

        created_event = (
            service.events().insert(calendarId="primary", body=event).execute()
        )
        print(f"Vacation '{title}' has been registered. ID: {created_event.get('id')}")

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    # Example: Register vacation
    add_vacation_event("Vacation", "2025-04-10", "2025-04-13")
    # Check schedule
    print_upcoming_events()
