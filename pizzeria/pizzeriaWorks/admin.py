from django.contrib import admin
from .models import Pizza, PizzaType, PizzaRating, Profile, Basket

# Register your models here.

admin.site.register(Pizza)
admin.site.register(PizzaType)
admin.site.register(PizzaRating)
admin.site.register(Profile)
admin.site.register(Basket)