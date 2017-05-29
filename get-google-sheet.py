#!/usr/bin/env python

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import calendar, json, re, os
import sqlite3


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


def print_json(sheet,name,filename):
    cells = get_cells(sheet,name)
    if not filename:
        print json.dumps(cells)
    else:
        with open(filename,"w") as f:
            f.write(json.dumps(cells))

def get_cells(sheet,name):
    sheet = connect(sheet)
    worksheet = sheet.worksheet(name)
    cells = worksheet.get_all_records(empty2zero=False, head=1, default_blank='')
    return cells

from sqlalchemy import Table, Column, Integer, Unicode, MetaData, create_engine
from sqlalchemy.orm import mapper, create_session

class Row(object):
    pass

def store_sqlite(data,outfile, header_rows = 2, cols = None, types = None):
  engine = create_engine('sqlite:///'+outfile)
    metadata = MetaData(bind=engine)

    t = Table('rows', metadata,
              Column('id', Integer, primary_key=True),
              *(Column(c, Unicode(255)) for c in cols))

    metadata.drop_all(engine)
    metadata.create_all(engine)
    mapper(Row, t)
    
    session = create_session(bind=engine, autocommit=False, autoflush=True)

    for j,e in enumerate(data):
        if j < header_rows: continue
        
        r = Row()
        for i,c in enumerate(cols):
            setattr(r,c,e[c])
        session.add(r)

    session.commit()
    
    
if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()

    
    parser.add_argument('outfile', metavar='O', nargs='?', help='output file name')
    
    parser.add_argument('--sqlite', default=False, action="store_const", const=True)

    parser.add_argument('--sheet', help='sheet key', default="1WWOD92D7SvCVh2Hlu-0dyyuIOctn7UMVMSOPoFBbGgI")
    parser.add_argument('--name', help='sheet name', default="INFO")

    parser.add_argument('--header-rows',help='n header rows', type=int, default = 2)
    parser.add_argument('--cols-row',dest ="c_row", default =0, help="row containing column names", type=int)
    parser.add_argument('--types-row',dest="t_row",default =1, help="row containing column types", type=int)
    
                 
    
    args = parser.parse_args()

    if args.sqlite:
        cells =get_cells(args.sheet, args.name)
        cols = cells[args.c_row]
        types = cells[args.t_row]
        
        store_sqlite(cells,
                     args.outfile,
                     cols = cols,
                     types = types)
        
    else:
        print_json(args.sheet, args.name, args.outfile)
