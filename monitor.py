#NOTE: This script is designed to be run once and left running

import sys
import time
import math
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import random

#Read arguements pass from Django's backend, can be many
	#Want to pass barcode 1, weight 1, barcode 2, weight 2 ..... barcode x , weight x & locationCode 
location = (sys.argv[-1])

#Select passed in products and their weights from command line
cmd_line_products = sys.argv[1:-1]
counter = 0

products = []

while counter < len(cmd_line_products):
				#Product key should contain value of the barcode
					#Want to update the products quantity if change of +-5% weight is detected

	#Need to get range of +- 3% to account for potential error in scales, increase too much and could get some overlaps in product weights
	startWeigth = math.floor((int(cmd_line_products[counter+1]) / 100) * 97)
	endWeight =  math.ceil((int(cmd_line_products[counter+1]) / 100) * 103)
	
	product = {"Product":cmd_line_products[counter], "Weight":cmd_line_products[counter+1], "Quantity":0, "Weight_Range":[*range(startWeigth, endWeight+1, 1)]}
	products.append(product)
	counter += 2


#Samples used to test, these are removed when on pi
currentW = 0
samples = [10,20,30,45,22,42,62,94,120,150,180,150,150,150,150,150,180,210,210,210,210,210,210,210]


#Add converted items in here, remove if placed back on shelf	
picked_up = []
placed_back = []
non_conversion = []
#Want to count changes and only send data when chage occurs
changes = 0
readings_until_send = 20
i = 0
while i < len(samples):
	print("Reading number:", i)
	#Value will be read in by scales
	val = samples[i]
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
					#Add item to the conversion list
					picked_up.append(product['Product'])
					break
	#Set the current weight to be the value currently detected
	currentW = val
	readings_until_send -= 1

	#Only sending new information to database every 10 readings and if change detected
	if (readings_until_send == 0 and changes > 0):
		try:
																											##### From last slide of presentation #########
			connection = mysql.connector.connect(host="34.105.243.211", database="shelfSense", user="root", password="")
			cursor = connection.cursor()
			#for product in products:
				#Need to create a random stock_control id here myself
			execution = """INSERT INTO mainApp_stockcontrol (quantity, timeAdded, barcode_id, location_id, stockControl_id) values (%s, %s, %s, %s, %s)"""
			#Creating the randomID here purely because we are having issue with DB and this offers a brute force solution
			for product in products:
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

			connection.commit()
			cursor.close()
		except mysql.connector.Error as error:
			print(error)
		finally:
			if connection.is_connected():
				connection.close()


		#Increase this for less frequent database sends, decrease to increase sends
		readings_until_send = 10
		changes = 0


	i+=1
	time.sleep(.5)







