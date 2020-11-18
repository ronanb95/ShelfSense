from django.shortcuts import render, redirect
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


def getWeight(request):

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
			product = Product.objects.all().filter(barcode=scannedBarcode)
			print(product)
			messages.success(request, 'Great, product was found in database')
			return redirect('testPage')
	

	return  render(request, 'mainApp/test.html', context)


def registerProduct(request):
	register_form = RegisterProductForm()
	context = {'form':register_form}

	return render(request, 'mainApp/register_product.html', context)