from top30Creator import Top30Creator
from clipList import ClipListModel

import sys
from PyQt4 import QtCore, QtGui, uic

class MainWindow(QtGui.QMainWindow):
    creator = Top30Creator()

    def __init__(self):
        super(MainWindow, self).__init__()
        if getattr(sys, 'Frozen', False):
            ui_file = sys.__MEIPASS + "/main_window.ui"
        else:
            ui_file = __file__[:-len("handlers.py")] + "main_window.ui"
        uic.loadUi(ui_file, self) 
        self.init_ui()

    def init_ui(self):
        self.btn_add_clip.clicked.connect(self.on_add_clip_clicked)
        self.btn_move_up.clicked.connect(self.on_move_up_clicked)
        self.btn_move_down.clicked.connect(self.on_move_down_clicked)
        self.btn_delete_clip.clicked.connect(self.on_delete_clip_clicked)
        self.btn_create.clicked.connect(self.on_create_clip_clicked)

        self.act_new.triggered.connect(self.on_new_clicked)
        self.act_exit.triggered.connect(QtGui.qApp.quit)
        self.act_create_clip.triggered.connect(self.on_create_clip_clicked)
        self.act_add_clip.triggered.connect(self.on_add_clip_clicked)
        self.act_delete_clip.triggered.connect(self.on_delete_clip_clicked)

        self.load_settings()
        self.init_table()

        self.move(200, 100)
        self.setWindowTitle("Top 30 Creator")
        self.show()

    def init_table(self):
        self.clip_model = ClipListModel()
        self.clip_view.setModel(self.clip_model)

    def on_new_clicked(self):
        self.init_table()

    def on_add_clip_clicked(self):
        filenames  = QtGui.QFileDialog.getOpenFileNames(self, "Add clip", "/home/kyle/Documents/projects/top30/songs",
                "Audio(*.mp3, *.ogg);;All Files(*)")
        for f in filenames:
            self.add_clip(f)
        self.clip_view.resizeColumnsToContents()

    def on_move_up_clicked(self):
        item = self.get_selected_clip()
        if not item == None and item.row() > 0:
            self.clip_model.moveRows(QtCore.QModelIndex(), item.row(), 
                    item.row(), QtCore.QModelIndex(), item.row() - 1)

    def on_move_down_clicked(self):
        item = self.get_selected_clip()
        if not item == None and item.row() < self.clip_model.rowCount() - 1:
            self.clip_model.moveRows(QtCore.QModelIndex(), item.row() + 1, 
                    item.row() + 1, QtCore.QModelIndex(), item.row())

    def on_delete_clip_clicked(self):
        item = self.get_selected_clip()
        if not item == None:
            self.clip_model.removeRow(item.row())

    def on_create_clip_clicked(self):
        if self.clip_model.rowCount() == 0:
            QtGui.QMessageBox.warning(self, "No Clips", 
                    "Please add clips to use")
            return

        self.save_settings()
        rundown_name = self.save_clip()
        if not rundown_name:
            return
        rundown_name = rundown_name[:-1]

        item = self.clip_model.createIndex(-1, 1)
        item = item.sibling(item.row() + 1, item.column()) # Makes it able to read the data
        while item.isValid():
            clip = item.data()
            clip_type = item.sibling(item.row(), item.column() - 1).data()
            if item.row() == 0:
                rundown = self.creator.get_start(clip)
            elif item.row() == self.clip_model.rowCount() - 1:
                rundown = self.creator.add_end(clip, rundown)
            elif clip_type == "Song":
                rundown = self.creator.add_song(clip, rundown)
            else:
                rundown = self.creator.add_voice(clip, rundown)
            item = item.sibling(item.row() + 1, item.column())
        self.creator.export(rundown_name, "mp3", rundown)
        QtGui.QMessageBox.information(self, "Complete", 
                "Clip " + rundown_name + " created.")

    def get_selected_clip(self):
        row = self.clip_view.selectionModel().selectedRows()
        if len(row) == 0:
            return None
        return row[0]

    def add_clip(self, filename):
        try:
            time = self.creator.get_start_time(filename)/1000
            time_string = "%02d:%02.1f" % (time / 60, time % 60)
            row = ["Song", filename, time_string]
        except:
            row = ["Voice", filename, None]
        self.clip_model.appendRow(row)
    
    def load_settings(self):
        clip_length = str(self.creator.get_song_length()/1000)
        voice_begin_overlap = str(self.creator.get_voice_begin_overlap()/1000)
        voice_end_overlap = str(self.creator.get_voice_end_overlap()/1000)
        self.txt_song_length.setText(clip_length)
        self.txt_voice_start.setText(voice_begin_overlap)
        self.txt_voice_end.setText(voice_end_overlap)

    def save_settings(self):
        clip_length = float(self.txt_song_length.text()) * 1000
        self.creator.set_song_length(clip_length)
        voice_begin_overlap = float(self.txt_voice_start.text()) * 1000
        self.creator.set_voice_begin_overlap(voice_begin_overlap)
        voice_end_overlap = float(self.txt_voice_end.text()) * 1000
        self.creator.set_voice_end_overlap(voice_end_overlap)

    def save_clip(self):
        filename  = QtGui.QFileDialog.getSaveFileName(self, "Add clip", "/home",
                "Audio (*.mp3, *.ogg)")
        return filename
    
class UserInterface:
    def run():
        app = QtGui.QApplication(sys.argv)
        ex = MainWindow()
        sys.exit(app.exec_())
