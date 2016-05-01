from lib.top30Creator import Top30Creator

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindowHandler:
    clip_type = {"voice": 0, "song": 1}
    creator = Top30Creator("config.yaml")

    def __init__(self, builder):
        self.builder = builder
        self.load_settings()
        self.clip_list = builder.get_object("list_clips")
        clip_list_view = builder.get_object("view_clip_list")
        columns = {"Name": Gtk.CellRendererText(), "Song": Gtk.CellRendererToggle(), 
                "Start": Gtk.CellRendererText()}

        list_clip_type = Gtk.ListStore(str)
        for t in self.clip_type.keys():
            list_clip_type.append([t])

        for i, title in enumerate(["Song", "Name", "Start"]):
            if title == "Song":
                column = Gtk.TreeViewColumn(title, columns[title], active=i)
            else:
                column = Gtk.TreeViewColumn(title, columns[title], text=i)
            clip_list_view.append_column(column)

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onAddClipClicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", 
                self.builder.get_object("mainWindow"), Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        dialog.set_select_multiple(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            for f in dialog.get_filenames():
                self.add_clip(f)
        dialog.destroy()

    def onMoveClipUpClicked(self, widget):
        item = self.get_selected_clip()
        if not item == None:
            previous = self.clip_list.iter_previous(item)
            if not previous == None:
                self.clip_list.move_before(item, previous)

    def onMoveClipDownClicked(self, widget):
        item = self.get_selected_clip()
        if not item == None:
            next_item = self.clip_list.iter_next(item)
            if not next_item == None:
                self.clip_list.move_after(item, next_item)

    def onDeleteClipClicked(self, widget):
        item = self.get_selected_clip()
        if not item == None:
            self.clip_list.remove(item)

    def onCreateClipClicked(self, widget):
        self.save_settings()
        rundown_name = self.save_clip()
        if not rundown_name:
            return

        it = self.clip_list.get_iter_first()
        song = self.clip_list[it][1]
        i = 1
        while not it == None:
            clip = self.clip_list[it][1]
            if i == 1:
                rundown = self.creator.get_start(clip)
            elif i == len(self.clip_list) - 1:
                rundown = self.creator.add_end(clip, rundown)
            elif self.clip_list[it][0]:
                rundown = self.creator.add_song(clip, rundown)
            else:
                rundown = self.creator.add_voice(clip, rundown)
            it = self.clip_list.iter_next(it)
            i += 1
        self.creator.export(rundown_name, "mp3", rundown)
        self.builder.get_object("bff_status").set_text("Complete", len("Complete"))

    def add_filters(self, dialog):
        fftr_audio = Gtk.FileFilter()
        fftr_audio.set_name("Audio Files")
        fftr_audio.add_mime_type("audio/ogg")
        fftr_audio.add_mime_type("audio/mp3")
        dialog.add_filter(fftr_audio)

        fftr_all = Gtk.FileFilter()
        fftr_all.set_name("All Files")
        fftr_all.add_pattern("*")
        dialog.add_filter(fftr_all)

    def get_selected_clip(self):
        clip_list_view = self.builder.get_object("view_clip_list")
        model, item = clip_list_view.get_selection().get_selected()
        return item


    def add_clip(self, filename):
        try:
            time = self.creator.get_start_time(filename)/1000
            time_string = "%02d:%02.1f" % (time / 60, time % 60)
            self.clip_list.append([True, filename, time_string])
        except:
            self.clip_list.append([False, filename, None])
    
    def load_settings(self):
        clip_length = str(self.creator.get_song_length()/1000)
        self.builder.get_object("txt_clip_length").set_text(clip_length)
        voice_begin_overlap = str(self.creator.get_voice_begin_overlap()/1000)
        self.builder.get_object("txt_voice_intro").set_text(voice_begin_overlap)
        voice_end_overlap = str(self.creator.get_voice_end_overlap()/1000)
        self.builder.get_object("txt_voice_outro").set_text(voice_end_overlap)

    def save_settings(self):
        clip_length = float(self.builder.get_object("txt_clip_length").get_text()) * 1000
        self.creator.set_song_length(clip_length)
        voice_begin_overlap = float(self.builder.get_object("txt_voice_intro").get_text()) * 1000
        self.creator.set_voice_begin_overlap(voice_begin_overlap)
        voice_end_overlap = float(self.builder.get_object("txt_voice_outro").get_text()) * 1000
        self.creator.set_voice_end_overlap(voice_end_overlap)

    def save_clip(self):
        dialog = Gtk.FileChooserDialog("Please choose a file", 
                self.builder.get_object("mainWindow"), Gtk.FileChooserAction.SAVE,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
        else:
            filename = ""
        dialog.destroy()
        return filename

