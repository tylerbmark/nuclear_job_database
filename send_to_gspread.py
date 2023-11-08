import gspread
from google.oauth2.credentials import Credentials
import pandas as pd
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
SCOPES=['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID='1ceaF-h6sflCJAfwCDBvrAmjnN3MBVQef'
SAMPLE_RANGE_NAME='Engie'
def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    return values
def write():
	excel_data=pd.read_excel('data.xlsx')
	creds= Credentials.from_authorized_user_file('token.json',SCOPES)
	service=build('sheets','v4',credentials=creds)
	body={
		'values':[excel_data.columns.values.tolist()]+excel_data.values.tolist()

	}
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=SAMPLE_RANGE_NAME).execute()
	values = result.get('values', [])
	print(values)
	#result=service.spreadsheets().values().update(
	#	spreadsheetId=SAMPLE_SPREADSHEET_ID, range=0,
	#	valueInputOption='RAW',body=body).execute()
	return
#gc=gspread.authorize(creds)
#sheet=gc.open_by_url('https://docs.google.com/spreadsheets/d/1ceaF-h6sflCJAfwCDBvrAmjnN3MBVQef')
#worksheet=sheet.get_worksheet(0)
#excel_data=pd.read_excel('data.xlsx')
#worksheet.update([excel_data.columns.values.tolist()]+excel_data.values.tolist())
#main()

write()
