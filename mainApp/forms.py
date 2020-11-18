from django import forms
from .models import Product

class ProductBarcodeForm(forms.ModelForm):
    barcode = forms.CharField()

    class Meta:
        model = Product
        fields = ['barcode']


class RegisterProductForm(forms.ModelForm):
	barcode = forms.CharField()
	brand = forms.CharField()
	productName = forms.CharField(max_length=100)
	unitSize = forms.CharField(max_length=100)
#weightGrams = models.IntegerField()

	class Meta:
		model = Product
		fields = ['barcode']