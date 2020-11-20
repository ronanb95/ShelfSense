from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product
#from django.contrib.auth.forms import UserCreationForm
from .forms import ProductBarcodeForm, RegisterProductForm
from django.contrib import messages
#Related to using APIs and serializers
from rest_framework import generics
from rest_framework.views import APIView
#Related to ssh to pi
import paramiko
import sys
import time


def home(request):
	return render(request, "mainApp/home.html")

def about(request):
	return render(request, "mainApp/about.html")


def getWeight():

	try:
		client = paramiko.SSHClient()
		print("Connected")
		#Needs to have logged into the pi once from host before
				#Will need to ssh into pi from server when deploying
		client.load_system_host_keys()
		client.connect('192.168.0.45', username='pi', password='raspberry')

		stdin, stdout, stderr = client.exec_command('python	example2.py')
		print("Running script")
		while not stdout.channel.exit_status_ready():
			if stdout.channel.recv_ready():
				stdoutLines = stdout.readlines()
				weight = stdoutLines[1].strip('\n')
				print(stdoutLines)
		#Once the loop finishes it prints the results
	except:
		print("Error in connection")
		weight = "No connection"
		# If weight is -5000 know that could not commuincate with pi

	
	return weight
	#return  render(request, 'mainApp/test.html', context)


#In current form can be used to add products
def test(request):

	barcode_form = ProductBarcodeForm()
	#Example Query of database
	context = {
		'weight':Product.objects.last().weightGrams,
		'form':barcode_form
	}

	if request.method == 'POST':
		form = ProductBarcodeForm(request.POST)
		#Form will be valid if the product is found in the data
		if form.is_valid():
			print("Valid form")
			messages.warning(request, 'Product was not found, please add now')
			return redirect('register_product')
			#Create a redirect here to a page that registers the products
		else:
			#Form will not be valid if the product barcode is in the database
			print("Not valid form")
			scannedBarcode = form.data['barcode']
			product = Product.objects.get(barcode=scannedBarcode)
			messages.success(request, f'Great, {product} was found in database')
			return redirect('testPage')
	

	return  render(request, 'mainApp/test.html', context)


def registerProduct(request):

	if request.method == 'POST' and 'run_script' in request.POST:
		form = RegisterProductForm(request.POST)
		#Form will be valid if the product is found in the data
		if form.is_valid():
			weight = getWeight()
			print(weight)
			#No weigth has been detected
			if weight == "None":
				messages.warning(request, 'Error, no weight detected')
				return redirect(reverse('register_product'))
			elif weight == "No connection":
				messages.warning(request, 'Error, could not connect to weight sensing unit, please try again')
				return redirect(reverse('register_product'))
			#Create and save new Product
			else:
				#Get data from form
				barcode = form.cleaned_data.get('barcode')
				brand = form.cleaned_data.get('brand')
				productName = form.cleaned_data.get('productName')
				unitSize = form.cleaned_data.get('unitSize')
				#Create and save new entry
				newProduct = Product(barcode=barcode, brand=brand, productName=productName, unitSize=unitSize, weightGrams=weight)
				newProduct.save()
				messages.success(request, f'Successfully created product {brand} {productName}')
				return redirect('testPage')

		else:
			print("invalid form")
			scannedBarcode = form.data['barcode']
			product = Product.objects.get(barcode=scannedBarcode)
			messages.warning(request, f'Barcode {scannedBarcode} already attached to {product}')
			return redirect('register_product')

	#A GET request
	else:
		register_form = RegisterProductForm()
		context = {'form':register_form}
		return render(request, 'mainApp/register_product.html', context)