import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("your_credentials.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Your Google Sheet Name").sheet1

def push_impact_event(timestamp, intensity, event_type):
    try:
        sheet.append_row([timestamp, float(intensity), str(event_type).lower()])
        print(f" Successfully logged: {event_type} ({intensity} Gs) at {timestamp}")
    except Exception as e:
        print(f"Error pushing data to sheet: {e}")

if __name__ == "__main__":
    print("Simulating Codey Rocky impact tracking...")
    push_impact_event("14:22:05", 2.93, "roll")
    time.sleep(1)
    push_impact_event("14:22:12", 3.16, "toss")
    time.sleep(1)
    push_impact_event("14:22:31", 8.36, "drop")
