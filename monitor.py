#Should make the last arguement the locationID(???)
import sys
import time
import math
import mysql.connector
from mysql.connector import Error

#Read arguements pass from Django's backend, can be many
cmd_line_products = sys.argv[1:]
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



currentW = 0
samples = [20, 40, 60, 40, 20, 20, 20,20,50, 40, 60, 40, 20, 20, 20,20, 40, 60, 40, 20, 20, 20, 0, 0, -20]

	

changes = 0
readings_until_send = 10
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
					#Don't want to update more than one product
					break
		#Stock removed
		elif diff < 0:
			for product in products:
				if (diff * -1) in product['Weight_Range'] and product['Quantity'] > 0:
					product["Quantity"] -= 1
					print(product["Product"] + " : " + str(product["Quantity"]))
					changes += 1
					break
	#Set the current weight to be the value currently detected
	currentW = val
	readings_until_send -= 1

	#Only sending new information to database every 10 readings and if change detected
	if (readings_until_send == 0 and changes > 0):
		try:
			connection = mysql.connector.connect(host=" ", database="shelfSense", user="root", password=" ")
			cursor = connection.cursor()
			time.sleep(5)
			#Want to then create a loop over products and enter the information into the database
			cursor.close()
		except mysql.connector.Error as error:
			print(error)
		finally:
			if connection.is_connected():
				connection.close()


		# print("Sending data to database")
		# time.sleep(10)
		# print("Sending successful")
		readings_until_send = 10
		changes = 0


	i+=1
	time.sleep(.5)








 