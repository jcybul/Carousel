import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Main(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="CIS")
        self.set_default_size(500,500)
        self.box1 = Gtk.Box(spacing = 10)
        

        self.button1 = Gtk.Button(label="Pump 1")
        self.button1.connect("clicked",self.click_b)
    
        self.add(self.box1)
        self.box1.add(self.button1)
        
        self.button2 = Gtk.Button(label = "Pump2")
        self.button2.connect("clicked",self.click_b)
        self.box1.add(self.button2)

    def click_b(self,widget):
        print("clicked")
win = Main()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

