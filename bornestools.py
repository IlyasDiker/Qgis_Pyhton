# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bornestools.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_bornesGUI(object):U
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(401, 261)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.field_X = QtWidgets.QLineEdit(Form)
        self.field_X.setObjectName("field_X")
        self.horizontalLayout_2.addWidget(self.field_X)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.field_Y = QtWidgets.QLineEdit(Form)
        self.field_Y.setObjectName("field_Y")
        self.horizontalLayout_4.addWidget(self.field_Y)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.ButtonZoom = QtWidgets.QPushButton(Form)
        self.ButtonZoom.setObjectName("ButtonZoom")
        self.verticalLayout.addWidget(self.ButtonZoom)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.fieldPreviewX = QtWidgets.QLineEdit(Form)
        self.fieldPreviewX.setObjectName("fieldPreviewX")
        self.horizontalLayout_3.addWidget(self.fieldPreviewX)
        self.fieldPreviewY = QtWidgets.QLineEdit(Form)
        self.fieldPreviewY.setObjectName("fieldPreviewY")
        self.horizontalLayout_3.addWidget(self.fieldPreviewY)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Zoom to Coords"))
        self.label_2.setText(_translate("Form", "X"))
        self.label_3.setText(_translate("Form", "Y"))
        self.ButtonZoom.setText(_translate("Form", "Zoom to Coords"))
        self.label_4.setText(_translate("Form", "X"))
        self.label_5.setText(_translate("Form", "Y"))
        self.pushButton.setText(_translate("Form", "Add"))

