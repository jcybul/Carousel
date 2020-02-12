# Carousel

The Carousel irrigation system is an agricultural research system used to measure the effects of different water salinities on plants.

![Flow chart](/Images/Flow_Chart.png)


The system divides in three main components:
   1. Hardware 
   2. Database 
   3. User-interface 
   
# HARDWARE

This project is meant to create a supplementary automatic irrigation system to the existing carousel, using the spinning capabilities it already has. For this project we will be using a raspberry pi 4 with Raspbian as the operating system. The hardware components required are the following. 

   1 Raspberry pi 4 (https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
   2  Electronic ball valves (https://www.amazon.com/gp/product/B06XRJF4JG/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
   2 Flow rate sensors (https://www.amazon.com/gp/product/B00VKAT9VA/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
   1 L298N motor driver (https://cdn.instructables.com/ORIG/FCN/YABW/IHNTEND4/FCNYABWIHNTEND4.pdf)
   1 RFID scanner (https://www.amazon.com/gp/product/B076HSDF2Y/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
   24 RFID tags (https://www.amazon.com/gp/product/B076HSDF2Y/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)

A side from that a soldering board extension and a soldering iron is recommended for organization

The wiring of the system can be seen in the picture below:

![Wiring Diagram](/Images/Carousel_Wiring_diagram_bb.png) 

[Refer to the fritzing file for more detailed information]( /Carousel_Wiring_diagram.fzz)


# DATABASE

The database used for this proyect is a MySql database running locally on the Raspberry Pi, which makes acces to it very simple, this database is only running when the Raspberry Pi is tunrned on.

# USER-INTERFACE


![UI](/Images/UI_ITERATION.png) 

The user-interface was created using python, GTK, which is a free and open-source cross-platform widget toolkit for creating graphical user interfaces ,and glade for the design.
