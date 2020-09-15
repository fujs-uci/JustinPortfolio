from django.urls import path
from .views import *

app_name = 'portfolio'
urlpatterns = [
    path('', home_page, name='home_page'),
    path('<str:link_name>/', link_view, name='link_view'),
]
