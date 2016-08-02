# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Tue Aug 02 11:28:27 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(647, 223)
        self.verticalLayout_3 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.nameLabel = QtGui.QLabel(Dialog)
        self.nameLabel.setObjectName("nameLabel")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.nameLabel)
        self.name_editor = QtGui.QLineEdit(Dialog)
        self.name_editor.setObjectName("name_editor")
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.name_editor)
        self.descriptionLabel = QtGui.QLabel(Dialog)
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.descriptionLabel)
        self.desc_editor = QtGui.QPlainTextEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.desc_editor.sizePolicy().hasHeightForWidth())
        self.desc_editor.setSizePolicy(sizePolicy)
        self.desc_editor.setMaximumSize(QtCore.QSize(16777215, 100))
        self.desc_editor.setObjectName("desc_editor")
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.desc_editor)
        self.file_path_label = QtGui.QLabel(Dialog)
        self.file_path_label.setText("")
        self.file_path_label.setObjectName("file_path_label")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.file_path_label)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.preview_label = QtGui.QLabel(Dialog)
        self.preview_label.setText("")
        self.preview_label.setObjectName("preview_label")
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.preview_label)
        self.verticalLayout_3.addLayout(self.formLayout_2)
        self.line = QtGui.QFrame(Dialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.submit_button = QtGui.QPushButton(Dialog)
        self.submit_button.setObjectName("submit_button")
        self.horizontalLayout.addWidget(self.submit_button)
        self.cancel_button = QtGui.QPushButton(Dialog)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "The Current Sgtk Environment", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("Dialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.descriptionLabel.setText(QtGui.QApplication.translate("Dialog", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.submit_button.setText(QtGui.QApplication.translate("Dialog", "Submit", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel_button.setText(QtGui.QApplication.translate("Dialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc
