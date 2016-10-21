# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 11:41:09 2016

@author: Vincent_Wu
"""

import stockquote,os
from bokeh.plotting import figure, output_file, show,ColumnDataSource
from bokeh.models import HoverTool, BoxSelectTool
#h = list(stockquote.historical_quotes("GOOG", "20160901", "20160930"))
#print os.linesep.join(["%25s: %s" % (k, h[0][k]) for k in sorted(h[0].keys())])
#q = stockquote.from_google("GOOG")

def plot_ui (data):
    output_file("plot.html")
    
    count = 0
    temp_x  = list()
    for count in range(len(data)):
#        temp_x.append(data[count]['Date'].split("-")[2])
        temp_x.append(len(data)-count)
        
    count = 0
    temp_high  = list()
    for count in range(len(data)):
        temp_high.append(data[count]['High'])

    count = 0
    temp_low  = list()
    for count in range(len(data)):
        temp_low.append(data[count]['Low'])

    count = 0
    temp_date  = list()
    for count in range(len(data)):
        temp_date.append(data[count]['Date'])

    count = 0
    temp_mean  = list()
    for count in range(len(data)):
        temp_mean.append((float(data[count]['High'])+float(data[count]['Low']))/2)

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
    hover = HoverTool(
        tooltips=[
            ("index", "$index"),
            ("date", "@date"),
            ("data","@data")
            ]
    )
    TOOLS = [BoxSelectTool(), hover]
    p = figure(tools=TOOLS)
    p.circle(temp_x,temp_high,color="red" ,size=10,source=source_high)
    p.circle(temp_x,temp_low,color="green",size=10,source=source_low)
    p.line(temp_x,temp_mean,source=source_mean)
    show(p)
    
if __name__ == "__main__":
    h = list(stockquote.historical_quotes("GOOG", "20160601", "20161030"))
    plot_ui(h)
