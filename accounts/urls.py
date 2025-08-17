from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.account_list, name='account_list'),
    path('create/', views.account_create, name='account_create'),
    path('update/<int:pk>/', views.account_update, name='account_update'),
    path('delete/<int:pk>/', views.account_delete, name='account_delete'),
    path('<int:pk>/', views.account_detail, name='account_detail'),

    path('transfers/', views.transfer_list, name='transfer_list'),
    path('transfers/create/', views.transfer_create, name='transfer_create'),
    path('transfers/update/<int:pk>/', views.transfer_update, name='transfer_update'),
    path('transfers/delete/<int:pk>/', views.transfer_delete, name='transfer_delete'),
    path('transfers/<int:pk>/', views.transfer_detail, name='transfer_detail'),
]
