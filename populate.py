import sys
sys.path.append('../')

from genki_wave.discover import run_discover_bluetooth
run_discover_bluetooth()

from genki_wave.asyncio_runner import run_asyncio_bluetooth
from graphData.graph_callback import PlotData

import time

#clear file
file1 = open('properties.csv','w')
file1.close()
#define how frequently new data is written to 'properties.csv'
callbacks = [PlotData(print_data_every_n_seconds=1)]
#static bluetooth address for Wave ring
ble_address = "0EAAC666-5C0B-2348-F264-010C165744B1"

#Connect to bluetooth and start printing to 'practice.csv' until Ctrl+c
run_asyncio_bluetooth(callbacks, ble_address)