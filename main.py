# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 11:41:09 2016

@author: Vincent_Wu
"""

import stockquote
import plot,scan_list
from Tkinter import *
import unicodecsv,os

from datetime import datetime,timedelta

def read_csv(filename):
    with open(filename, 'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)

def write_csv(filename,fieldnames):
    with open(filename, 'w') as f:
        reader = unicodecsv.DictWriter(f,fieldnames=fieldnames)
        reader.writeheader()
        return reader

def get_symbol_list(data):
    temp = set()
    for dp in data:
        temp.add(dp['Symbol'])
    return temp

def show_ui(symbol,start_date,end_date):
    h = list(stockquote.historical_quotes(symbol, start_date, end_date))
    plot.plot_ui(h)
    print symbol

def scan_all_list(start_date,end_date):
    #Init symbol_list
    symbol_list = list()

    f = open('companylist.csv', 'r')
    for row in csv.DictReader(f):
        symbol_list.append(row['Symbol']) #Get Symbol List
    f.close()

    #Save Data
    save_path = os.getcwd()

    for index in symbol_list:
        dict_url = os.path.join(save_path,'data\\%s.csv' % index)
        csvfile = open(dict_url, 'w')
        fieldnames = ['Date', 'High','Low','Close','K val','D val']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        k = list(stockquote.historical_quotes(index, start_date, end_date))
        plot.save_data(k,writer)
    print "Scan Completed"
    
    #Append Daily check
    scan_list.scan_list_find_point()

if __name__ == "__main__":

# Definition
    COMP_LIST = "companylist.csv"
    DEFAULTVALUE_OPTION = "Select stock for analysis :"
    DEFAULTVALUE_START_DATE = ""
    DEFAULTVALUE_END_DATE = ""
    global SELECT_VALUE
    SELECT_VALUE = ""
# Initialization
    root = Tk()
    root.title("Stock Analysis v1.0")
    root.grid()
    
#Read list from file
    comp_csv = read_csv(COMP_LIST)
    symbol_list = get_symbol_list(comp_csv)
    
#Create UI Component
    label1 = Label(root)
    label1["text"] = "Symbol:"
    label1.grid(row=0, column=0)
    
    defaultOption=StringVar()

    #optionMenuWidget = apply(OptionMenu, (root, defaultOption) + tuple(symbol_list))
    optionMenuWidget=OptionMenu(root, defaultOption, *symbol_list)
    defaultOption.set(DEFAULTVALUE_OPTION)
    optionMenuWidget["width"] = 50
    optionMenuWidget.grid(row=0, column=1, columnspan=10)
    #optionMenuWidget.pack(side=LEFT)

    label2 = Label(root)
    label2["text"] = "Start Date:"
    label2.grid(row=1, column=0)
    
    default_start_date= datetime.now() - timedelta(days=100)
    start_inputField = Entry(root)
    start_inputField.insert(END, default_start_date.strftime("%Y%m%d"))
    start_inputField["width"] = 50
    start_inputField.grid(row=1, column=1, columnspan=10)

    label3 = Label(root)
    label3["text"] = "End Date:"
    label3.grid(row=2, column=0)
    
    default_end_date = datetime.now()
    end_inputField = Entry(root)
    end_inputField.insert(END, default_end_date.strftime("%Y%m%d"))
    end_inputField["width"] = 50
    end_inputField.grid(row=2, column=1, columnspan=10)
    
    plot_btn = Button()
    plot_btn['text'] = "GO"
    plot_btn['command'] = lambda: show_ui(defaultOption.get(),start_inputField.get(),end_inputField.get())
    plot_btn.grid(row=3,column = 4)
    #scan_btn.pack()
    
    scan_btn = Button()
    scan_btn['text'] = "Scan"
    scan_btn['command'] = lambda: scan_all_list(start_inputField.get(),end_inputField.get())
    scan_btn.grid(row=3,column = 6)
    
    scan_daily_btn = Button()
    scan_daily_btn['text'] = "Daily Judge"
    scan_daily_btn['command'] = lambda: scan_list.scan_list_find_point()
    scan_daily_btn.grid(row=3,column = 8)
    
    
    root.mainloop()
