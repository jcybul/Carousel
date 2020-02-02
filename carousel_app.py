import gi
import sys
from gi.repository import GObject
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import RPi.GPIO as GPIO 
import time
import MySQLdb
from time import sleep
import time    
import csv
import datetime
from threading import Thread
from multiprocessing import Process
from mfrc522 import SimpleMFRC522

in1 = 12
in2 = 13
in3 = 16
in4 = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(23,GPIO.IN,pull_up_down = GPIO.PUD_UP)
GPIO.setup(18,GPIO.IN,pull_up_down = GPIO.PUD_UP)
global count 
count = 0

global count2 
count2 = 0

def countPulse(channel):
    global count
    count= count+1

def countPulse2(channel):
    global count2
    count2= count2+1

def irrigate():
    print("in irrigation")
    pot_count = 1
    reader = SimpleMFRC522()
    print ("reading")
    GPIO.add_event_detect(18,GPIO.FALLING, callback = countPulse2)
    GPIO.add_event_detect(23,GPIO.FALLING, callback = countPulse)
    
    while(pot_count < 24):
        pot_count = pot_count+1
        global count,count2 
        count =0
        count2 = 0
        print(" in while")
        try:
            id,rfid = reader.read()
            print(rfid)
        except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
            print("Keyboard interrupt")
            print(rfid)
        finally:
    
         if(int(rfid) > 0 and int(rfid) < 25): 
             
            db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                             user="root",         # your username
                             passwd="iqp2020",  # your password
                             db="mydb")    
            cur = db.cursor(MySQLdb.cursors.DictCursor)
            try:
                query = "SELECT * from Carousel where barrel_num = %s"
                cur.execute(query,[rfid])
                result = cur.fetchall()
                for r in result:
                    q = (r['Water_Liters'])
                    ec = (r['Water_ec'])
            finally:
                db.close()

            if(ec == 2.3):
                print(rfid + " ec 2.3")
                while(count/(60 *7.5) < q):
                    print(count)
                    irrigate_open(ec)
                irrigate_close(ec)
            elif ( ec == 0):
               
                while(count2/(60 *7.5) < q):
                    print(count2/(60*7.5))
                    irrigate_open(ec)
                irrigate_close(ec)
                print (rfid + " ec 0")            
def irrigate_open(ec):
    if(ec == 0):
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
    elif(ec == 0):
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)
def irrigate_close(ec):
    if(ec == 0):
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
    elif(ec == 0):
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)


def setToolTip():
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="iqp2020",  # your password
                     db="mydb")    
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur2 = db.cursor(MySQLdb.cursors.DictCursor)
    for x in range (1, 25):
        query2 = "Select Height,date_recorded from Plant_records where barrel_num = %s and date_recorded = (SELECT MAX(date_recorded) from Plant_records where barrel_num = %s group by barrel_num)"
        query = "SELECT *  from Carousel WHERE Barrel_num = %s"
        cur.execute(query,[str(x)])
        cur2.execute(query2,([str(x)],[str(x)]))
        result2 = cur2.fetchall()
        result = cur.fetchall()
        sstring = "pot_" +str(x)
        s =""
        temp = builder.get_object(sstring)
        for t in result:
            print("Number"+ str(t['Barrel_num']))
            s = " Pot Number: " + str(t['Barrel_num']) +" \n Date Planted: " + str(t['Date_planted'])+"\n Seed type: " + str(t['Seed_type']) +" \n Water EC: " + str(t['Water_ec']) +" \n Quantity: " + str(t['Water_Liters'])
        for f in result2: 
            s =  s + "\n Recorded Height(cm): "+ str(f['Height'])  + "\n Height recorded on: " + str(f['date_recorded'])
        temp.set_tooltip_text(s)

class Handler:
    sw = Gtk.Switch()
    sw.set_active(True)
    sw2 = Gtk.Switch()
    sw2.set_active(True)
    def onDestroy(self, *args):
        print("cleanup")
        GPIO.cleanup()
        Gtk.main_quit()
    
    def irr(self,widget):
        irrigate()
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
            comments.set_text("")
            b.set_text("")
            h.set_text("")
            setToolTip()
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
            water_ec.set_text("")
            q_water.set_text("")
            setToolTip()
            db.close()

    def pumpOneOpen(self,sw,data):
        
        if sw.get_active(): 
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
        else:
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            time.sleep(5) 

    def pumpTwoOpen(self,sw2,data):
        if sw2.get_active():
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
            time.sleep(5)
        else: 
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            time.sleep(5)

    def exportCsv(self,widget):


        fileName = 'CSV/Carousel' +  time.strftime('%Y-%m-%d %H-%M-%S')
        db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="iqp2020",  # your password
                     db="mydb")    
        cur = db.cursor()

        query = "SELECT * from Plant_records"
        try:
            cur.execute(query)
            result = cur.fetchall()

            for r in result:
                print(r)
                with open(fileName +'.csv', 'a') as Carousel:
                    employee_writer = csv.writer(Carousel, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    employee_writer.writerow([r[0],r[1],r[2]])
        finally:
            cur.close
            db.close



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


irrigation = 0
now = datetime.datetime.now()
seven_am = now.replace(hour=11, minute=52, second=0, microsecond=0)

if datetime.datetime.now == seven_am:
    print("timeeeeee")
count2 = 0


def testthread():
    count2 = 0
    while(1):
        count2 += 1
        print("succes")
        if count2 > 200:
            break
Process(target=testthread()).start()
Process(target=Gtk.main()).start()


#Gtk.main()
GPIO.cleanup()






