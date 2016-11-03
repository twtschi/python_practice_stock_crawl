# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 17:07:27 2016

@author: Vincent_Wu
"""

from bokeh.plotting import figure, output_file, show,ColumnDataSource
from bokeh.models import HoverTool

def save_data (data,file_writer):
#Initialization
    n          = 10  #Calculate n days period criteria
    RSV        = 0   #Initial RSV value
    count      = 0
    init_k     = 50  #Initial K value when there is no K value exist
    temp_x     = list() #sort in date
    temp_high  = list()
    temp_low   = list()
    temp_date  = list()
    temp_close = list()
    temp_mean  = list()
    temp_k     = list()
    temp_d     = list()
    temp_k_value = 0
    temp_d_value = 0
    for count in range(len(data)):
#        temp_x.append(data[count]['Date'].split("-")[2])
        temp_x.append(len(data)-count)
        temp_high.append(data[count]['High'])
        temp_low.append(data[count]['Low'])
        temp_date.append(data[count]['Date'])
        temp_close.append(data[count]['Close'])
        temp_mean.append((float(data[count]['High'])+float(data[count]['Low']))/2)

#Calculate K value
    buff_k = init_k
    buff_d = init_k
    for index_x in range(len(data)):
        
        if (index_x-n) >0:
            index_start=index_x-n
        else:
            index_start = 0

        if not (index_x <1):
            min_low = min(temp_low[index_start:index_x])
            max_high = max(temp_high[index_start:index_x])

            RSV = (float(temp_close[index_x])-float(min_low))/(float(max_high)-float(min_low))*100
            temp_k_value = (2*float(buff_k)/3) +(float(RSV)/3)
            buff_k = temp_k_value
            temp_k.append(temp_k_value)
#Calculate D value
            temp_d_value = (2*float(buff_d)/3) +(float(temp_k_value)/3)
            buff_d = temp_d_value
            temp_d.append(temp_d_value)
#Judge buy/sell signal

        file_writer.writerow({'Date' : data[index_x]['Date'],
                              'High' : data[index_x]['High'],
                              'Low'  : data[index_x]['Low'],
                              'Close': data[index_x]['Close'],
                              'K val': temp_k_value,
                              'D val': temp_d_value
                              })
        #file_write_opener.seek(-2, os.SEEK_END) # Delete writerow with '/r'/n'
        #file_write_opener.truncate()            # 
            
def plot_ui (data):
    output_file("plot.html")
#Initialization
    n          = 10  #Calculate n days period criteria
    RSV        = 0   #Initial RSV value
    count      = 0
    init_k     = 50  #Initial K value when there is no K value exist
    temp_x     = list() #sort in date
    temp_high  = list()
    temp_low   = list()
    temp_date  = list()
    temp_close = list()
    temp_mean  = list()
    temp_k     = list()
    temp_d     = list()
    buy_sig_x  = list()
    buy_sig_y  = list()
    buy_sig_d  = list()
    sold_sig_x = list()
    sold_sig_y = list()
    sold_sig_d = list()
#Get data from datalist    
    for count in range(len(data)):
#        temp_x.append(data[count]['Date'].split("-")[2])
        temp_x.append(len(data)-count)
        temp_high.append(data[count]['High'])
        temp_low.append(data[count]['Low'])
        temp_date.append(data[count]['Date'])
        temp_close.append(data[count]['Close'])
        temp_mean.append((float(data[count]['High'])+float(data[count]['Low']))/2)

#Calculate K value
    buff_k = init_k
    buff_d = init_k
    for index_x in range(len(data)):
        
        if (index_x-n) >0:
            index_start=index_x-n
        else:
            index_start = 0

        if not (index_x <1):
            min_low = min(temp_low[index_start:index_x])
            max_high = max(temp_high[index_start:index_x])

            RSV = (float(temp_close[index_x])-float(min_low))/(float(max_high)-float(min_low))*100
            temp_k_value = (2*float(buff_k)/3) +(float(RSV)/3)
            buff_k = temp_k_value
            temp_k.append(temp_k_value)
#Calculate D value
            temp_d_value = (2*float(buff_d)/3) +(float(temp_k_value)/3)
            buff_d = temp_d_value
            temp_d.append(temp_d_value)
#Judge buy/sell signal
            if (temp_d_value < 15) and (temp_k_value > temp_d_value):
                buy_sig_x.append(len(data)-index_x)
                buy_sig_y.append(temp_d_value)
                buy_sig_d.append(data[index_x]['Date'])
            if (temp_d_value > 85) and (temp_k_value < temp_d_value):
                sold_sig_x.append(len(data)-index_x)
                sold_sig_y.append(temp_d_value)
                sold_sig_d.append(data[index_x]['Date'])

#Generate Plot Source
    source_high = ColumnDataSource(
        data=dict(
            date=temp_date,
            data=temp_high,
            )
    )
    source_low = ColumnDataSource(
        data=dict(
            date=temp_date,
            data=temp_low,
            )
    )
    source_mean = ColumnDataSource(
        data=dict(
            date=temp_date,
            data=temp_mean,
            )
    )
    source_k = ColumnDataSource(
        data=dict(
            date=temp_date,
            data=temp_k,
            )
    )
    source_d = ColumnDataSource(
        data=dict(
            date=temp_date,
            data=temp_d,
            )
    )
    source_buy_signal = ColumnDataSource(
        data=dict(
            date=buy_sig_d,
            data=buy_sig_y,
            )
    )
    source_sold_signal = ColumnDataSource(
        data=dict(
            date=sold_sig_d,
            data=sold_sig_y,
            )
    )
    hover = HoverTool(
        tooltips=[
            ("date", "@date"),
            ("data","@data")
            ]
    )
    TOOLS = 'box_zoom,box_select,crosshair,resize,reset'
    p = figure(toolbar_location="below",plot_width=1000, plot_height=600,title=data[0]['symbol'],tools=TOOLS)
    p.add_tools(hover)
    p.circle(temp_x,temp_high,color="red" ,size=3,source=source_high)
    p.circle(temp_x,temp_low,color="green",size=3,source=source_low)
    p.line(temp_x,temp_mean,source=source_mean)
    p.line(temp_x,temp_k,source=source_k,color="red")
    p.line(temp_x,temp_d,source=source_d,color="green")
    p.circle(buy_sig_x,buy_sig_y,source=source_buy_signal,size=15,color="red")
    p.circle(sold_sig_x,sold_sig_y,source=source_sold_signal,size=15,color="green")
    show(p)