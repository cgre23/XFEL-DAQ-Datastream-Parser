# XFEL-DAQ-Datastream-Parser

Author: Christian Grech (christian.grech@desy.de)

Software to convert raw DAQ files from the XFEL DAQ Datastream to accessible HDF5 files.

Thu 09 Dec 2021
* Added Filter system to filter channel list by name group.
* Added local mode to run parser using local raw files.
* Catalogue now has a search function to find keywords.


TBD:
* Try PNFS data in BKR
* Set up data folder in BKR


python3 level0.py --start 2021-11-17T15:02:00 --stop 2021-11-17T15:02:05 --xmldfile xml/xfel_sase1_main_run1727_chan_dscr.xml --dest SA1
