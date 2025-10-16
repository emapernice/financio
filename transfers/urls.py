from django.urls import path
from . import views

app_name = 'transfers'

urlpatterns = [
    path('', views.transfer_list, name='transfer_list'),
    path('create/', views.transfer_create, name='transfer_create'),
    path('update/<int:pk>/', views.transfer_update, name='transfer_update'),
    path('delete/<int:pk>/', views.transfer_delete, name='transfer_delete'),

    path('get_account_currency/<int:account_id>/', views.get_account_currency, name='get_account_currency'),
    path('get_accounts_by_currency/<int:from_account_id>/', views.get_accounts_by_currency, name='get_accounts_by_currency'),
]
