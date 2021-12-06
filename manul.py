import sys
import string
import os
from xml.sax.saxutils import escape
from PyQt5 import QtGui, QtCore, QtWidgets
from gui.UI_daq import Ui_Form
import datetime


class DAQApp(QtWidgets.QWidget):
    def __init__(self):
        super(DAQApp, self).__init__()
        #uic.loadUi('gui/UIdaq.ui', self)
        #self.show()
        self.daterange = 0
        #self.currentChanged.connect(self.setup_settings)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.streamcombo.addItems(
            ["linac", "xfel_sase1", "xfel_sase2", "xfel_sase3"])
        self.ui.streamcombo2.addItems(
            ["linac", "xfel_sase1", "xfel_sase2", "xfel_sase3"])
        self.ui.startdate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.stopdate.setDateTime(QtCore.QDateTime.currentDateTime())
        self.ui.startdate.setDisplayFormat("dd/MM/yyyy hh:mm:ss")
        self.ui.stopdate.setDisplayFormat("dd/MM/yyyy hh:mm:ss")

        self.ui.treeWidget.setHeaderLabels(['Channel name'])
        self.ui.treeWidget_2.setHeaderLabels(
            ['Channel name', 'Description', 'Unit'])

        self.channel_list = []
        self.channels_selected = []
        self.ui.channelpb.clicked.connect(self.openClicked)
        self.ui.loadcataloguepb.clicked.connect(self.openClickedCatalogue)

        self.ui.pushButton.clicked.connect(self.find_checked)

        header = self.ui.treeWidget_2.header()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        #selmodel = self.ui.treeWidget.selectionModel()
        #selmodel.selectionChanged.connect(self.handleSelection)

    def openClicked(self):
        #fname = QtGui.QFileDialog.getOpenFileName(
        #self, 'Open file...', '', 'xml (*.xml)')
        fname = "/Users/christiangrech/Documents/GitHub/XFEL-DAQ-Datastream-Parser/xml/xfel_sase1_main_run1727_chan_dscr.xml"

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
                        self.channel = str(xml.readElementText())
                        self.channel_list.append(str(xml.readElementText()))
                        self.add_items()
                elif(xml.isEndElement()):
                    if(xml.name() == "option"):
                        print("</option>")
                    elif(xml.name() == "text"):
                        print("</text>")

            xml.clear()
            f.close()

    def openClickedCatalogue(self):
        #fname = QtGui.QFileDialog.getOpenFileName(
        #self, 'Open file...', '', 'xml (*.xml)')
        fname = "/Users/christiangrech/Documents/GitHub/XFEL-DAQ-Datastream-Parser/xml/xfel_sase1_main_run1727_chan_dscr.xml"

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
                        self.channel = str(xml.readElementText())
                        self.channel_list.append(str(xml.readElementText()))

                        rowcount = self.ui.treeWidget_2.topLevelItemCount()
                        item = QtWidgets.QTreeWidgetItem(rowcount)
                        self.ui.treeWidget_2.addTopLevelItem(item)
                        self.ui.treeWidget_2.topLevelItem(
                            rowcount).setText(0, self.channel)
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
                elif(xml.isEndElement()):
                    if(xml.name() == "option"):
                        print("</option>")
                    elif(xml.name() == "text"):
                        print("</text>")

            xml.clear()
            f.close()

    def add_items(self):
        rowcount = self.ui.treeWidget.topLevelItemCount()
        item = QtWidgets.QTreeWidgetItem(rowcount)
        self.ui.treeWidget.addTopLevelItem(item)
        #print(self.channel)
        self.ui.treeWidget.topLevelItem(
            rowcount).setText(0, self.channel)
        self.ui.treeWidget.topLevelItem(
            rowcount).setCheckState(0, QtCore.Qt.Unchecked)
        self.ui.treeWidget.topLevelItem(rowcount).setFlags(
            self.ui.treeWidget.topLevelItem(rowcount).flags() | QtCore.Qt.ItemIsUserCheckable)
        self.ui.treeWidget.topLevelItem(
            rowcount).setTextAlignment(0, QtCore.Qt.AlignLeft)

    def find_checked(self):
        self.checked_list = list()
        root = self.ui.treeWidget.invisibleRootItem()
        signal_count = root.childCount()
        print(signal_count)

        for i in range(signal_count):
            signal = root.child(i)
            if signal.checkState(0) == QtCore.Qt.Checked:
                self.checked_list.append(signal.text(0))
        print(self.checked_list)
        self.create_xml()

    def create_xml(self):
        inner_template = string.Template('<Chan name="${name}"/>')

        outer_template = string.Template("""<DAQREQ>
        <TStart time='${starttime}'/>
        <TStop  time='${stoptime}'/>
        <Exp  name='${exp}'/>
        ${document_list}
        </DAQREQ>
         """)

        data = self.checked_list
        start_timestamp = self.ui.startdate.dateTime()
        start_timestamp_str = start_timestamp.toString('yyyy-MM-ddTHH:mm:ss')
        stop_timestamp_min = start_timestamp.addSecs(1)
        self.ui.stopdate.setMinimumDateTime(stop_timestamp_min)
        stop_timestamp = self.ui.stopdate.dateTime().toString('yyyy-MM-ddTHH:mm:ss')

        inner_contents = [inner_template.substitute(
            name=channel) for channel in data]
        result = outer_template.substitute(
            document_list='\n'.join(inner_contents), exp=str(self.ui.streamcombo.currentText()), starttime=start_timestamp_str, stoptime=stop_timestamp)
        self.write_status = None
        filename = str(self.ui.streamcombo.currentText()) + \
            '_run' + str(self.ui.runspinBox.value()) + '.xml'
        self.write_status = None
        try:
            with open(filename, 'w') as writer:
                writer.write(result)
                self.write_status = True
        except Exception as err:
            self.write_status = False
        self.launch_script()

    def launch_script(self):
        with open('run.sh', 'w') as rsh:
            rsh.writelines('echo "I ran this"\n')
        os.system("xterm -hold -e run.sh")
        #self.panel = daqraw2hdf5.runscript()
        #self.panel.show()

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
