import gi
from gi.repository import GObject
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import RPi.GPIO as GPIO 
import time
import MySQLdb
from time import sleep
import time    

in1 = 2
in2 = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)

def setToolTip():
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="iqp2020",  # your password
                     db="mydb")    
    cur = db.cursor(MySQLdb.cursors.DictCursor)

    for x in range (1, 24):
        query = "SELECT *  from Carousel WHERE Barrel_num = %s"
        cur.execute(query,[str(x)])
        result = cur.fetchall()
        sstring = "pot_" +str(x)
        temp = builder.get_object(sstring)
        for t in result:
            print(t) 
        s = "pot_"+str(x) +" " +str(t)   
        temp.set_tooltip_text(s)

class Handler:
    sw = Gtk.Switch()
    sw.set_active(True)
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onButtonPressed(self, widget):
        now = time.strftime('%Y-%m-%d %H-%M-%S')
        db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="iqp2020",  # your password
                     db="mydb")        # name of the data base

        cur = db.cursor()
        
        # Use all the SQL you like
        try:
            pot = (b.get_text())
            he = (h.get_text())
            com = comments.get_text()
            #if isinstance(b.get_text(),int) and isinstance(h.get_text(),int):
            sql = "INSERT INTO Plant_records (barrel_num, date_recorded,Height,Comments) VALUES (%s,%s ,%s,%s)"
            cur.execute(sql, (pot,now ,he,com))
            db.commit()
            print("test")
        except:
            print('Error:')
        finally:
            db.close()
    def buttonUpdate(self,widget):
        db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="iqp2020",  # your password
                     db="mydb")    
        cur = db.cursor()

        try:
             
             new_water_ec = water_ec.get_text()
             new_water_q = q_water.get_text()
             combo_val = combo.get_active_text()
             print(combo_val)
             query = "UPDATE Carousel SET Water_ec = %s , Water_Liters = %s WHERE Barrel_num = %s"
             cur.execute(query,(new_water_ec,new_water_q,combo_val))
             db.commit()
             print("Row updates")
        except:
            print("ERROR: **********")
        finally:
            db.close()

    def pumpOneOpen(self,sw,data):
        if sw.get_active():
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
            time.sleep(5)
        else: 
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            time.sleep(5)
builder = Gtk.Builder()
builder.add_from_file("example.glade")

builder.connect_signals(Handler())
setToolTip()

comments = builder.get_object("comment_entry")
combo = builder.get_object("combo_box1")
b = builder.get_object("b_entry")
water_ec = builder.get_object("water_ec")
q_water = builder.get_object("q_water")
h = builder.get_object("h_entry")
window = builder.get_object("window1")
window.show_all()

Gtk.main()







