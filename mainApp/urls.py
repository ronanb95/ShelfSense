from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name='mainAbout'),
    path('test/', views.test, name='testPage'),
    path('register_product/', views.registerProduct, name='register_product')
]
