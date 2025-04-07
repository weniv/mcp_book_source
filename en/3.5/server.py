from mcp.server.fastmcp import FastMCP

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ✅ Changed to calendar write permission
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Create MCP server
mcp = FastMCP(name="server", timeout=3000)


def get_credentials():
    """Handle Google Calendar API authentication"""
    creds = None
    token_path = "c:\\test\\token.json"
    creds_path = "c:\\test\\credentials.json"

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    return creds


@mcp.tool()
async def get_upcoming_schedule() -> list:
    """Return the upcoming 10 events"""
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
            return "No upcoming events found."

        result = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            result.append([start, event["summary"]])
        return result

    except HttpError as error:
        return [f"An error occurred: {error}"]


# ✅ Added vacation registration function
@mcp.tool()
async def add_vacation_schedule(title: str, start_date: str, end_date: str) -> str:
    """
    Register vacation schedule in Google Calendar.
    - title: Schedule title (e.g. 'Vacation')
    - start_date, end_date: 'YYYY-MM-DD' format
    """
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": title,
            "start": {"date": start_date},
            "end": {
                "date": end_date
            },  # End date should be last vacation day + 1 for accurate input
        }

        service.events().insert(calendarId="primary", body=event).execute()
        return f"'{title}' vacation schedule has been registered from {start_date} to {end_date}."

    except HttpError as error:
        return f"An error occurred: {error}"


if __name__ == "__main__":
    mcp.run()
