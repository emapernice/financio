from django.urls import path
from . import views

app_name = 'transfers'

urlpatterns = [
    path('', views.transfer_list, name='transfer_list'),
    path('create/', views.transfer_create, name='transfer_create'),
    path('update/<int:pk>/', views.transfer_update, name='transfer_update'),
    path('delete/<int:pk>/', views.transfer_delete, name='transfer_delete'),
]