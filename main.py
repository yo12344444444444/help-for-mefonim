import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tkinter as tk
from tkinter import messagebox
from collections import Counter

# === Google Sheets Setup ===
# Setup
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("YOUR-CREDENTIALS.json", scope)
client = gspread.authorize(creds)

active_sheet = client.spreadsheet = client.open_by_key("18FoNALG1RT3KM6ELf4YBUm7itlwS7htp1zBm3neI4ew").sheet1
new_loc_sheet  = client.spreadsheet = client.open_by_key("1Kb2mY9XN9vmfWuuP2_1fW7LUUnU_peEzaaAstMW5w1U").sheet1

# === GUI Setup ===
root = tk.Tk()
root.title("📍 Help Location Dashboard")
root.geometry("1000x600")

# === New Suggestions (LEFT) ===
tk.Label(root, text="🆕 New Locations (help location)", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
new_listbox = tk.Listbox(root, width=45, height=25)
new_listbox.grid(row=1, column=0, padx=10)

def refresh_new_locations():
    new_listbox.delete(0, tk.END)
    try:
        rows = new_loc_sheet.get_all_values()
        locations = [row[1].strip() for row in rows if row]
        unique = Counter(locations)
        for loc, count in unique.items():
            new_listbox.insert(tk.END, f"{loc} ({count})")
    except Exception as e:
        new_listbox.insert(tk.END, f"❌ Error: {e}")

def delete_new_location():
    try:
        selected = new_listbox.get(new_listbox.curselection())
        loc = selected.split(" (")[0]
        all_rows = new_loc_sheet.get_all_values()
        rows_to_delete = [i for i, row in enumerate(all_rows) if row and row[0].strip() == loc]
        for i in reversed(rows_to_delete):
            new_loc_sheet.delete_rows(i + 1)
        messagebox.showinfo("Deleted", f"Deleted new location: {loc}")
        refresh_new_locations()
    except Exception as e:
        messagebox.showerror("Error", f"Could not delete: {e}")

tk.Button(root, text="🗑 Delete New Location", command=delete_new_location).grid(row=2, column=0, pady=10)

# === Existing Locations (RIGHT) ===
tk.Label(root, text="📍 Existing Location Reports (help)", font=("Arial", 14)).grid(row=0, column=1, padx=10, pady=5)
known_listbox = tk.Listbox(root, width=45, height=25)
known_listbox.grid(row=1, column=1, padx=10)

def refresh_known_locations():
    known_listbox.delete(0, tk.END)
    try:
        rows = active_sheet.get_all_values()
        locations = [row[1].strip() for row in rows if row]
        grouped = Counter(locations)
        for loc, count in grouped.items():
            known_listbox.insert(tk.END, f"{loc} ({count})")
    except Exception as e:
        known_listbox.insert(tk.END, f"❌ Error: {e}")

def delete_known_group():
    try:
        selected = known_listbox.get(known_listbox.curselection())
        loc = selected.split(" (")[0]
        all_rows = active_sheet.get_all_values()
        rows_to_delete = [i for i, row in enumerate(all_rows) if row and row[0].strip() == loc]
        for i in reversed(rows_to_delete):
            active_sheet.delete_rows(i + 1)
        messagebox.showinfo("Deleted", f"Deleted all entries for: {loc}")
        refresh_known_locations()
    except Exception as e:
        messagebox.showerror("Error", f"Could not delete: {e}")

tk.Button(root, text="🗑 Delete Group from Known Locations", command=delete_known_group).grid(row=2, column=1, pady=10)

# === Refresh Both Lists Automatically ===
def refresh_all():
    refresh_new_locations()
    refresh_known_locations()
    root.after(3000, refresh_all)

refresh_all()
root.mainloop()
