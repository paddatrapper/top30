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

        self.setGeometry(300, 300, 480, 310)
        self.setWindowTitle("Top 30 Creator")
        self.show()

    def on_add_clip_clicked(self):
        filenames  = QtGui.QFileDialog.getOpenFileNames(self, "Add clip", "/home/kyle",
                "Audio(*.mp3, *.ogg);;All Files(*)")
        for f in filenames:
            self.add_clip(filenames)

    def on_move_up_clicked(self):
        #item = self.get_selected_clip()
        #if not item == None:
        #    previous = self.clip_list.iter_previous(item)
        #    if not previous == None:
        #        self.clip_list.move_before(item, previous)
        print("on move clicked")

    def on_move_down_clicked(self):
        #item = self.get_selected_clip()
        #if not item == None:
        #    next_item = self.clip_list.iter_next(item)
        #    if not next_item == None:
        #        self.clip_list.move_after(item, next_item)
        print("on move down clicked")

    def on_delete_clip_clicked(self):
        #item = self.get_selected_clip()
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
        #clip_list_view = self.builder.get_object("view_clip_list")
        #model, item = clip_list_view.get_selection().get_selected()
        #return item
        print("get selected clip >>> SHOULD NOT BE CALLED")


    def add_clip(self, filename):
        #try:
        #    time = self.creator.get_start_time(filename)/1000
        #    time_string = "%02d:%02.1f" % (time / 60, time % 60)
        #    self.clip_list.append([True, filename, time_string])
        #except:
        #    self.clip_list.append([False, filename, None])
        print("add clip")
    
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
        print(filename)
        return filename

class UserInterface:
    def run():
        app = QtGui.QApplication(sys.argv)
        ex = MainWindow()
        sys.exit(app.exec_())
