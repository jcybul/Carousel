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
def GPIOsetup(): 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(in1,GPIO.OUT)
    GPIO.setup(in2,GPIO.OUT)
    GPIO.setup(in3,GPIO.OUT)
    GPIO.setup(in4,GPIO.OUT)
    GPIO.setup(4,GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.setup(17,GPIO.IN,pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(4,GPIO.FALLING, callback = countPulse2)
    GPIO.add_event_detect(17,GPIO.FALLING, callback = countPulse)


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


GPIOsetup()
def irrigate():
   # print("in irrigation")
       pot_count = 0
       
   # print ("reading")
   # while(pot_count < 2):
       
       while(pot_count < 2):
        GPIO.cleanup()   
        reader = SimpleMFRC522()  
        print("the Pot_count is: " + str(pot_count))
        global count,count2 
       
       
        try:
            print(" Waiting to read ")
            id,rfid = reader.read()
            print(rfid)
        finally:
            print("cleaned")
            GPIO.cleanup()
        time.sleep(1)
        try:
            if(int(rfid) > 0 and int(rfid) < 25): 
                pot_count = pot_count+1
                GPIOsetup()
                print ("Read pot: " + rfid)
                try:
                    w = int(rfid)
                except ValueError:
                    print("not transformable int")
                print("coneverted")
                water = ((w -2) + 24 ) % 24
                print ( "Water pot number  " + str(water))
                time.sleep(5)
                db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                             user="root",         # your username
                             passwd="iqp2020",  # your password
                             db="mydb")    
                cur = db.cursor(MySQLdb.cursors.DictCursor)
                try:
                    query = "SELECT * from Carousel where barrel_num = %s"
                    cur.execute(query,[str(water)])
                    result = cur.fetchall()
                    for r in result:
                        q = (r['Water_Liters'])
                        ec = (r['Water_ec'])
                        print("The amount is "+ str(q) + " and the ec " + str(ec))
                finally:
                    db.close()
                print("ready to water")
                count = 0
                count2 = 0
                if(ec == 2.3):
                    print(str(water) + " ec 2.3")
                    while(count/(60 *7.5) < q):
                         print(count/(60 *7.5))
                         irrigate_open(ec)
                    print("calling the close function") 
                    irrigate_close(ec)
                elif ( ec == 0.0): 
                    while(count2/(60 *7.5) < q):
                        print(count2/(60*7.5))
                        irrigate_open(ec)
                    print( "calling the close function")
                    irrigate_close(ec)      
        except ValueError:
            print(" Not a number ")
 
                 

def irrigate_open(ec):
    print( "opening the water")
    if(ec == 2.3):
        print("in close for 2.3")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
    elif(ec == 0):
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)


def irrigate_close(ec):
    print( "closing the water")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
   


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
             combo_val = (combo.get_text())
             print(combo_val)
             query = "UPDATE Carousel SET Water_ec = %s , Water_Liters = %s WHERE barrel_num = %s"
             cur.execute(query,(new_water_ec,new_water_q,combo_val))
             db.commit()
             print("Row updates")
        except:
            print("ERROR: **********")
        finally:
            water_ec.set_text("")
            q_water.set_text("")
            combo.set_text("")
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


    def warning(self,widget):
        warning.show_all()
        window.hide()
    def back(self,widget):
        window.show_all()
        warning.hide()
    def continue1(self,widget):
        exWind.show_all()
        warning.hide()

builder = Gtk.Builder()
builder.add_from_file("app.glade")
builder.connect_signals(Handler())

builder.add_from_file("warning.glade")
builder.connect_signals(Handler())
builder.add_from_file("newExperiment.glade")
builder.connect_signals(Handler())
setToolTip()

progress = builder.get_object("progress_bar1")
warning = builder.get_object("window2")
progress.set_pulse_step(0)
comments = builder.get_object("comment_entry")
combo = builder.get_object("update_pot")
b = builder.get_object("b_entry")
water_ec = builder.get_object("water_ec")
q_water = builder.get_object("q_water")
h = builder.get_object("h_entry")
window = builder.get_object("window1")
exWind = builder.get_object("window3")
window.show_all()

irrigation = 0
now = datetime.datetime.now()
seven_am = now.replace(hour=11, minute=52, second=0, microsecond=0)

if datetime.datetime.now == seven_am:
    print("timeeeeee")
count2 = 0

Gtk.main()
GPIO.cleanup() 

