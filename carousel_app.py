import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
    
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onButtonPressed(self, widget):
        b = Gtk.Builder()
        b.add_from_file("window2.glade")
        win = b.get_object("window2")
        win.show_all()

    def onImagePressed(self,widget,udata):
        b = Gtk.Builder()
        b.add_from_file("window2.glade")
        win = b.get_object("window2")
        win.show_all()

builder = Gtk.Builder()
builder.add_from_file("example.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
window.show_all()

Gtk.main()
