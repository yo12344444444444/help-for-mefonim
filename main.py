import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

# Setup
scope = ["https://docs.google.com/spreadsheets/d/18FoNALG1RT3KM6ELf4YBUm7itlwS7htp1zBm3neI4ew/edit?resourcekey=&gid=1509355680#gid=1509355680", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("YOUR-CREDENTIALS.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Your Sheet Name").sheet1

last_row = None

while True:
    data = sheet.get_all_values()
    if len(data) > 1 and data[-1] != last_row:
        print("New number:", data[-1][0])
        last_row = data[-1]
    time.sleep(10)
