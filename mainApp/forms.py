from django import forms
from .models import Product

class ProductBarcodeForm(forms.ModelForm):
    barcode = forms.CharField()

    class Meta:
        model = Product
        fields = ['barcode']


class RegisterProductForm(forms.ModelForm):
	#Used to retrieve SSH information to activate weight sensor
		#Change to required in production
	Unit_barcode = forms.CharField(label="Scan barcode of unit")

	barcode = forms.CharField(label="Product barcode")
	brand = forms.CharField(label="Barnd")
	productName = forms.CharField(max_length=100, label="Full product type")
	unitSize = forms.CharField(max_length=100, label="Unit Size")
	lowStockLevel = forms.IntegerField(required=False, label="Low Stock Level (Only enter if known)")
	#weightGrams = models.IntegerField()

	class Meta:
		model = Product
		fields = ['barcode', 'brand', 'productName', 'unitSize']