import sys
import logging
import datetime
import logging
import numpy as np
import pandas as pd
from plotnine import *
from mizani.formatters import date_format
import os

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO)

csvfile = "SDRPlayBatDetector.csv"
colnames = ['timestamp','timestamp-utc','start_freq','start_power','end_freq','end_power','bins']
logging.info("Processing %s", csvfile)

event_df = pd.read_csv(csvfile, names=colnames, header=None).dropna()

#event_df = pd.read_csv(csvfile, usecols=[0,6,7,8], names=['timestamp', 'channel', 'signal_dbm', 'ssid'])

event_df['timestamp-utc'] = event_df['timestamp-utc'].apply(lambda x: datetime.datetime.fromtimestamp(x))

title = "Possible events"

graph = ggplot(event_df) 

graph = ggplot(event_df, aes(y = 'timestamp-utc', x = 'start_freq+end_freq/2')) + geom_point(aes(size='start_power+end_power/2'), alpha=0.2) + \
        ylab("Hour") + theme(axis_text_x=element_text(rotation=90, size=6)) + \
        scale_y_datetime(date_breaks = "1 hour", labels = date_format("%H")) + \
        theme(axis_text_y=element_text(size=6)) + theme(figure_size=(16, 8)) + \
        ggtitle(title)

plot_filename = os.getcwd() + '/events.jpg'
logging.info("Saving %s", plot_filename)
graph.save(filename = plot_filename, dpi = 600)





