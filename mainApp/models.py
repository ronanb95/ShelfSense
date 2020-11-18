from django.contrib.auth.models import User
from django.db import models

class Product(models.Model):
	barcode = models.CharField(max_length=50, primary_key=True)
	brand = models.CharField(max_length=100)
	productName = models.CharField(max_length=100)
	unitSize = models.CharField(max_length=100)
	weightGrams = models.IntegerField()

	def __str__ (self):
		return (self.brand + " " + self.productName )
