# coding: utf-8
#
# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
import os
import datetime


# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
# from PySide import QtGui, QtCore
from .ui.dialog import Ui_Dialog


def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # different types of windows. By using these methods, your windows will be correctly
    # decorated and handled in a consistent fashion by the system. 
    
    # we pass the dialog class to this method and leave the actual construction
    # to be carried out by toolkit.
    app_instance.engine.show_dialog("Submit Version", app_instance, AppDialog)
    

class AppDialog(QtGui.QWidget):
    
    def __init__(self):
        super(AppDialog, self).__init__()
        self.setAcceptDrops(1)
        
        # now load in the UI that was created in the UI designer
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)
        
        # most of the useful accessors are available through the Application class instance
        # it is often handy to keep a reference to this. You can get it via the following method:
        self._app = sgtk.platform.current_bundle()

        self._template = self._app.sgtk.templates['review_version']
        self._fields = self._app.context.as_template_fields(self._template)
        self._fields['Step'] = self._app.context.step['name']
        self._fields['Entity'] = self._app.context.entity['name']

        self.ui.cancel_button.clicked.connect(self.close)
        self.ui.submit_button.clicked.connect(self.on_submit_clicked)
        self.ui.name_editor.textChanged.connect(self.on_name_editor_changed)

    def set_file_path(self, path):
        self.ui.file_path_label.setText(path)
        self._fields['ext'] = path.split('.')[-1]
        self.on_name_editor_changed(self.ui.name_editor.text())

    def on_name_editor_changed(self, text):
        if text == '':
            self.ui.preview_label.setText('Error: name is empty!')
        else:
            self.__update_fields(text)
            path = self._template.apply_fields(self._fields)
            self.ui.preview_label.setText(path)

    def on_submit_clicked(self):
        self.setDisabled(1)
        name = self.ui.name_editor.text()
        if name == '':
            QtGui.QMessageBox.critical(self, 'error', 'Name is empty!')
            self.setEnabled(1)
            return

        orig_file = self.ui.file_path_label.text()
        if not os.path.isfile(orig_file):
            QtGui.QMessageBox.critical(self, 'error', 'No valid file!')
            self.setEnabled(1)
            return

        self.__update_fields(name)
        path_at_server = self._template.apply_fields(self._fields)
        if os.path.exists(path_at_server):
            QtGui.QMessageBox.critical(self, 'error', '"%s" already exists!' % path_at_server)
            self.setEnabled(1)
            return

        try:
            version = self.create_version(orig_file, path_at_server)
            QtGui.QMessageBox.information(self, 'info', 'Version is created successfully!\n\n%s' % str(version))
            self.close()
        except Exception as err:
            QtGui.QMessageBox.critical(self, 'error', err.message)
            self.setEnabled(1)

    def create_version(self, src_file, dst_file):
        dst_dir = os.path.dirname(dst_file)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        sgtk.util.filesystem.copy_file(src_file, dst_file)
        data = {
            'project': self._app.context.project,
            'entity': self._app.context.entity,
            'sg_task': self._app.context.task,
            'description': self.ui.desc_editor.toPlainText(),
            'sg_uploaded_movie': {
                'local_path': dst_file,
                'name': self._fields['name']
            },
            'sg_path_to_movie': dst_file
        }
        return self._app.shotgun.create('Version', data)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/uri-list'):
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = []
        for i in event.mimeData().urls():
            files.append(i.toLocalFile())
        if len(files) > 0:
            self.set_file_path(files[0])

    def __update_fields(self, name):
        self._fields['name'] = name
        self._fields['timestamp'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
