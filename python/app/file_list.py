# coding: utf-8
# ----------------------------------------------------------------------------------------------------------------------

import os

import sgtk
# from sgtk.platform.qt import QtCore, QtGui
from PySide import QtGui, QtCore


# ----------------------------------------------------------------------------------------------------------------------

class MxSGFileListData(object):

    def __init__(self, file_path):
        self.__file_path = file_path
        self.__new_name = ''
        self.__ext = ''
        self.__thumbnail = None

        file_names = os.path.basename(file_path).split('.')
        if len(file_names) > 1:
            self.__ext = file_names.pop(-1)
            self.set_name('.'.join(file_names))
        else:
            self.set_name(file_names[0])

    def set_name(self, name):
        app = sgtk.platform.current_bundle()


    def make_thumbnail(self):
        pass






class MxSGFileItemWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(MxSGFileItemWidget, self).__init__(parent)
        form_layout = QtGui.QFormLayout()




if __name__ == '__main__':
    app = QtGui.QApplication([])
    print QtGui.QImageReader.imageFormat(r"E:\workspace\python\shotgun\apps\mx-local-version-submit\resources\build_resources.py")
    playback_label = sgtk.platform.import_framework("tk-framework-qtwidgets", "playback_label")

    # construct label object
    label =  playback_label.ShotgunPlaybackLabel(parent_widget)
    app.exec_()











class MxSGFileListDelegate(QtGui.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(MxSGFileListDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        if option.state & QtGui.QStyle.State_HasFocus:
            option.state = option.state ^ QtGui.QStyle.State_HasFocus

        delegate_painter = self.__field.delegate_painter
        if delegate_painter:
            if option.state & QtGui.QStyle.State_Selected:
                painter.fillRect(option.rect, option.palette.highlight())
            else:
                painter.fillRect(option.rect, index.data(QtCore.Qt.BackgroundRole))

                self.initStyleOption(option, index)
                style = QtGui.QApplication.style()
                style.drawControl(QtGui.QStyle.CE_ItemViewItem, option, painter)
        else:
            super(MxSGFileListDelegate, self).paint(painter, option, index)

    def createEditor(self, parent, option, index):
        if not self.__field.readonly:
            return self.__field.create_editor(parent)
        else:
            return None

    def setEditorData(self, editor, model_index):
        data = model_index.data(QtCore.Qt.UserRole)
        editor.set_value(data)

    def setModelData(self, editor, model, model_index):
        model.setData(model_index, editor.value(), QtCore.Qt.UserRole)


class MxSGFileListWidget(QtGui.QListWidget):

    def __init__(self, parent=None):
        super(MxSGFileListWidget, self).__init__(parent)
        self.setAcceptDrops(1)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(u'text/uri-list'):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if self.ui.to_be_removed_listwgt.count() > 0:
            dependencies = []
            for sel in self.ui.to_be_removed_listwgt.selectedItems():
                dependencies.append(sel.text())

            files = []
            for i in event.mimeData().urls():
                files.append(i.toLocalFile())
            if not len(files):
                self.__cleaner_thread.setFiles(files)
                self.__cleaner_thread.setDependencies(dependencies)
                self.__cleaner_thread.run()
                self.ui.cancel_button.setEnable(1)
        else:
            self.ui.log_texteditor.append(u'Dependency list is empty.')