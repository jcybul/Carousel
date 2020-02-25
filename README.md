# Carousel

The Carousel Irrigation System at the Southern Arava R&D is an agricultural research system used to measure the effects of different water salinities on plants.

![Flow chart](/Images/Flow_Chart.png)


The system is divided into three main components:
   1. Hardware 
   2. Database 
   3. User-interface 
   
# HARDWARE

This project is meant to create a supplementary automatic irrigation system to the existing carousel, using the spinning capabilities it already has. For this project we will be using a Raspberry Pi 4 with Raspbian as the operating system. The hardware components required are the following: 

   1 Raspberry pi 4 (https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
   2  Electronic ball valves (https://www.amazon.com/gp/product/B06XRJF4JG/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
   2 Flow rate sensors (https://www.amazon.com/gp/product/B00VKAT9VA/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
   1 L298N motor driver (https://cdn.instructables.com/ORIG/FCN/YABW/IHNTEND4/FCNYABWIHNTEND4.pdf)
   1 RFID scanner (https://www.amazon.com/gp/product/B076HSDF2Y/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
   24 RFID tags (https://www.amazon.com/gp/product/B076HSDF2Y/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)

Aside from that, a soldering board extension and a soldering iron is recommended for organization

The wiring of the system can be seen in the pictures below:

![Wiring Diagram of the RFID scanner](/Images/Carousel_Wiring_diagram_RFID.png)
![Wiring Diagram of the Flowrate sensors and ball valves](/Images/diagram.png) 


[Refer to the fritzing files for more detailed information]( /Fritzing_Files)


# DATABASE

The database used for this project is a MySql database running locally on the Raspberry Pi, which makes access to it very simple, this database is only running when the Raspberry Pi is turned on.

# USER-INTERFACE


![UI](/Images/UI.png) 

The user-interface was created using python, the GTK library, which is a free and open-source cross-platform widget toolkit for creating graphical user interfaces, and Glade for the design.

# USER-MANUAL

A user manual was created for operating the system
![UI](/Images/1.png) 
![UI](/Images/2.png) 
![UI](/Images/3.png) 
![UI](/Images/4.png) 
![UI](/Images/5.png) 
![UI](/Images/6.png) 
![UI](/Images/7.png) 
![UI](/Images/8.png) 
![UI](/Images/9.png) 
![UI](/Images/10.png) 
![UI](/Images/11.png) 
![UI](/Images/12.png) 
![UI](/Images/13.png) 
![UI](/Images/14.png) 
![UI](/Images/15.png) 
![UI](/Images/16.png) 

