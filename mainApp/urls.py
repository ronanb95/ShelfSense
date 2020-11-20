from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name='mainAbout'),
    path('test/', views.test, name='testPage'),
    path('register_product/', views.registerProduct, name='register_product'),

    path('all', views.displayEntireStore, name='all'),
    path('barcode/<slug:barcode>/', views.singleProduct, name='singleProduct'),
    path('brand/<slug:brand>/', views.selectByBrand, name='selectByBrand')
]
