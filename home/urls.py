from django.urls import path
from .views import *

urlpatterns = [
    path('nearby_food_trucks', nearby_food_trucks, name = "nearby_food_trucks")
]