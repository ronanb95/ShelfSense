from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product
# from django.contrib.auth.forms import UserCreationForm
from .forms import ProductBarcodeForm, RegisterProductForm
from django.contrib import messages
# Related to using APIs and serializers
from rest_framework import generics
from rest_framework.views import APIView
# Related to ssh to pi
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
from django.db.models import F, Count, Max
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
from django.contrib.auth.decorators import login_required


# Basic homepage render
@login_required(login_url='landing')
def home(request):
    # if user not logged in:
    # return render(request, "mainApp/index.html")

    # else:
    heading = "Dashboard"
    context = {"heading": heading}
    return render(request, "mainApp/datatable.html", context)


def landing(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, "mainApp/index.html")


# Function connects to PI and gets Weigth reading to register product
def getWeight():
    try:
        client = paramiko.SSHClient()
        print("Connected")
        # Needs to have logged into the pi once from host before
        # Will need to ssh into pi from server when deploying
        client.load_system_host_keys()
        client.connect('192.168.0.45', username='pi', password='raspberry')

        stdin, stdout, stderr = client.exec_command('python    getWeight.py')
        print("Running script")
        while not stdout.channel.exit_status_ready():
            if stdout.channel.recv_ready():
                stdoutLines = stdout.readlines()
                weight = stdoutLines[1].strip('\n')
                print(stdoutLines)
        # Once the loop finishes it prints the results
    except:
        print("Error in connection")
        weight = "No connection"
        # If weight is -5000 know that could not commuincate with pi
    return weight


# Actually start the monitoring process
def startUnit(barcodes, weights, location):
    print(barcodes)
    print(weights)
    commandString = "python3 completeMonitor.py "

    for i in range(0, len(barcodes)):
        print("i is: ", i)
        commandString = commandString + barcodes[i] + " "
        commandString = commandString + str(weights[i]) + " "

    commandString = commandString + str(location)

    print(commandString)

    try:
        client = paramiko.SSHClient()
        print("Connected to unit for monitoring")
        client.load_system_host_keys()
        client.connect('192.168.0.45', username='pi', password='raspberry')

        # stdin, stdout, stderr = client.exec_command('python getWeight.py')
        client.exec_command(commandString)

        return ("Great, the unit has been set up successfully")

    except:
        return ("Error connecting to the unit for monitoring")


# Check and Register Product Page
@login_required(login_url='landing')
def registerProduct(request):
    # Heading used for nav bar
    heading = 'Register Product'

    #### Barcoode checking form
    if request.method == 'POST' and 'barcode_check' in request.POST:
        form = ProductBarcodeForm(request.POST)
        if form.is_valid():
            messages.warning(request, 'Product was not found, please add now')
            register_form = RegisterProductForm()
            context = {'form': register_form, 'heading': heading}
            return render(request, 'mainApp/register_product.html', context)
        else:
            scannedBarcode = form.data['barcode']
            product = Product.objects.get(barcode=scannedBarcode)
            messages.success(request, f'Great, {product} was found in database. Please check the next product now')
            return redirect('register_product')

    #### Product Registration form
    elif request.method == 'POST' and 'run_script' in request.POST:
        form = RegisterProductForm(request.POST)
        # Form will be valid if the product is found in the data
        if form.is_valid():
            weight = getWeight()
            # No weigth has been detected
            if weight == "None":
                messages.warning(request, 'Error, no weight detected')
                return redirect(reverse('register_product'))
            elif weight == "No connection":
                messages.warning(request, 'Error, could not connect to weight sensing unit, please try again')
                return redirect(reverse('register_product'))
            # Create and save new Product
            else:
                # Get data from form
                barcode = form.cleaned_data.get('barcode')
                brand = form.cleaned_data.get('brand')
                productName = form.cleaned_data.get('productName')
                unitSize = form.cleaned_data.get('unitSize')
                # Create and save new entry
                newProduct = Product(barcode=barcode, brand=brand, productName=productName, unitSize=unitSize,
                                     weightGrams=weight)
                newProduct.save()
                messages.success(request, f'Successfully created product {brand} {productName}')
                barcode_form = ProductBarcodeForm()
                heading = 'Register Product'
                context = {
                    'check_form': barcode_form,
                    'heading': heading
                    # 'form':register_form
                }
                return render(request, 'mainApp/register_product.html', context)

        # Barcode provided for registration form already exists
        else:
            print("invalid form")
            scannedBarcode = form.data['barcode']
            product = Product.objects.get(barcode=scannedBarcode)
            messages.warning(request, f'Barcode {scannedBarcode} already attached to {product}')
            return redirect('register_product')

    # A standard GET request
    else:
        barcode_form = ProductBarcodeForm()
        context = {
            'check_form': barcode_form,
            'heading': heading
        }
        return render(request, 'mainApp/register_product.html', context)


@login_required(login_url='landing')
def setUpDevice(request):
    if request.method == "POST":
        pass
    else:
        return render(request, 'mainApp/startMonitor.html', context={'heading': "Set Up Unit"})


# Starts monitoring process and passes arguements to the pi
class startMonitoringProcess(generics.RetrieveAPIView):
    def get(self, request):

        print("Received request")

        barcode1 = request.query_params.get('barcode1')
        barcode2 = request.query_params.get('barcode2')
        barcode3 = request.query_params.get('barcode3')
        barcode4 = request.query_params.get('barcode4')
        barcode5 = request.query_params.get('barcode5')
        location = request.query_params.get('location')
        barcodes = []
        weights = []
        barcodesToSend = []
        barcodes.extend([barcode1, barcode2, barcode3, barcode4, barcode5])

        for barcode in barcodes:
            if len(barcode) > 1:
                barcodesToSend.append(barcode)
                print("Checking for :", barcode)
                weight = Product.objects.get(barcode=barcode)
                weights.append(weight.weightGrams)

        responseFromPi = startUnit(barcodesToSend, weights, location)

        # error_data = "Error, issue with connecting to unit..."
        return Response(responseFromPi)


# def get(self, request):
#        barcode2 = request.query_params.get('barcode2')
#  barcode1 = request.query_params.get('barcode1')
#  print("Barcode1 from form is: ", barcode1, barcode2, barcode3, barcode4, barcode5)
#  error_data = "ERROR, problem with Real Time API"
#  return Response(error_data, status=status.HTTP_503_SERVICE_UNAVAILABLE)


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


def singleProduct(request, barcode):
    """
    :param request:
    :param barcode: primary key //this parameter can be removed when sending a POST request from front end page
    :return: the product info af given barcode
    """
    # if request.method == 'POST':
    #     barcode = request.POST['barcode']
    info = Product.objects.filter(pk=barcode).values('barcode', 'productName', 'brand', 'stockcontrol__location',
                                                     'stockcontrol__quantity')
    # tmpJson = serializers.serialize("json", info)
    # tmpObj = json.loads(tmpJson)
    response = json.dumps(list(info))
    return HttpResponse(response)


def selectByBrand(request, brand):
    """
    :param request:
    :param brand:
    :return: the product info af given brand
    """
    # if request.method == 'POST':
    #     barcode = request.POST['barcode']
    info = Product.objects.filter(brand=brand).values('barcode', 'productName', 'brand', 'stockcontrol__location',
                                                      'stockcontrol__quantity')
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
    info = Product.objects.filter(stockcontrol__location=location).select_related().values('barcode', 'productName',
                                                                                           'brand',
                                                                                           'stockcontrol__location',
                                                                                           'stockcontrol__quantity')
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
    info = Product.objects.all().select_related('stockcontrol').order_by('-stockcontrol__timeAdded')[:10].values(
        'barcode', 'productName', 'brand', 'stockcontrol__location', 'stockcontrol__quantity')

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

    # distinct = Product.objects.order_by('-stockcontrol__timeAdded').filter(lowStockLevel__gte=F('stockcontrol__quantity')).values(
    #     'barcode'
    # ).annotate(
    #     barcode_count=Count('barcode')
    # ).filter(barcode_count=1)
    # info = Product.objects.filter(lowStockLevel__gte=F('stockcontrol__quantity')).order_by('barcode').values('barcode').distinct().values('barcode','productName','brand','stockcontrol__location','lowStockLevel','stockcontrol__quantity')
    # info = Product.objects.filter(lowStockLevel__gte=F('stockcontrol__quantity')).values('barcode','productName','brand','stockcontrol__location','lowStockLevel','stockcontrol__quantity').order_by('barcode','-stockcontrol__timeAdded')

    info = Product.objects.annotate(most_recent=Max('stockcontrol__timeAdded'))
    info1 = StockControl.objects.filter(timeAdded__in=[s.most_recent for s in info]).filter(
        barcode__lowStockLevel__gte=F('quantity')).values('barcode', 'location', 'barcode__productName',
                                                          'barcode__brand', 'barcode__lowStockLevel', 'quantity',
                                                          'location__store')
    # print(info)
    print(info1)
    response = json.dumps(list(info1))
    return HttpResponse(response)


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":

            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/home")
                else:
                    msg = 'Invalid credentials'
            else:
                msg = 'Error validating the form'

        return render(request, "mainApp/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                user = authenticate(username=username, password=raw_password)
                success = True

                return redirect("/login")

            else:
                msg = 'Form is not valid'
        else:
            form = SignUpForm()

        return render(request, "mainApp/register.html", {"form": form, "msg": msg, "success": success})


def user_page(request):
    return render(request, "mainApp/page_user.html")


def logout_user(request):
    logout(request)
    return redirect('landing')



