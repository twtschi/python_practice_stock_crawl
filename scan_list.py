# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 15:45:01 2016

@author: Vincent_Wu
"""
import main,os,csv
from datetime import datetime,timedelta

def scan_list_find_point():
#if __name__ == "__main__":
    COMP_LIST  = "companylist.csv"
    curr_path  = os.getcwd()
    today_date = datetime.now()
    save_path  = os.path.join(curr_path,'data_point\\%s.csv' % today_date.strftime("%Y%m%d"))
    write_header =  ['Date','Symbol', 'K val','D val','Buy','Sell']


    comp_csv = main.read_csv(COMP_LIST)
    symbol_list = main.get_symbol_list(comp_csv)
    
#    _write_file = main.write_csv(save_path,write_header)
    _write_file = open(save_path, 'w')
    _write_handler = csv.DictWriter(_write_file,fieldnames=write_header)
    _write_handler.writeheader()
    
    for index in symbol_list:
        count = 3
        buy_value = 'None'
        sell_value = 'None'
        dict_url = os.path.join(curr_path,'data\\%s.csv' % index)
        _read_file = main.read_csv(dict_url)
        
        while(count > 0):
            temp_k_value = _read_file[count]['K val']
            temp_d_value = _read_file[count]['D val']
            if (float(temp_d_value) < 15) and (float(temp_k_value) > float(temp_d_value)):
                buy_value = 'Yes'
            if (float(temp_d_value) > 85) and (float(temp_k_value) < float(temp_d_value)):
                sell_value = 'Yes'

            _write_handler.writerow({ 'Date' : _read_file[count]['Date'],
                                  'Symbol': index,
                                  'K val' : temp_k_value,
                                  'D val' : temp_d_value,
                                  'Buy'   : buy_value,
                                  'Sell'  : sell_value  })

            count -=1
        print "Completed %s"%index
    _write_file.close()