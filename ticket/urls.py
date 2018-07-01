from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('<int:ticket_id>/', views.ticket_details, name='ticket_details'),
]
