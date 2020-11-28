from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')