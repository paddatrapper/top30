import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindowHandler:
    clip_type = {"voice": 0, "song": 1}

    def __init__(self, builder):
        self.builder = builder
        self.clip_list = builder.get_object("view_clip_list")
        columns = {"Position": Gtk.CellRendererText(), "Name": Gtk.CellRendererText(), 
                "Artist": Gtk.CellRendererText(), "Song": Gtk.CellRendererToggle(), 
                "Start": Gtk.CellRendererText()}

        list_clip_type = Gtk.ListStore(str)
        for t in self.clip_type.keys():
            list_clip_type.append([t])

        for i, title in enumerate(["Position","Song", "Name", "Artist", "Start"]):
            if title == "Song":
                column = Gtk.TreeViewColumn(title, columns[title], active=i)
            else:
                column = Gtk.TreeViewColumn(title, columns[title], text=i)
            self.clip_list.append_column(column)

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onClipListDoubleClick(self, *args):
        print("double click")

    def onAddClipClicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", 
                self.builder.get_object("mainWindow"), Gtk.FileChooserAction.OPEN,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.add_clip(dialog.get_filename())
        dialog.destroy()

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

    def add_clip(self, file_name):
        print(file_name)
