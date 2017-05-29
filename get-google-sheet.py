#!/usr/bin/env python

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import calendar, json, re, os
import sqlite3
import sqlalchemy
import dateparser


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

from sqlalchemy import Table, Column, Integer, Unicode, Date, Numeric, MetaData, create_engine
from sqlalchemy.orm import mapper, create_session

class Row(object):
    pass

def store_sqlite(data,outfile, header_rows = 1, cols = None, types = None, indexes=None,tablename=None):
    engine = create_engine('sqlite:///'+outfile)
    metadata = MetaData(bind=engine)

    types_map = {
        "text": Unicode(255),
        "number": Numeric(),
        "date":Date()
    }

    
    t =Table(tablename if tablename else 'rows', metadata,
             Column('id', Integer, primary_key = True),
             *(Column(c,
                      types_map.get(types[c],Unicode(255))  if types else Unicode(255),
                      index=True if indexes and indexes[c]==1 else False)
               for c in cols))


    try:
        t.drop()
    except sqlalchemy.exc.OperationalError as err:
        print err
        print "continuing"
    t.create()
    
    mapper(Row, t)
    session = create_session(bind=engine, autocommit=False, autoflush=True)
    for j,e in enumerate(data):
        if j < (header_rows - 1): continue
        
        r = Row()
        for i,c in enumerate(cols):
            setattr(r,c,dateparser.parse( e[c]) if types and types[c] == "date" else e[c] )
        session.add(r)

    session.commit()
    
    
if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--output, -o', dest="output", required=True, help='output file')
    parser.add_argument('--sqlite', default=True, action="store_const", const=True, help="create a sqlite database instead of a flat file")
    parser.add_argument('--sheet, -s', dest="sheet",help='google spreadsheet workbook key', default="1WWOD92D7SvCVh2Hlu-0dyyuIOctn7UMVMSOPoFBbGgI")
    parser.add_argument('--name, -n', dest="name", help='google speadsheet page name', default="DATABASE")
    parser.add_argument('--header-rows',dest="h_rows", help='n header rows', type=int, default = 2)
    parser.add_argument('--cols-row',dest ="c_row", default =0, help="[SQLITE3] row containing column names", type=int)
    parser.add_argument('--types-row',dest="t_row",default=None, help="[SQLITE3] row containing column types", type=int)
    parser.add_argument('--index-row',dest="i_row",default=None, help="[SQLITE3] row containing binary values for whether or not to create an sqlite index", type=int)
    parser.add_argument('--table -t',dest="tablename",default ="rows", help="[SQLITE3] specify a table name for", type=str)
 
    args = parser.parse_args()

    if args.sqlite:
        cells =get_cells(args.sheet, args.name)
        #cols = cells[args.c_row] if args.c_row != None else None
        cols=cells[0].keys()
        types = cells[args.t_row -2] if args.t_row else None
        indexes = cells[args.i_row -2] if args.i_row else None

        print types
        print indexes
 
        store_sqlite(cells,
                     args.output,
                     cols = cols,
                     indexes = indexes,
                     types = types,
                     header_rows=args.h_rows,
                     tablename = args.tablename)
        
    else:
        print_json(args.sheet, args.name, args.outfile)
