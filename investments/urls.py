from django.urls import path
from . import views

app_name = 'investments'

urlpatterns = [
    path('', views.investment_list, name='investment_list'),
    path('create/', views.investment_create, name='investment_create'),
    path('update/<int:pk>/', views.investment_update, name='investment_update'),
    path('delete/<int:pk>/', views.investment_delete, name='investment_delete'),

]
