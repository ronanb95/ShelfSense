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
from .models import *
from django.core import serializers
import json
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from django.db.models import F


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

def setUpDevice(request):
	if request.method == "POST":
		pass
	else:
		return render(request, 'mainApp/startMonitor.html')

#Starts monitoring process and passes arguements to the pi
class startMonitoringProcess(generics.RetrieveAPIView):
    def get(self, request):
        barcode1 = request.query_params.get('barcode1')
        barcode2 = request.query_params.get('barcode2')
        barcode3 = request.query_params.get('barcode3')
        barcode4 = request.query_params.get('barcode4')
        barcode5 = request.query_params.get('barcode5')
        print("Barcodes received are: ", barcode1, barcode2, barcode3, barcode4, barcode5)
        success_data = "Great, the unit is up and running..."
        #error_data = "Error, issue with connecting to unit..."
        return Response(success_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)




	# def get(self, request):
 #        barcode2 = request.query_params.get('barcode2')
	# 	barcode1 = request.query_params.get('barcode1')
	# 	print("Barcode1 from form is: ", barcode1, barcode2, barcode3, barcode4, barcode5)
	# 	error_data = "ERROR, problem with Real Time API"
	# 	return Response(error_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)



def displayEntireStore(request):
    """
    :param request:
    :return: the info of all products
    """
    info = Product.objects.all()
    print(info)
    tmpJson = serializers.serialize("json", info)
    tmpObj = json.loads(tmpJson)

    return HttpResponse(json.dumps(tmpObj))
    # return JsonResponse({"models_to_return": list(info)})


def singleProduct(request,barcode):
    """
    :param request:
    :param barcode: primary key //this parameter can be removed when sending a POST request from front end page
    :return: the product info af given barcode
    """
    # if request.method == 'POST':
    #     barcode = request.POST['barcode']
    info = Product.objects.filter(pk=barcode).values('productName','brand','stockcontrol__location','stockcontrol__quantity')
    # tmpJson = serializers.serialize("json", info)
    # tmpObj = json.loads(tmpJson)
    response = json.dumps(list(info))
    return HttpResponse(response)

def selectByBrand(request,brand):
    """
    :param request:
    :param brand:
    :return: the product info af given brand
    """
    # if request.method == 'POST':
    #     barcode = request.POST['barcode']
    info = Product.objects.filter(brand=brand).values('productName','brand','stockcontrol__location','stockcontrol__quantity')
    # tmpJson = serializers.serialize("json", info)
    # tmpObj = json.loads(tmpJson)
    #
    # return HttpResponse(json.dumps(tmpObj))
    response = json.dumps(list(info))
    return HttpResponse(response)


def selectByLocation(request, location):
    """

    :param request:
    :param location:
    :return: Product info of given location
    """

    # info = StockControl.objects.filter(location= location).select_related('barcode')
    # print(info.)
    # info = Product.objects.filter(stockcontrol__location=location)
    # info = StockControl.objects.filter(location=location)
    # for i in info:
    #     print(i)
    # barcode = info.barcode
    # print(barcode)
    # context={}
    # count = 1
    info = Product.objects.filter(stockcontrol__location=location).select_related().values('productName','brand','stockcontrol__location','stockcontrol__quantity')
    # for i in info:
    #     context[count] = [i.barcode, i.productName,i.brand,i.]
    #     print("a")
    #     print(i.barcode,i.brand,i.productName)
    # info = Product._meta.get_fields()
    # links = [rel.get_accessor_name() for rel in a._meta.get_all_related_objects()]
    # for link in links:
    #     objects = getattr(a, link).all()
    #     for object in objects:
    #


# do something with related object instance

    # info = StockControl.objects.all()
    # tmpJson = serializers.serialize("json", info)
    # tmpObj = json.loads(tmpJson)
    #
    # return HttpResponse(json.dumps(tmpObj))
    response = json.dumps(list(info))
    return HttpResponse(response)


def selectByTime(request):
    """

    :param request:
    :return: the last 10 records
    """
    # info = StockControl.objects.all().order_by('timeAdded')
    info = Product.objects.all().select_related('stockcontrol').order_by('-stockcontrol__timeAdded')[:10].values('productName','brand','stockcontrol__location','stockcontrol__quantity')



    # tmpJson = serializers.serialize("json", info)
    # tmpObj = json.loads(tmpJson)
    #
    # return HttpResponse(json.dumps(tmpObj))
    response = json.dumps(list(info))
    return HttpResponse(response)


def selectLocation(request):
    """
    :param request:
    :return: the info of all products
    """
    info = Location.objects.all()
    print(info)
    tmpJson = serializers.serialize("json", info)
    tmpObj = json.loads(tmpJson)

    return HttpResponse(json.dumps(tmpObj))

def lowStockLevel(request):
    """
        :param request:
        :return: low stock level products
        """
    info = Product.objects.filter(lowStockLevel__gte=F('stockcontrol__quantity')).values('productName','brand','stockcontrol__location','lowStockLevel','stockcontrol__quantity')

    response = json.dumps(list(info))
    return HttpResponse(response)



