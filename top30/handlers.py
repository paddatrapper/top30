from top30Creator import Top30Creator

import sys
from PyQt4 import QtCore, QtGui, uic

class MainWindow(QtGui.QMainWindow):
    creator = Top30Creator("config.yaml")

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("main_window.ui", self) 
        self.init_ui()

    def init_ui(self):
        self.btn_add_clip.clicked.connect(self.on_add_clip_clicked)
        self.btn_move_up.clicked.connect(self.on_move_up_clicked)
        self.btn_move_down.clicked.connect(self.on_move_down_clicked)
        self.btn_delete_clip.clicked.connect(self.on_delete_clip_clicked)
        self.btn_create.clicked.connect(self.on_create_clip_clicked)

        self.load_settings()
        self.init_table()

        self.move(200, 100)
        self.setWindowTitle("Top 30 Creator")
        self.show()

    def init_table(self):
        header = ["Type", "Filename", "Start"]
        self.clip_model = QtGui.QStandardItemModel()
        self.clip_model.setHorizontalHeaderLabels(header)
        self.clip_view.setModel(self.clip_model)

        self.clip_view.horizontalHeader().setStretchLastSection(True)
        self.clip_view.resizeColumnsToContents()
        self.clip_view.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.clip_view.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

    def on_add_clip_clicked(self):
        filenames  = QtGui.QFileDialog.getOpenFileNames(self, "Add clip", "/home/kyle/Documents/projects/top30/songs",
                "Audio(*.mp3, *.ogg);;All Files(*)")
        for f in filenames:
            self.add_clip(f)
        self.clip_view.resizeColumnsToContents()

    def on_move_up_clicked(self):
        item = self.get_selected_clip()
        if not item == None and item.row() > 0:
            self.clip_model.insertRow(item.row() - 1)
            item_row = item.sibling(item.row() + 1, 0)
            previous_row = item.sibling(item.row() - 1, 0)
            previous = previous_row.row()
            self.swap(item_row, previous_row)
            self.clip_view.selectRow(previous)

    def on_move_down_clicked(self):
        item = self.get_selected_clip()
        if not item == None and item.row() < self.clip_model.rowCount():
            self.clip_model.insertRow(item.row())
            item_row = item.sibling(item.row() + 2, 0)
            next_row = item.sibling(item.row(), 0)
            self.swap(item_row, next_row)

    def on_delete_clip_clicked(self):
        item = self.get_selected_clip()
        #if not item == None:
        #    self.clip_list.remove(item)
        print("on delete clip clicked")

    def on_create_clip_clicked(self):
        self.save_settings()
        rundown_name = self.save_clip()
        if not rundown_name:
            return
        rundown_name = rundown_name[:-1]

        #it = self.clip_list.get_iter_first()
        #song = self.clip_list[it][1]
        #i = 1
        #while not it == None:
        #    clip = self.clip_list[it][1]
        #    if i == 1:
        #        rundown = self.creator.get_start(clip)
        #    elif i == len(self.clip_list) - 1:
        #        rundown = self.creator.add_end(clip, rundown)
        #    elif self.clip_list[it][0]:
        #        rundown = self.creator.add_song(clip, rundown)
        #    else:
        #        rundown = self.creator.add_voice(clip, rundown)
        #    it = self.clip_list.iter_next(it)
        #    i += 1
        #self.creator.export(rundown_name, "mp3", rundown)
        QtGui.QMessageBox.information(self, "Complete", 
                "Clip " + rundown_name + " created.")
        print("on create clip clicked")

    def get_selected_clip(self):
        row = self.clip_view.selectionModel().selectedRows()
        if len(row) == 0:
            return None
        return row[0]

    def swap(self, source, destination):
        source_row = source.row()
        destination_row = destination.row()
        while destination.isValid():
            self.clip_model.setData(destination, source.data())
            destination = destination.sibling(
                    destination.row(), destination.column() + 1)
            source = source.sibling(source.row(), source.column() + 1)

        self.clip_model.removeRow(source_row)

    def add_clip(self, filename):
        try:
            time = self.creator.get_start_time(filename)/1000
            time_string = "%02d:%02.1f" % (time / 60, time % 60)
            row = [QtGui.QStandardItem("Song"), 
                    QtGui.QStandardItem(filename), 
                    QtGui.QStandardItem(time_string)]
        except:
            row = [QtGui.QStandardItem("Voice"), 
                    QtGui.QStandardItem(filename), 
                    QtGui.QStandardItem(None)]
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
