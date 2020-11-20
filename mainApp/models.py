from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
	barcode = models.CharField(max_length=50, primary_key=True)
	brand = models.CharField(max_length=100)
	productName = models.CharField(max_length=100)
	unitSize = models.CharField(max_length=100)
	weightGrams = models.PositiveIntegerField()
	lowStockLevel = models.PositiveIntegerField(default=3)

	def __str__ (self):
		return (self.brand + " " + self.productName )

# class Products(models.Model):
#     brand = models.TextField(db_column='Brand', blank=True, null=True)  # Field name made lowercase.
#     product = models.TextField(db_column='Product', blank=True, null=True)  # Field name made lowercase.
#     barcode = models.CharField(db_column='Barcode', primary_key=True, max_length=45)  # Field name made lowercase.
#     unit_size = models.TextField(db_column='unit_size', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
#     weight_grams = models.FloatField()
#
#     class Meta:
#         managed = False
#         db_table = 'products'

class StockControl(models.Model):
	stockControlId = models.IntegerField(auto_created=True, primary_key=True)
	#barcode (FK)
	#location (FK)
	#quantity = Need to calculate this?? Do similar thing as the weight thing above
	#DateTime
	pass


class Location(models.Model):
	locationID = models.CharField(max_length=100, primary_key=True)
	#unit (FK)


class Unit(models.Model):
	UnitID = models.PositiveIntegerField(primary_key=True)
	SSH = models.CharField(max_length=1000)