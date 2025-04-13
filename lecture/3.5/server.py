from mcp.server.fastmcp import FastMCP

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ✅ 캘린더 쓰기 권한으로 변경
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# MCP 서버 생성
mcp = FastMCP(name="server", timeout=3000)


def get_credentials():
    """Google Calendar API 인증 처리"""
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
    """다가오는 10개의 일정을 반환"""
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


# ✅ 휴가 등록 함수 추가
@mcp.tool()
async def add_vacation_schedule(title: str, start_date: str, end_date: str) -> str:
    """
    Google Calendar에 휴가 일정을 등록합니다.
    - title: 일정 제목 (예: '휴가')
    - start_date, end_date: 'YYYY-MM-DD' 형식
    """
    try:
        creds = get_credentials()
        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": title,
            "start": {"date": start_date},
            "end": {
                "date": end_date
            },  # 종료일은 휴가 마지막 날 + 1일이어야 정확히 들어감
        }

        service.events().insert(calendarId="primary", body=event).execute()
        return f"'{title}' 휴가 일정이 {start_date}부터 {end_date}까지 등록되었습니다."

    except HttpError as error:
        return f"An error occurred: {error}"


if __name__ == "__main__":
    mcp.run()
