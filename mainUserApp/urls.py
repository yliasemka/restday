from django.urls import path
from .views import *

urlpatterns = [
    path('', view_data_from_db, name="view_data_from_db")
]

