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
import tempfile
import subprocess


# by importing QT from sgtk rather than directly, we ensure that
# the code will be compatible with both PySide and PyQt.
# from sgtk.platform.qt import QtCore, QtGui
from PySide import QtGui, QtCore
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


class PreviewLabel(QtGui.QWidget):

    clicked = QtCore.Signal()

    def __init__(self, parent=None):
        super(PreviewLabel, self).__init__(parent)
        self.setFixedSize(160, 100)
        self.__file_path = ''
        self.__preview_img = None
        self.clear_temp_thumbnail()

    def mouseReleaseEvent(self, event):
        self.clicked.emit()

    def set_file_path(self, file_path):
        self.__file_path = file_path

        output_path = self.temp_thumbnail_image_path()
        self.clear_temp_thumbnail()
        self.make_thumbnail(file_path, output_path)

        if os.path.exists(output_path):
            fp = open(output_path, 'rb')
            data = fp.read()
            fp.close()
            self.__preview_img = QtGui.QPixmap()
            self.__preview_img.loadFromData(data)
        else:
            self.__preview_img = None

        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        rect = event.rect()
        painter.save()
        painter.setPen(QtGui.QPen(QtCore.Qt.gray))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.gray))
        painter.drawRect(rect)
        painter.restore()

        if self.__preview_img:
            painter.save()
            img = self.__preview_img
            wh_ratio = rect.width()*1.0/rect.height()
            img_wh_ratio = img.width()*1.0/img.height()
            img_rect = rect.adjusted(0, 0, 0, 0)
            if wh_ratio > img_wh_ratio:
                img_rect.setWidth(rect.height()*img_wh_ratio)
            else:
                img_rect.setHeight(rect.width()/img_wh_ratio)

            img_rect = QtCore.QRect(rect.x()+(rect.width()-img_rect.width())*0.5,
                                    rect.y()+(rect.height()-img_rect.height())*0.5,
                                    img_rect.width(), img_rect.height())
            painter.drawPixmap(img_rect, img)
            painter.restore()
        else:
            painter.drawText(50, 50, 'No Preview')
        event.accept()

    @classmethod
    def temp_thumbnail_image_path(cls):
        return os.path.join(tempfile.gettempdir(), 'mx_shotgun_thumbnail.png')

    @classmethod
    def clear_temp_thumbnail(cls):
        p = cls.temp_thumbnail_image_path()
        if os.path.exists(p):
            os.remove(p)

    @classmethod
    def make_thumbnail(cls, src, out):
        p = subprocess.Popen(r'Y:\MatrixStudio\bin\ffmpeg -i "%s" -vf "select=gte(n\,0)" -vframes 1 "%s" -y' %
                             (src, out))
        p.wait()


class AppDialog(QtGui.QWidget):
    
    def __init__(self):
        super(AppDialog, self).__init__()
        self.setAcceptDrops(1)
        
        # now load in the UI that was created in the UI designer
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)
        self.file_preview_label = PreviewLabel()
        self.ui.file_info_layout.insertWidget(0, self.file_preview_label)

        # most of the useful accessors are available through the Application class instance
        # it is often handy to keep a reference to this. You can get it via the following method:
        self._app = sgtk.platform.current_bundle()
        self.ui.context_label.setText('%s' % self._app.context)
        self.ui.context_label.setStyleSheet('font-size: 18pt;')

        self._template = self._app.sgtk.templates['review_version']
        self._fields = self._app.context.as_template_fields(self._template)
        self._fields['Step'] = self._app.context.step['name']
        self._fields['Entity'] = self._app.context.entity['name']

        self.ui.cancel_button.clicked.connect(self.close)
        self.ui.submit_button.clicked.connect(self.on_submit_clicked)
        self.ui.name_editor.textChanged.connect(self.on_name_editor_changed)
        self.file_preview_label.clicked.connect(self.on_file_preview)

    def set_file_path(self, path):
        self.ui.file_path_label.setText(path)
        self._fields['ext'] = path.split('.')[-1]
        self.on_name_editor_changed(self.ui.name_editor.text())
        self.file_preview_label.set_file_path(path)

    def on_file_preview(self):
        file_path = self.ui.file_path_label.text()
        if os.path.exists(file_path):
            os.startfile(file_path)

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
            'code': self._fields['name'],
            'sg_uploaded_movie': {
                'local_path': dst_file,
                'name': self._fields['name']
            },
            'sg_path_to_movie': dst_file
        }
        new_version = self._app.shotgun.create('Version', data)

        thumbnail = PreviewLabel.temp_thumbnail_image_path()
        if os.path.exists(thumbnail):
            self._app.shotgun.upload_thumbnail('Version', new_version['id'], thumbnail)

        return new_version

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

