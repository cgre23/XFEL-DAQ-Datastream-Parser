import sys
import string
import os
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
import h5py
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from gui.UIdaq import Ui_Form
import shutil
import re
from datetime import datetime
from functools import reduce
import pyarrow as pa
import pyarrow.parquet as pq
from collections import defaultdict


class DAQApp(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        # Initialize parameters
        self.daterange = 0
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.channel_list = defaultdict(list)
        self.channel_list_cat, self.channel_group_list, self.channels_selected = [], [], []
        self.clusters = self.nested_dict(2, list)

        self.tablist = [self.ui.treeWidget, self.ui.treeWidget_3,
                        self.ui.treeWidget_4, self.ui.treeWidget_5, self.ui.treeWidget_6]
        self.filtertables = [self.ui.filtertable, self.ui.filtertable_2,
                             self.ui.filtertable_3, self.ui.filtertable_4, self.ui.filtertable_5]
        self.filterpbs = [self.ui.filterpb, self.ui.filterpb_2,
                          self.ui.filterpb_3, self.ui.filterpb_4, self.ui.filterpb_5]
        self.streams = ['xfel_sase1', 'xfel_sase2',
                        'xfel_sase3', 'linac', 'karabo']
        self.banned_channels = ['INDEX', 'METADATA', 'XFEL.DAQ']
        self.streampath = ''
        self.storagepath = '/Users/christiangrech/Documents/GitHub/XFEL-DAQ-Datastream-Parser/hdf5'
        self.outpath = os.getcwd() + '/out'
        # Disable buttons
        self.ui.loadcataloguepb.setEnabled(False)
        self.ui.pushButton.setEnabled(False)

        self.xml_name_matches = ["main", "run", "chan", "dscr", ".xml"]
        self.ui.number_of_files.setText('No files selected.')

        # Timestamp
        self.ui.startdate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.stopdate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.startdate.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self.ui.stopdate.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self.ui.streamtabs.setTabEnabled(0, False)
        self.ui.streamtabs.setTabEnabled(1, False)
        self.ui.streamtabs.setTabEnabled(2, False)
        self.ui.streamtabs.setTabEnabled(3, False)
        self.ui.streamtabs.setTabEnabled(4, False)

        for filtertable, filterpb in zip(self.filtertables, self.filterpbs):
            filtertable.setRowCount(0)
            filtertable.setColumnCount(1)
            filtertable.horizontalHeader().setStretchLastSection(True)
            filtertable.setHorizontalHeaderLabels(['Filter by subsystem:'])
            filtertable.setFont(QtGui.QFont('Arial', 10))
            filterpb.setEnabled(False)

        self.timeline_res = 3
        self.tw_columns = 10 * self.timeline_res
        self.ui.timeline.setRowCount(1)
        self.ui.timeline.setColumnCount(self.tw_columns+1)
        self.ui.timeline.horizontalHeader().setVisible(False)
        self.ui.timeline.verticalHeader().setVisible(False)
        #header = self.ui.timeline.horizontalHeader()
        #header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        #self.ui.timeline.setSizeAdjustPolicy(
        #    QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.timeline_colors = [QtGui.QColor(
            255, 0, 0), QtGui.QColor(0, 119, 255), QtGui.QColor(255, 255, 0), QtGui.QColor(0, 255, 0), QtGui.QColor(102, 0, 204), QtGui.QColor(255, 0, 0), ]
        self.date_header_color = QtGui.QColor(195, 195, 195)
        # Push buttons
        self.ui.browsepb.clicked.connect(self.choose_output_directory)
        self.ui.filenameEdit.setText(self.outpath)
        self.ui.browsepb2.clicked.connect(self.open_file_catalogue)
        self.ui.loadcataloguepb.clicked.connect(self.getChannelListCatalogue)
        self.ui.pushButton.clicked.connect(self.find_checked)
        self.ui.filterpb.clicked.connect(
            lambda: self.find_checked_filters(self.streams[0]))
        self.ui.filterpb_2.clicked.connect(
            lambda: self.find_checked_filters(self.streams[1]))
        self.ui.filterpb_3.clicked.connect(
            lambda: self.find_checked_filters(self.streams[2]))
        self.ui.filterpb_4.clicked.connect(
            lambda: self.find_checked_filters(self.streams[3]))
        self.ui.filterpb_5.clicked.connect(
            lambda: self.find_checked_filters(self.streams[4]))
        self.ui.hdf5button.clicked.connect(self.select_hdf5_files)

        # table/ tree headers
        for treeWidget in self.tablist:
            treeWidget.setHeaderLabels(
                ['Channel name'])
            treeWidget.setHeaderLabels(
                ['Channel name'])
            treeWidget.setHeaderLabels(
                ['Channel name'])
            header = treeWidget.header()
            header.setStretchLastSection(True)

        # Catalogue
        self.ui.treeWidget_2.setHeaderLabels(
            ['Channel name', 'Description', 'Unit'])
        header = self.ui.treeWidget_2.header()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ui.searchbar.setEnabled(False)
        self.ui.searchbar.setPlaceholderText("Search...")
        self.ui.searchbar.textChanged.connect(self.search_bar)

    def resetChannelList(self):
        self.ui.treeWidget.clear()
        self.ui.timeline.clear()
        h5f = None
        for treeWidget in self.tablist:
            treeWidget.clear()
        for filtertable, filterpb in zip(self.filtertables, self.filterpbs):
            filtertable.setRowCount(0)
            filterpb.setEnabled(False)
        self.ui.streamtabs.setTabEnabled(0, False)
        self.ui.streamtabs.setTabEnabled(1, False)
        self.ui.streamtabs.setTabEnabled(2, False)
        self.ui.streamtabs.setTabEnabled(3, False)
        self.ui.streamtabs.setTabEnabled(4, False)
        self.ui.timeline.setRowCount(1)
        self.ui.status_text.setText(
            '')
        self.channel_list = defaultdict(list)
        self.datasets_list = defaultdict(list)

    def getChannelList(self):
        self.resetChannelList()
        start_timestamp = self.ui.startdate.dateTime()
        self.start_t = start_timestamp.toPyDateTime()
        self.start_timestamp_str = start_timestamp.toString(
            'yyyyMMddTHHmmss')
        stop_timestamp_min = start_timestamp.addSecs(1)
        self.ui.stopdate.setMinimumDateTime(stop_timestamp_min)
        stop_timestamp = self.ui.stopdate.dateTime()
        self.stop_t = stop_timestamp.toPyDateTime()
        self.stop_timestamp_str = stop_timestamp.toString(
            'yyyyMMddTHHmmss')
        difference = (self.stop_t - self.start_t)
        self.total_seconds = difference.total_seconds()
        self.files_match = defaultdict(list)
        self.timeline = self.nested_dict(2, list)
        if self.filepathlist != []:
            self.ui.pushButton.setEnabled(True)
            for file in self.filepathlist:
                match = re.search('\d{8}T\d{6}_\d{8}T\d{6}', file)
                if match:
                    startdate = datetime.strptime(
                        match.group(0).split('_')[0], '%Y%m%dT%H%M%S')
                    stopdate = datetime.strptime(
                        match.group(0).split('_')[1], '%Y%m%dT%H%M%S')
                    if (startdate >= start_timestamp and stopdate <= stop_timestamp) or (stopdate >= start_timestamp and startdate <= stop_timestamp):
                        self.files_match['filename'].append(file)
                        stream = file.split('_2')[0]
                        self.files_match['stream'].append(stream)
                        self.files_match['startdate'].append(startdate)
                        self.files_match['stopdate'].append(stopdate)
                        difference_1 = (startdate - self.start_t)
                        marker_1 = difference_1.total_seconds()
                        self.timeline[stream]['start_diff'].append(
                            marker_1/self.total_seconds)
                        difference_2 = (stopdate - self.start_t)
                        marker_2 = difference_2.total_seconds()
                        self.timeline[stream]['stop_diff'].append(
                            marker_2/self.total_seconds)
                        filter = file.split('_')[-2]
                        self.timeline[stream]['filter'].append(filter)
            #print(self.files_match)
            list_len = len(self.files_match['filename'])
            self.ui.number_of_files.setText(
                '%d file(s) found.' % (list_len))

        self.getChannelsFromH5()
        # Switch current tab to one of the streams
        if self.files_match['stream'] != []:
            self.ui.streamtabs.setCurrentIndex(
                self.streams.index(self.files_match['stream'][0]))
        #print('Dataset list', self.channel_list)
        # Create a nested dictionary clusters[stream][clustername]
        self.clusters = self.nested_dict(2, list)
        date_list = pd.date_range(
            start=self.start_t, end=self.stop_t, periods=11).to_pydatetime().tolist()
        #print(date_list)
        self.ui.timeline.setRowCount(len(self.channel_list.keys())+1)

        idx = 0
        for column in range(1, self.tw_columns+1, self.timeline_res):
            self.ui.timeline.setSpan(0, column, 1, self.timeline_res)
            date_header = QtWidgets.QTableWidgetItem(
                date_list[idx].strftime("%b %d %H:%M"))
            self.ui.timeline.setItem(0, column, date_header)
            date_header.setBackground(self.date_header_color)
            idx = idx + 1
        self.ui.timeline.setRowHeight(0, 11)  # Set header row height
        idx = 0
        for stream in self.channel_list.keys():
            idx = idx + 1
            self.add_timeline(idx, stream)
            for channel in self.channel_list[stream]:
                self.add_items(channel, stream)
            self.clusters_check(stream)

    def add_timeline(self, idx, stream):
        title = QtWidgets.QTableWidgetItem(stream)
        self.ui.timeline.setItem(idx, 0, title)
        title.setBackground(self.date_header_color)
        self.ui.timeline.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.ui.timeline.setRowHeight(idx, 8)
        filters = self.timeline[stream]['filter']
        start_times = np.rint(
            np.multiply(self.timeline[stream]['start_diff'], self.tw_columns-1))
        stop_times = np.rint(
            np.multiply(self.timeline[stream]['stop_diff'], self.tw_columns-1))
        #print('Start', start_times)
        #print('Stop', stop_times)
        for start, stop, filter in zip(start_times, stop_times, filters):
            boxes = QtWidgets.QTableWidgetItem(filter)
            for column in range(1, self.tw_columns+1):
                self.ui.timeline.setColumnWidth(column, 110/self.timeline_res)
                if column >= start+1 and column <= stop+1:
                    if start != stop:
                        self.ui.timeline.setSpan(
                            idx, column, 1, (stop-start)+1)
                    self.ui.timeline.setItem(idx, column, boxes)
                    boxes.setBackground(self.timeline_colors[idx-1])
                    self.ui.timeline.setColumnWidth(
                        column, 110/self.timeline_res)

    def getChannelsFromH5(self):
        # Enable appropriate tabs
        for streamname, filename in zip(self.files_match['stream'], self.files_match['filename']):
            if streamname == self.streams[0]:
                self.ui.streamtabs.setTabEnabled(0, True)
                h5f = h5py.File(
                        self.storagepath + '/'+filename, 'r')
                self.datasets_list[streamname] = self.getdatasets('/', h5f)
                h5f.close()
            if streamname == self.streams[1]:
                self.ui.streamtabs.setTabEnabled(1, True)
                h5f = h5py.File(
                        self.storagepath + '/'+filename, 'r')
                self.datasets_list[streamname] = self.getdatasets('/', h5f)
                h5f.close()
            if streamname == self.streams[2]:
                self.ui.streamtabs.setTabEnabled(2, True)
                h5f = h5py.File(
                        self.storagepath + '/'+filename, 'r')
                self.datasets_list[streamname] = self.getdatasets('/', h5f)
                h5f.close()
            if streamname == self.streams[3]:
                self.ui.streamtabs.setTabEnabled(3, True)
                h5f = h5py.File(
                        self.storagepath + '/'+filename, 'r')
                self.datasets_list[streamname] = self.getdatasets('/', h5f)
                h5f.close()
            if streamname == self.streams[4]:
                self.ui.streamtabs.setTabEnabled(4, True)
                h5f = h5py.File(
                        self.storagepath + '/'+filename, 'r')
                self.datasets_list[streamname] = self.getdatasets('/', h5f)
                h5f.close()
            self.channel_list[streamname].extend(
                self.datasets_list[streamname])

    def getChannelListCatalogue(self):
        self.ui.treeWidget_2.clear()
        fname = self.streampath_cat

        if(fname != None and fname != ''):
            self.fname = fname
            f = QtCore.QFile(fname)
            f.open(QtCore.QIODevice.ReadOnly)
            xml = QtCore.QXmlStreamReader(f)
            while(xml.atEnd() != True):
                xml.readNext()
                if(xml.isStartDocument()):
                    continue
                if(xml.isStartElement()):
                    if(xml.name() == "NAME"):
                        self.channel_cat = str(xml.readElementText())
                        self.channel_list_cat.append(
                            str(xml.readElementText()))
                        rowcount = self.ui.treeWidget_2.topLevelItemCount()
                        item = QtWidgets.QTreeWidgetItem(rowcount)
                        self.ui.treeWidget_2.addTopLevelItem(item)
                        self.ui.treeWidget_2.topLevelItem(
                            rowcount).setText(0, self.channel_cat)
                        self.ui.treeWidget_2.topLevelItem(rowcount).setFlags(
                            self.ui.treeWidget_2.topLevelItem(rowcount).flags() | QtCore.Qt.ItemIsUserCheckable)
                        self.ui.treeWidget_2.topLevelItem(
                            rowcount).setTextAlignment(0, QtCore.Qt.AlignLeft)
                    if(xml.name() == "UNITS"):
                        self.channel_unit = str(xml.readElementText())
                        self.ui.treeWidget_2.topLevelItem(
                            rowcount).setText(2, self.channel_unit)
                    if(xml.name() == "DESC"):
                        self.channel_descriptions = str(xml.readElementText())
                        self.ui.treeWidget_2.topLevelItem(
                            rowcount).setText(1, self.channel_descriptions)
                    if(xml.name() == "DIM_NAME"):
                        self.dim_names = str(xml.readElementText())
                    if(xml.name() == "DIM_UNITS"):
                        self.dim_units = str(xml.readElementText())
                    if(xml.name() == "DIM_DESCR"):
                        self.dim_descriptions = str(xml.readElementText())
                        child = QtWidgets.QTreeWidgetItem(
                            [self.dim_names, self.dim_descriptions, self.dim_units])
                        item.addChild(child)
                #elif(xml.isEndElement()):
            xml.clear()
            f.close()
        self.ui.searchbar.setEnabled(True)

    def add_items(self, channel, stream):
        if stream == self.streams[0]:
            self.treeWidget = self.ui.treeWidget
        elif stream == self.streams[1]:
            self.treeWidget = self.ui.treeWidget_3
        elif stream == self.streams[2]:
            self.treeWidget = self.ui.treeWidget_4
        elif stream == self.streams[3]:
            self.treeWidget = self.ui.treeWidget_5
        elif stream == self.streams[4]:
            self.treeWidget = self.ui.treeWidget_6
        rowcount = self.treeWidget.topLevelItemCount()
        item = QtWidgets.QTreeWidgetItem(rowcount)
        self.treeWidget.addTopLevelItem(item)
        self.treeWidget.topLevelItem(
            rowcount).setText(0, channel)
        self.treeWidget.topLevelItem(
            rowcount).setCheckState(0, QtCore.Qt.Unchecked)
        self.treeWidget.topLevelItem(rowcount).setFlags(
            self.treeWidget.topLevelItem(rowcount).flags() | QtCore.Qt.ItemIsUserCheckable)
        self.treeWidget.topLevelItem(
            rowcount).setTextAlignment(0, QtCore.Qt.AlignLeft)

        #self.add_timeline_box(rowcount, start_times, stop_times)
        #self.ui.treeWidget.topLevelItem(
        #rowcount).setBackground(1, QtGui.QColor(125, 125, 125))

    def clusters_check(self, stream):
        if stream == self.streams[0]:
            filtertable = self.ui.filtertable
            filterpb = self.ui.filterpb
        elif stream == self.streams[1]:
            filtertable = self.ui.filtertable_2
            filterpb = self.ui.filterpb_2
        elif stream == self.streams[2]:
            filtertable = self.ui.filtertable_3
            filterpb = self.ui.filterpb_3
        elif stream == self.streams[3]:
            filtertable = self.ui.filtertable_4
            filterpb = self.ui.filterpb_4
        elif stream == self.streams[4]:
            filtertable = self.ui.filtertable_5
            filterpb = self.ui.filterpb_5
        self.clusters[stream]['Select all'] = self.channel_list[stream]
        for channel in self.channel_list[stream]:
            if channel.find('BPM') != -1:
                self.clusters[stream]['BPM'].append(channel)
            if channel.find('BAM.DAQ') != -1:
                self.clusters[stream]['BAM'].append(channel)
            if channel.find('BCM/BCM') != -1:
                self.clusters[stream]['BCM'].append(channel)
            if channel.find('XGM/XGM') != -1:
                self.clusters[stream]['XGM'].append(channel)
            if channel.find('TOROID') != -1:
                self.clusters[stream]['TOROID'].append(channel)
            if channel.find('DISTRIBUTOR') != -1:
                self.clusters[stream]['DAQ_INFO'].append(channel)
            if channel.find('XGM.POSMON') != -1 or channel.find('XGM.CURRENT') != -1 or channel.find('XGM.TEMP') != -1 or channel.find('XGM.PHOTONFLUX') != -1 or channel.find('XGM.GAS') != -1 or channel.find('XGM.PRESSURE') != -1:
                self.clusters[stream]['XGM_PROPERTIES'].append(channel)
            if channel.find('SA1') != -1:
                self.clusters[stream]['SA1'].append(channel)
            if channel.find('SA2') != -1:
                self.clusters[stream]['SA2'].append(channel)
            if channel.find('SA3') != -1:
                self.clusters[stream]['SA3'].append(channel)
            if channel.find('TIMINGINFO') != -1:
                self.clusters[stream]['TIMINGINFO'].append(channel)
            if channel.find('MAGNETS/MAGNET') != -1:
                self.clusters[stream]['MAGNET'].append(channel)
            if channel.find('HOLDDMA') != -1:
                self.clusters[stream]['HOLDDMA'].append(channel)
            if channel.find('CHICANE') != -1:
                self.clusters[stream]['CHICANE'].append(channel)
            if channel.find('UNDULATOR') != -1:
                self.clusters[stream]['UNDULATOR'].append(channel)
            if channel.find('RF/MODULATOR') != -1:
                self.clusters[stream]['RF'].append(channel)
            if channel.find('BEAM_ENERGY_MEASUREMENT') != -1:
                self.clusters[stream]['BEAM_ENERGY_MEASUREMENT'].append(
                    channel)
            if channel.find('CHARGE.ML') != -1:
                self.clusters[stream]['CHARGE'].append(channel)
            if channel.find('HOLDSCOPE') != -1:
                self.clusters[stream]['HOLDSCOPE'].append(channel)
            if channel.find('BHM/BHM') != -1:
                self.clusters[stream]['BHM'].append(channel)
            if channel.find('KICKER.ADC') != -1:
                self.clusters[stream]['KICKER'].append(channel)
            if channel.find('FARADAY') != -1:
                self.clusters[stream]['FARADAY'].append(channel)
            if channel.find('DCM/DCM') != -1:
                self.clusters[stream]['DCM'].append(channel)
            if channel.find('BLM/BLM') != -1:
                self.clusters[stream]['BLM'].append(channel)
            if channel.find('BEAMVIEW_SHIMADZU') != -1:
                self.clusters[stream]['SHIMADZU'].append(channel)
            if channel.find('MDL/MAIN') != -1:
                self.clusters[stream]['MDL'].append(channel)
            if channel.find('BEAMCONDITIONS') != -1:
                self.clusters[stream]['BEAMCONDITIONS'].append(channel)
            if channel.find('MOTOR') != -1:
                self.clusters[stream]['MOTOR'].append(channel)
            if channel.find('X2TIMER2') != -1:
                self.clusters[stream]['X2TIMER2'].append(channel)
            if channel.find('HIREX') != -1:
                self.clusters[stream]['HIREX'].append(channel)
        self.fill_filter_table(filtertable, stream)
        filterpb.setEnabled(True)

    def find_checked(self):
        self.checked_list = []
        for treeView in self.tablist:
            root = treeView.invisibleRootItem()
            signal_count = root.childCount()
            if signal_count > 0:
                for i in range(signal_count):
                    signal = root.child(i)
                    if signal.checkState(0) == QtCore.Qt.Checked:
                        self.checked_list.append(signal.text(0))
        if self.checked_list != []:
            self.ui.status_text.setText(
                    'Writing files to output directory......')
            print(self.checked_list)
            self.ui.pushButton.setEnabled(False)
            #self.create_hdf5_file('1')
            self.write_files()
            self.ui.status_text.setText(
                'Files created successfully.')
            # ACTION
            self.ui.pushButton.setEnabled(True)
        else:
            self.ui.status_text.setText('No channels selected')

    def find_checked_filters(self, stream):
        self.checked_filter_list = defaultdict(list)
        selected_channels = []
        if stream == self.streams[0]:
            filtertable = self.ui.filtertable
            treeWidget = self.ui.treeWidget
        elif stream == self.streams[1]:
            filtertable = self.ui.filtertable_2
            treeWidget = self.ui.treeWidget_3
        elif stream == self.streams[2]:
            filtertable = self.ui.filtertable_3
            treeWidget = self.ui.treeWidget_4
        elif stream == self.streams[3]:
            filtertable = self.ui.filtertable_4
            treeWidget = self.ui.treeWidget_5
        elif stream == self.streams[4]:
            filtertable = self.ui.filtertable_5
            treeWidget = self.ui.treeWidget_6
        for i in range(filtertable.rowCount()):
            if filtertable.item(i, 0).checkState() == QtCore.Qt.Checked:
                self.checked_filter_list[stream].append(
                    filtertable.item(i, 0).text())
            else:
                pass
        selected_channels = [self.clusters[stream][x]
                             for x in self.checked_filter_list[stream]]
        flat_list = [item for sublist in selected_channels for item in sublist]
        # Uncheck current items
        root = treeWidget.invisibleRootItem()
        signal_count = root.childCount()
        if signal_count > 0:
            for i in range(signal_count):
                signal = root.child(i)
                if signal.checkState(0) == QtCore.Qt.Checked:
                    signal.setCheckState(0, QtCore.Qt.Unchecked)
        # Check items in filter
        for channel in flat_list:
            matching_items = treeWidget.findItems(
                channel, Qt.MatchExactly)
            if matching_items:
                # We have found something.
                item = matching_items[0]  # Take the first.
                item.setCheckState(0, QtCore.Qt.Checked)

    def write_files(self):
        self.d = {}
        for inputfile, stream in zip(self.files_match['filename'], self.files_match['stream']):
            h5f = h5py.File(self.storagepath + '/'+inputfile)
            self.getkeys('/', h5f)
            if stream == 'karabo':
                self.index = pd.DataFrame()
                self.getindex('/', h5f)
            h5f.close()

        dfs_list = []
        for key, sub_df in self.d.items():
            if not 'Trainid' in sub_df.columns:
                sub_df['Trainid'] = self.index['trainId']
            if key.find('INSTRUMENT') != -1:
                sub_df['timestamp'] = self.index['timestamp']
            if 'timestamp' in sub_df.columns:
                sub_df['timestamp'] = [int(x // 1000)
                                       for x in self.index['timestamp']]
            if 'TimeStamp' in sub_df.columns:    # XFEL DAQ
                sub_df['timestamp'] = [int((datetime.fromtimestamp(x[0]).replace(
                    microsecond=x[1]).timestamp())*1e6) for x in sub_df['TimeStamp']]
                sub_df = sub_df.drop(columns=['TimeStamp'])
            sub_df.set_index(['Trainid', 'timestamp'], inplace=True, drop=True)
            dfs_list.append(sub_df)
        #dfs_list.sort(key=len, reverse=True)
        print(dfs_list)
        df_merged = reduce(lambda left, right: pd.merge(
            left, right, on=['Trainid', 'timestamp'], how='outer'), dfs_list)
        print(df_merged)
        table = pa.Table.from_pandas(df_merged)
        pq.write_to_dataset(
            table,
            root_path=self.outpath + '/xfel_' + self.start_timestamp_str
            + '_' + self.stop_timestamp_str + '.parquet'
        )

    def getdatasets_filtered(self, key, archive):
        if key[-1] != '/':
            key += '/'
        out = []
        for name in archive[key]:
            if any(key[1:-1] in s for s in self.checked_list):
                #print('KEY', key[1:-1])
                path = key + name
                if isinstance(archive[path], h5py.Dataset):
                    out += [path]
                else:
                    out += self.getdatasets_filtered(path, archive)
        return out

# function to return a list of paths to each dataset
    def getdatasets(self, key, archive):
        if key[-1] != '/':
            key += '/'
        out = []
        for name in archive[key]:
            #print('KEY', key[1:-1])
            path = key + name
            if isinstance(archive[path], h5py.Dataset):
                if (key[1:-1] not in out) and (key[1:-1].split('/')[0] not in self.banned_channels):
                    out += [key[1:-1]]
            else:
                out += self.getdatasets(path, archive)
        return out

    def getkeys(self, key, archive):
        if key[-1] != '/':
            key += '/'
        out_key = []
        for name in archive[key]:
            if any(key[1:-1] in s for s in self.checked_list):
                path = key + name
                if path.find('IMGPII45') != -1:
                    continue
                if isinstance(archive[path], h5py.Dataset):
                    if (key[1:-1] not in out_key):
                        self.d[key[1:-1]] = pd.DataFrame()
                        out_key += [key[1:-1]]
                    if name == 'TimeStamp' or name == 'timestamp':
                        self.d[key[1:-1]][name] = archive[path]
                        continue
                    if name == 'TrainId' or name == 'trainId':
                        self.d[key[1:-1]]['Trainid'] = archive[path]
                        continue
                    else:
                        self.d[key[1:-1]][path] = archive[path]
                else:
                    self.getkeys(path, archive)

    def getindex(self, key, archive):
        if key[-1] != '/':
            key += '/'
        for name in archive[key]:
            path = key + name
            if isinstance(archive[path], h5py.Dataset):
                #print(path)
                if path.find('INDEX/trainId') != -1:
                    self.index['trainId'] = archive[path]
                if path.find('INDEX/timestamp') != -1:
                    self.index['timestamp'] = archive[path]
                    #print(self.index['timestamp'])
            else:
                self.getindex(path, archive)

    def choose_output_directory(self):  # self.parent.data_dir
        self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(
            self, caption='Choose Directory', directory=os.getcwd())
        if self.folderpath != []:
            print(self.folderpath)
            self.ui.filenameEdit.setText(self.folderpath)
            self.outpath = self.folderpath
            self.ui.pushButton.setEnabled(True)
            # Do Action
        else:
            self.ui.status_text.setText('No output directory selected')

    def select_hdf5_files(self):  # self.parent.data_dir
        self.filepathlist = [f for f in listdir(
            self.storagepath) if isfile(join(self.storagepath, f))]
        #self.filepathlist, _ = QtWidgets.QFileDialog.getOpenFileNames(
        #    self, "Pick hdf5 files", "/pnfs/desy.de/xfel", 'hdf5 (*.hdf5)', None, QtWidgets.QFileDialog.DontUseNativeDialog)
        if self.filepathlist != []:
            self.getChannelList()
        else:
            self.ui.number_of_files.setText(
                'No files found.')

    def open_file_catalogue(self):  # self.parent.data_dir
        self.streampath_cat, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Pick channel description file", "/daq/xfel/admtemp", 'xml (*.xml)', None, QtWidgets.QFileDialog.DontUseNativeDialog)
        if self.streampath_cat != "":
            filename_cat = os.path.basename(self.streampath_cat)
            self.ui.filenameEdit2.setText(filename_cat)
            self.ui.loadcataloguepb.setEnabled(
                self.check_xml_filename(self.streampath_cat))
        else:
            self.ui.filenameEdit2.setText('')

    def fill_filter_table(self, filtertable, stream):
        filtertable.setRowCount(0)
        for row, key in enumerate(self.clusters[stream]):
            if self.clusters[stream][key] == []:
                pass
            else:
                rowPosition = filtertable.rowCount()
                filtertable.insertRow(rowPosition)  # insert new row
                chkBoxItem = QtWidgets.QTableWidgetItem(key)
                chkBoxItem.setText(key)
                chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable
                                    | QtCore.Qt.ItemIsEnabled)
                chkBoxItem.setCheckState(QtCore.Qt.Unchecked)
                filtertable.setItem(
                    rowPosition, 0, chkBoxItem)

    def nested_dict(self, n, type):
        if n == 1:
            return defaultdict(type)
        else:
            return defaultdict(lambda: self.nested_dict(n-1, type))

    def search_bar(self, s):
        # Clear current selection.
        self.ui.treeWidget_2.setCurrentItem(None)
        if not s:
            # Empty string, don't search.
            return
        matching_items = self.ui.treeWidget_2.findItems(s, Qt.MatchContains)
        if matching_items:
            # We have found something.
            item = matching_items[0]  # Take the first.
            self.ui.treeWidget_2.setCurrentItem(item)

    def filter_by_group(self, group):
        # Clear current selection.
        self.ui.treeWidget_2.setCurrentItem(None)
        if not group:
            # Empty string, don't search.
            return
        matching_items = self.ui.treeWidget_2.findItems(
            group, Qt.MatchContains)
        if matching_items:
            # We have found something.
            item = matching_items[0]  # Take the first.
            self.ui.treeWidget_2.setCurrentItem(item)

    def check_xml_filename(self, path):
        if all(x in path for x in self.xml_name_matches):
            return True
        else:
            return False

    def makedirs(self, dest):
        if not os.path.exists(dest):
            os.makedirs(dest)

    def deletedirs(self):
        path = os.getcwd()
        file_path = path + '/temp/'
        try:
            shutil.rmtree(file_path)
            print("Temp file deleted.")
        except OSError as e:
            print("Error: %s : %s" % (file_path, e.strerror))

    def error_box(self, message):
        QtGui.QMessageBox.about(self, "Error box", message)

    def question_box(self, message):
        #QtGui.QMessageBox.question(self, "Question box", message)
        reply = QtGui.QMessageBox.question(self, "Question Box",
                                           message,
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            return True

        return False


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DAQApp()

    path = 'gui/xfel.png'
    app.setWindowIcon(QtGui.QIcon(path))
    window.show()
    window.raise_()

    sys.exit(app.exec_())
