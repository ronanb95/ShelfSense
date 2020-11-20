from django.contrib import admin
from .models import Product, StockControl, Location, Unit

admin.site.register(Product)
admin.site.register(StockControl)
admin.site.register(Location)
admin.site.register(Unit)
