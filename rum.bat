@echo off
pip install gspread oauth2client pyinstaller
pyinstaller --onefile --add-data "YOUR-CREDENTIALS.json;." main.py
pause
