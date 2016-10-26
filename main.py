# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 11:41:09 2016

@author: Vincent_Wu
"""

import stockquote
import plot
from Tkinter import *

#h = list(stockquote.historical_quotes("GOOG", "20160901", "20160930"))
#print os.linesep.join(["%25s: %s" % (k, h[0][k]) for k in sorted(h[0].keys())])
#q = stockquote.from_google("GOOG")

if __name__ == "__main__":
    #h = list(stockquote.historical_quotes("GOOG", "20160101", "20161030"))
    #plot.plot_ui(h)
    root = Tk()
    some = Label(root, text="Tk's job!!", width="30", height="5")
    some.pack()
    root.mainloop()
