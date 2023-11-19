import gspread
from google.oauth2.credentials import Credentials
import pandas as pd
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SAMPLE_SPREADSHEET_ID = "11NKQs2Bd_1fu8dV_71a9GkMuTVXIpOfTC2ipfn2DJI8"
SCOPES=['https://www.googleapis.com/auth/spreadsheets',
        # 'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive',]
        # 'https://www.googleapis.com/auth/drive.file'
        # F'https://sheets.googleapis.com/v4/spreadsheets/{SAMPLE_SPREADSHEET_ID}:batchUpdate']
SAMPLE_RANGE_NAME = "Sheet1"

def main():
  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials_2.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    # service.files().copy(fileId=SAMPLE_SPREADSHEET_ID,convert=True,body={'title':'specifyName'}).execute()
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])
    print(values)
    if not values:
      print("No data found.")
      return

    # print("Name, Major:")
    # for row in values:
    #   # Print columns A and E, which correspond to indices 0 and 4.
    #   print(f"{row[0]}, {row[4]}")
  except HttpError as err:
    print(err)
  return
def write():
  sheet_names=pd.ExcelFile('data.xlsx').sheet_names
  creds= Credentials.from_authorized_user_file('token.json',SCOPES)
  service=build('sheets','v4',credentials=creds)
  for name_i,sheet_name in enumerate(sheet_names):
    excel_data=pd.read_excel('data.xlsx',sheet_name=sheet_name)
    body={
  	  'values':[excel_data.columns.values.tolist()]+excel_data.values.tolist()
      }
    result=service.spreadsheets().values().update(
    	spreadsheetId=SAMPLE_SPREADSHEET_ID, range=sheet_name,
    	valueInputOption='RAW',body=body).execute()
  return
# if os.path.exists("token.json"):
#     creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# gc=gspread.authorize(creds)
# sheet=gc.open_by_url('https://docs.google.com/spreadsheets/d/11NKQs2Bd_1fu8dV_71a9GkMuTVXIpOfTC2ipfn2DJI8/edit#gid=0')
# worksheet=sheet.get_worksheet(0)
# excel_data=pd.read_excel('data.xlsx')
# worksheet.update([excel_data.columns.values.tolist()]+excel_data.values.tolist())
# main()
write()
# write()
