from ui.handlers import MainWindowHandler

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class UserInterface:
    def run():
        builder = Gtk.Builder()
        builder.add_from_file("ui/mainWindow.glade")
        main_window_handler = MainWindowHandler(builder)
        builder.connect_signals(main_window_handler)
        window = builder.get_object("mainWindow")
        window.show_all()
        Gtk.main()
