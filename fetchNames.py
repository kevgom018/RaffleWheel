import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Setup
def get_participants(sheet_url):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1
    names = sheet.col_values(3)[1:] # Names are in third column
    amt = sheet.col_values(5)[1:] # Amounts are in fifth colummn
    return names, amt

def main():
    url_file = open("sheet_url.txt", "r")
    SHEET_URL = url_file.readline().strip()
    url_file.close()
    
    participants, amt = get_participants(SHEET_URL)
    output = []
    for i in range(len((participants))):
        output.append(participants[i] + " " + amt[i] + "\n")
    output.sort()

    file = open("participants.txt", "w")
    for participant in output:
        file.write(participant)
    file.close()

if __name__ == "__main__":
    main()