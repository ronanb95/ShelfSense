from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

#The actual weigth sensing unit and ssh details
class Unit(models.Model):
	unitID = models.PositiveIntegerField(auto_created=True, primary_key=True)
	ssh = models.CharField(max_length=1000)

	def __str__ (self):
		return("Unit " + str(self.unitID))

#The location within the store eg(1A is the first shelf on the first shelving unit, 1B is second shelf on first shelving unit etc..)
class Location(models.Model):
	locationID = models.CharField(max_length=100, primary_key=True)
	unit = models.OneToOneField(Unit, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return("Location " + self.locationID)

#The product details
class Product(models.Model):
	barcode = models.CharField(max_length=50, primary_key=True)
	brand = models.CharField(max_length=100)
	productName = models.CharField(max_length=100)
	unitSize = models.CharField(max_length=100)
	weightGrams = models.PositiveIntegerField()
	lowStockLevel = models.PositiveIntegerField(default=3)

	def __str__ (self):
		return (self.brand + " " + self.productName )

class StockControl(models.Model):
	stockControlId = models.IntegerField(auto_created=True, primary_key=True)
	#If product is deleted want to stop monitoring
	barcode = models.OneToOneField(Product, on_delete=models.CASCADE)
	#Want to stop monitoring if location is deleted
	location = models.ForeignKey(Location, on_delete=models.CASCADE)
	#PositiveIntegerField allows for 0 aswell 
	quantity = models.PositiveIntegerField(default=0)
	timeAdded = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return (self.barcode.brand + " " + self.barcode.productName + " at location " + str(self.location.locationID))

	
