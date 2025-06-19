import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
# Setup
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("YOUR-CREDENTIALS.json", scope)
client = gspread.authorize(creds)

sheet = client.spreadsheet = client.open_by_key("18FoNALG1RT3KM6ELf4YBUm7itlwS7htp1zBm3neI4ew").sheet1

last_row = None
try:
    while True:
        data = sheet.get_all_values()
        if len(data) > 1 and data[-1] != last_row:
            print(data)
            last_row = data[-1]
        time.sleep(0)
except Exception as e:
    pass
