from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('home/', views.home, name="home"),
    path('register_product/', views.registerProduct, name='register_product'),
    path('setupdevice/', views.setUpDevice, name='setupdevice'),

    path('all', views.displayEntireStore, name='all'),
    path('barcode/<slug:barcode>/', views.singleProduct, name='singleProduct'),
    path('brand/<slug:brand>/', views.selectByBrand, name='selectByBrand'),
    path('location/<slug:location>/', views.selectByLocation, name='selectByLocation'),
    path('default/', views.selectByTime, name='selectByTime'),
    path('selectLocation/', views.selectLocation, name='selectLocation'),
    path('lowLevelStock/', views.lowStockLevel, name='lowLevelStock'),
    path('login/', views.login_view, name="login"),
    path('register/', views.register_user, name="register"),
    path('user/', views.user_page, name="user"),
    path('logout/', views.logout_user, name="logout"),
    path('maintenance/', views.maintenance, name="maintenance"),

    # Start monitor form
    path('startMonitoringProcess/', views.startMonitoringProcess.as_view(), name="startMonitoringProcess"),
    # Check pi is online
    path('checkMaintenance/', views.startMaintenanceCheck.as_view(), name="startMaintenance"),
    path('getrates/', views.getRates, name='getrates'),
]
