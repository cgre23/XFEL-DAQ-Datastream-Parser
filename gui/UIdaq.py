# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIdaq.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(1331, 640)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        Form.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        Form.setWindowOpacity(1.0)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.status_text = QtWidgets.QLabel(self.tab)
        self.status_text.setText("")
        self.status_text.setObjectName("status_text")
        self.gridLayout_3.addWidget(self.status_text, 5, 0, 1, 2)
        self.streamtabs = QtWidgets.QTabWidget(self.tab)
        self.streamtabs.setObjectName("streamtabs")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.filterpb = QtWidgets.QPushButton(self.tab_3)
        self.filterpb.setObjectName("filterpb")
        self.gridLayout_5.addWidget(self.filterpb, 1, 1, 1, 1)
        self.treeWidget = QtWidgets.QTreeWidget(self.tab_3)
        self.treeWidget.setTabletTracking(False)
        self.treeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget.setAutoScroll(True)
        self.treeWidget.setIndentation(25)
        self.treeWidget.setAnimated(False)
        self.treeWidget.setWordWrap(False)
        self.treeWidget.setHeaderHidden(False)
        self.treeWidget.setColumnCount(11)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.treeWidget.header().setVisible(False)
        self.treeWidget.header().setCascadingSectionResizes(True)
        self.treeWidget.header().setHighlightSections(True)
        self.treeWidget.header().setSortIndicatorShown(False)
        self.treeWidget.header().setStretchLastSection(False)
        self.gridLayout_5.addWidget(self.treeWidget, 0, 0, 2, 1)
        self.filtertable = QtWidgets.QTableWidget(self.tab_3)
        self.filtertable.setMaximumSize(QtCore.QSize(300, 16777215))
        self.filtertable.setColumnCount(0)
        self.filtertable.setObjectName("filtertable")
        self.filtertable.setRowCount(0)
        self.filtertable.verticalHeader().setVisible(False)
        self.gridLayout_5.addWidget(self.filtertable, 0, 1, 1, 1)
        self.streamtabs.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.filtertable_2 = QtWidgets.QTableWidget(self.tab_4)
        self.filtertable_2.setMaximumSize(QtCore.QSize(300, 16777215))
        self.filtertable_2.setColumnCount(0)
        self.filtertable_2.setObjectName("filtertable_2")
        self.filtertable_2.setRowCount(0)
        self.filtertable_2.verticalHeader().setVisible(False)
        self.gridLayout_6.addWidget(self.filtertable_2, 0, 1, 1, 1)
        self.filterpb_2 = QtWidgets.QPushButton(self.tab_4)
        self.filterpb_2.setObjectName("filterpb_2")
        self.gridLayout_6.addWidget(self.filterpb_2, 1, 1, 1, 1)
        self.treeWidget_3 = QtWidgets.QTreeWidget(self.tab_4)
        self.treeWidget_3.setTabletTracking(False)
        self.treeWidget_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget_3.setAutoScroll(True)
        self.treeWidget_3.setIndentation(25)
        self.treeWidget_3.setAnimated(False)
        self.treeWidget_3.setWordWrap(False)
        self.treeWidget_3.setHeaderHidden(False)
        self.treeWidget_3.setColumnCount(11)
        self.treeWidget_3.setObjectName("treeWidget_3")
        self.treeWidget_3.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.treeWidget_3.header().setVisible(False)
        self.treeWidget_3.header().setCascadingSectionResizes(True)
        self.treeWidget_3.header().setHighlightSections(True)
        self.treeWidget_3.header().setSortIndicatorShown(False)
        self.treeWidget_3.header().setStretchLastSection(False)
        self.gridLayout_6.addWidget(self.treeWidget_3, 0, 0, 2, 1)
        self.streamtabs.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.filtertable_3 = QtWidgets.QTableWidget(self.tab_5)
        self.filtertable_3.setMaximumSize(QtCore.QSize(300, 16777215))
        self.filtertable_3.setColumnCount(0)
        self.filtertable_3.setObjectName("filtertable_3")
        self.filtertable_3.setRowCount(0)
        self.filtertable_3.verticalHeader().setVisible(False)
        self.gridLayout_7.addWidget(self.filtertable_3, 0, 1, 1, 1)
        self.filterpb_3 = QtWidgets.QPushButton(self.tab_5)
        self.filterpb_3.setObjectName("filterpb_3")
        self.gridLayout_7.addWidget(self.filterpb_3, 1, 1, 1, 1)
        self.treeWidget_4 = QtWidgets.QTreeWidget(self.tab_5)
        self.treeWidget_4.setTabletTracking(False)
        self.treeWidget_4.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget_4.setAutoScroll(True)
        self.treeWidget_4.setIndentation(25)
        self.treeWidget_4.setAnimated(False)
        self.treeWidget_4.setWordWrap(False)
        self.treeWidget_4.setHeaderHidden(False)
        self.treeWidget_4.setColumnCount(11)
        self.treeWidget_4.setObjectName("treeWidget_4")
        self.treeWidget_4.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.treeWidget_4.header().setVisible(False)
        self.treeWidget_4.header().setCascadingSectionResizes(True)
        self.treeWidget_4.header().setHighlightSections(True)
        self.treeWidget_4.header().setSortIndicatorShown(False)
        self.treeWidget_4.header().setStretchLastSection(False)
        self.gridLayout_7.addWidget(self.treeWidget_4, 0, 0, 2, 1)
        self.streamtabs.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.tab_6)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.filtertable_4 = QtWidgets.QTableWidget(self.tab_6)
        self.filtertable_4.setMaximumSize(QtCore.QSize(300, 16777215))
        self.filtertable_4.setColumnCount(0)
        self.filtertable_4.setObjectName("filtertable_4")
        self.filtertable_4.setRowCount(0)
        self.filtertable_4.verticalHeader().setVisible(False)
        self.gridLayout_8.addWidget(self.filtertable_4, 0, 1, 1, 1)
        self.filterpb_4 = QtWidgets.QPushButton(self.tab_6)
        self.filterpb_4.setObjectName("filterpb_4")
        self.gridLayout_8.addWidget(self.filterpb_4, 1, 1, 1, 1)
        self.treeWidget_5 = QtWidgets.QTreeWidget(self.tab_6)
        self.treeWidget_5.setTabletTracking(False)
        self.treeWidget_5.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget_5.setAutoScroll(True)
        self.treeWidget_5.setIndentation(25)
        self.treeWidget_5.setAnimated(False)
        self.treeWidget_5.setWordWrap(False)
        self.treeWidget_5.setHeaderHidden(False)
        self.treeWidget_5.setColumnCount(11)
        self.treeWidget_5.setObjectName("treeWidget_5")
        self.treeWidget_5.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.treeWidget_5.header().setVisible(False)
        self.treeWidget_5.header().setCascadingSectionResizes(True)
        self.treeWidget_5.header().setHighlightSections(True)
        self.treeWidget_5.header().setSortIndicatorShown(False)
        self.treeWidget_5.header().setStretchLastSection(False)
        self.gridLayout_8.addWidget(self.treeWidget_5, 0, 0, 2, 1)
        self.streamtabs.addTab(self.tab_6, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_7)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.filtertable_5 = QtWidgets.QTableWidget(self.tab_7)
        self.filtertable_5.setMaximumSize(QtCore.QSize(300, 16777215))
        self.filtertable_5.setColumnCount(0)
        self.filtertable_5.setObjectName("filtertable_5")
        self.filtertable_5.setRowCount(0)
        self.filtertable_5.verticalHeader().setVisible(False)
        self.gridLayout_4.addWidget(self.filtertable_5, 0, 1, 1, 1)
        self.filterpb_5 = QtWidgets.QPushButton(self.tab_7)
        self.filterpb_5.setObjectName("filterpb_5")
        self.gridLayout_4.addWidget(self.filterpb_5, 1, 1, 1, 1)
        self.treeWidget_6 = QtWidgets.QTreeWidget(self.tab_7)
        self.treeWidget_6.setTabletTracking(False)
        self.treeWidget_6.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget_6.setAutoScroll(True)
        self.treeWidget_6.setIndentation(25)
        self.treeWidget_6.setAnimated(False)
        self.treeWidget_6.setWordWrap(False)
        self.treeWidget_6.setHeaderHidden(False)
        self.treeWidget_6.setColumnCount(11)
        self.treeWidget_6.setObjectName("treeWidget_6")
        self.treeWidget_6.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.treeWidget_6.header().setVisible(False)
        self.treeWidget_6.header().setCascadingSectionResizes(True)
        self.treeWidget_6.header().setHighlightSections(True)
        self.treeWidget_6.header().setSortIndicatorShown(False)
        self.treeWidget_6.header().setStretchLastSection(False)
        self.gridLayout_4.addWidget(self.treeWidget_6, 0, 0, 2, 1)
        self.streamtabs.addTab(self.tab_7, "")
        self.gridLayout_3.addWidget(self.streamtabs, 3, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.filenameEdit = QtWidgets.QLineEdit(self.groupBox)
        self.filenameEdit.setMaximumSize(QtCore.QSize(300, 16777215))
        self.filenameEdit.setObjectName("filenameEdit")
        self.gridLayout.addWidget(self.filenameEdit, 3, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 3, 8, 1, 1)
        self.startlabel = QtWidgets.QLabel(self.groupBox)
        self.startlabel.setObjectName("startlabel")
        self.gridLayout.addWidget(self.startlabel, 0, 0, 1, 1)
        self.startdate = QtWidgets.QDateTimeEdit(self.groupBox)
        self.startdate.setMinimumSize(QtCore.QSize(200, 0))
        self.startdate.setMaximumSize(QtCore.QSize(300, 16777215))
        self.startdate.setCalendarPopup(True)
        self.startdate.setObjectName("startdate")
        self.gridLayout.addWidget(self.startdate, 0, 1, 1, 1)
        self.browsepb = QtWidgets.QPushButton(self.groupBox)
        self.browsepb.setMaximumSize(QtCore.QSize(100, 16777215))
        self.browsepb.setObjectName("browsepb")
        self.gridLayout.addWidget(self.browsepb, 3, 2, 1, 1)
        self.stoplabel = QtWidgets.QLabel(self.groupBox)
        self.stoplabel.setObjectName("stoplabel")
        self.gridLayout.addWidget(self.stoplabel, 0, 2, 1, 1)
        self.thresholdSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.thresholdSpinBox.setMinimumSize(QtCore.QSize(100, 0))
        self.thresholdSpinBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.thresholdSpinBox.setProperty("showGroupSeparator", False)
        self.thresholdSpinBox.setSuffix("")
        self.thresholdSpinBox.setDecimals(1)
        self.thresholdSpinBox.setMaximum(10.0)
        self.thresholdSpinBox.setSingleStep(0.1)
        self.thresholdSpinBox.setProperty("value", 1.0)
        self.thresholdSpinBox.setObjectName("thresholdSpinBox")
        self.gridLayout.addWidget(self.thresholdSpinBox, 3, 5, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 3, 1, 1)
        self.stopdate = QtWidgets.QDateTimeEdit(self.groupBox)
        self.stopdate.setMinimumSize(QtCore.QSize(200, 0))
        self.stopdate.setMaximumSize(QtCore.QSize(300, 16777215))
        self.stopdate.setCalendarPopup(True)
        self.stopdate.setObjectName("stopdate")
        self.gridLayout.addWidget(self.stopdate, 0, 3, 1, 1)
        self.hdf5button = QtWidgets.QPushButton(self.groupBox)
        self.hdf5button.setObjectName("hdf5button")
        self.gridLayout.addWidget(self.hdf5button, 0, 8, 1, 1)
        self.number_of_files = QtWidgets.QLabel(self.groupBox)
        self.number_of_files.setMaximumSize(QtCore.QSize(600, 16777215))
        self.number_of_files.setText("")
        self.number_of_files.setObjectName("number_of_files")
        self.gridLayout.addWidget(self.number_of_files, 1, 0, 1, 2)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 2)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.treeWidget_2 = QtWidgets.QTreeWidget(self.tab_2)
        self.treeWidget_2.setObjectName("treeWidget_2")
        self.treeWidget_2.headerItem().setText(0, "1")
        self.gridLayout_2.addWidget(self.treeWidget_2, 3, 0, 1, 3)
        self.loadcataloguepb = QtWidgets.QPushButton(self.tab_2)
        self.loadcataloguepb.setObjectName("loadcataloguepb")
        self.gridLayout_2.addWidget(self.loadcataloguepb, 1, 2, 1, 1)
        self.filenameEdit2 = QtWidgets.QLineEdit(self.tab_2)
        self.filenameEdit2.setMaximumSize(QtCore.QSize(500, 16777215))
        self.filenameEdit2.setObjectName("filenameEdit2")
        self.gridLayout_2.addWidget(self.filenameEdit2, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.browsepb2 = QtWidgets.QPushButton(self.tab_2)
        self.browsepb2.setObjectName("browsepb2")
        self.gridLayout_2.addWidget(self.browsepb2, 0, 2, 1, 1)
        self.searchbar = QtWidgets.QLineEdit(self.tab_2)
        self.searchbar.setMaximumSize(QtCore.QSize(500, 16777215))
        self.searchbar.setObjectName("searchbar")
        self.gridLayout_2.addWidget(self.searchbar, 1, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        self.streamtabs.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "DAQ Parser"))
        self.filterpb.setText(_translate("Form", "Apply Filter"))
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.headerItem().setText(0, _translate("Form", "Channel Name"))
        self.streamtabs.setTabText(self.streamtabs.indexOf(self.tab_3), _translate("Form", "XFEL_SASE1"))
        self.filterpb_2.setText(_translate("Form", "Apply Filter"))
        self.treeWidget_3.setSortingEnabled(False)
        self.treeWidget_3.headerItem().setText(0, _translate("Form", "Channel Name"))
        self.streamtabs.setTabText(self.streamtabs.indexOf(self.tab_4), _translate("Form", "XFEL_SASE2"))
        self.filterpb_3.setText(_translate("Form", "Apply Filter"))
        self.treeWidget_4.setSortingEnabled(False)
        self.treeWidget_4.headerItem().setText(0, _translate("Form", "Channel Name"))
        self.streamtabs.setTabText(self.streamtabs.indexOf(self.tab_5), _translate("Form", "XFEL_SASE3"))
        self.filterpb_4.setText(_translate("Form", "Apply Filter"))
        self.treeWidget_5.setSortingEnabled(False)
        self.treeWidget_5.headerItem().setText(0, _translate("Form", "Channel Name"))
        self.streamtabs.setTabText(self.streamtabs.indexOf(self.tab_6), _translate("Form", "LINAC"))
        self.filterpb_5.setText(_translate("Form", "Apply Filter"))
        self.treeWidget_6.setSortingEnabled(False)
        self.treeWidget_6.headerItem().setText(0, _translate("Form", "Channel Name"))
        self.streamtabs.setTabText(self.streamtabs.indexOf(self.tab_7), _translate("Form", "KARABO"))
        self.groupBox.setTitle(_translate("Form", "Settings"))
        self.label_3.setText(_translate("Form", "Output directory:"))
        self.pushButton.setText(_translate("Form", "Create HDF5 files"))
        self.startlabel.setText(_translate("Form", "Start time:"))
        self.browsepb.setText(_translate("Form", "Browse"))
        self.stoplabel.setText(_translate("Form", "Stop time:"))
        self.label_2.setText(_translate("Form", "File size threshold (GB):"))
        self.hdf5button.setText(_translate("Form", "Get Channel List"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "DAQ Parser"))
        self.treeWidget_2.setSortingEnabled(False)
        self.loadcataloguepb.setText(_translate("Form", "Load stream catalogue"))
        self.label.setText(_translate("Form", "Stream:"))
        self.browsepb2.setText(_translate("Form", "Browse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Stream Catalogue"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
