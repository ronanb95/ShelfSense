#! /usr/bin/python3
import sys
import time
import math
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import random

EMULATE_HX711=False

referenceUnit = 852937 / 2000

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")
    if not EMULATE_HX711:
        GPIO.cleanup()  
    print("Bye!")
    sys.exit()


## 19 and 26 are the GPIO pins on PI
hx = HX711(19, 26)
#hx = HX711(17, 27) #If have multiple sensors just add like so
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()


#Read arguements pass from Django's backend, can be many
location = (sys.argv[-1])

#Select passed in products and their weights from command line
cmd_line_products = sys.argv[1:-1]
counter = 0

products = []

while counter < len(cmd_line_products):
    #Want to update the products quantity if change of +-5% weight is detected
    #Need to get range of +- 3% to account for potential error in scales, increase too much and could get some overlaps in product weights
    startWeigth = math.floor((int(cmd_line_products[counter+1]) / 100) * 97)
    endWeight =  math.ceil((int(cmd_line_products[counter+1]) / 100) * 103)
    #Product key should contain value of the barcode
    product = {"Product":cmd_line_products[counter], "Weight":cmd_line_products[counter+1], "Quantity":0, "Weight_Range":[*range(startWeigth, endWeight+1, 1)]}
    products.append(product)
    counter += 2




#Add converted items in here, remove if placed back on shelf    
picked_up = []
placed_back = []
non_conversion = []
currentW = 0
changes = 0
#Will send data after 20 readings
readings_until_send = 20

print("Tare done! Add weight now...")
while True:
    try:
        val = hx.get_weight(5)
        print(val)
        diff = val - currentW
        if diff != 0:
            #New stock added
            if diff > 1:
                for product in products:
                    if diff in product['Weight_Range']:
                        product["Quantity"] += 1
                        print(product["Product"] + " : " + str(product["Quantity"]))
                        changes += 1
                        #Check if item is in picked_up list, if is then remove and mark as non conversion
                        if product["Product"] in picked_up:
                            picked_up.remove(product["Product"])
                            non_conversion.append(product["Product"])
                        #Don't want to update more than one product
                        break
            #Stock removed
            elif diff < 0:
                for product in products:
                    if (diff * -1) in product['Weight_Range'] and product['Quantity'] > 0:
                        product["Quantity"] -= 1
                        print(product["Product"] + " : " + str(product["Quantity"]))
                        changes += 1
                        picked_up.append(product['Product'])
                        break
        #Set the current weight to be the value currently detected
        currentW = val
        readings_until_send -= 1

        #Only sending new information to database every 10 readings and if change detected
        if (readings_until_send == 0 and changes > 0):
            try:                                                                                                ###### Use password from presentation #######
                connection = mysql.connector.connect(host="34.105.243.211", database="shelfSense", user="root", password="")
                cursor = connection.cursor()
                #for product in products:
                    #Need to create a random stock_control id here myself
                execution = """INSERT INTO mainApp_stockcontrol (quantity, timeAdded, barcode_id, location_id, stockControl_id) values (%s, %s, %s, %s, %s)"""
                for product in products:
                #Creating the randomID here purely because we are having issue with DB and this offers a brute force solution
                    randomID = random.randint(1,100000000000)
                    #Want to set the current time for timestamp
                    dateTimeObj = datetime.now()
                    recordTuple = (product["Quantity"], dateTimeObj, product['Product'], location, randomID)
                    cursor.execute(execution, recordTuple)

                #Then insert the conversion rates
                executionConv = """INSERT INTO mainApp_cr (crID, barcode, conversion) values (%s, %s, %s)"""
                for convert in picked_up:
                    #Quick fix for id issues
                    randomID = random.randint(1,100000000000)
                    recordTuple = (randomID, convert, 1)
                    cursor.execute(executionConv, recordTuple)

                #Then add in the non conversions
                for non in non_conversion:
                    #Quick fix for id issues
                    randomID = random.randint(1,100000000000)
                    recordTuple = (randomID, non, 0)
                    cursor.execute(executionConv, recordTuple)

                #Want to then create a loop over products and enter the information into the database
                connection.commit()
                cursor.close()
            except mysql.connector.Error as error:
                print(error)
            finally:
                if connection.is_connected():
                    connection.close()
        #Increase this for less frequent database sends, decrease to increase sends
        readings_until_send = 20
        changes = 0
        

        hx.power_down()
        hx.power_up()
        time.sleep(2.5)

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

time.sleep(5)
cleanAndExit()