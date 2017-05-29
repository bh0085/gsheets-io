#!/usr/bin/env python

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import calendar, json, re, os


#connects to google spreadsheets
def connect(sheet):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('google-key.json', scope)
    client = gspread.authorize(creds)
    
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open_by_key(sheet)

    return sheet


def main(sheet,name):
    sheet = connect(sheet)
    worksheet = sheet.worksheet(name)
    cells = worksheet.get_all_records(empty2zero=False, head=1, default_blank='')
    print json.dumps(cells)

    
if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--sheet', help='sheet key', default="1BpydUa4pcwheZ1YISK3Kbw9Pt2rFKnEzyiqIDtC-CCQ")
    parser.add_argument('--name', help='sheet name', default="IMPORT Cellar Logs")
        
    args = parser.parse_args()
    main(args.sheet, args.name)
