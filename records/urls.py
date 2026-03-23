from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('', views.record_list, name='record_list'),
    path('create/', views.record_create, name='record_create'),
    path('update/<int:pk>/', views.record_update, name='record_update'),
    path('delete/<int:pk>/', views.record_delete, name='record_delete'),

    path('category/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/update/<int:pk>/', views.category_update, name='category_update'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),

    path('subcategory/', views.subcategory_list, name='subcategory_list'),
    path('subcategory/create/', views.subcategory_create, name='subcategory_create'),
    path('subcategory/update/<int:pk>/', views.subcategory_update, name='subcategory_update'),
    path('subcategory/delete/<int:pk>/', views.subcategory_delete, name='subcategory_delete'),

    path('financial-type/', views.financial_type_list, name='financial_type_list'),
    path('financial-type/create/', views.financial_type_create, name='financial_type_create'),
    path('financial-type/update/<int:pk>/', views.financial_type_update, name='financial_type_update'),
    path('financial-type/delete/<int:pk>/', views.financial_type_delete, name='financial_type_delete'),

    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('get_entities/', views.get_entities, name='get_entities'),
    path('get_account_currency/<int:account_id>/', views.get_account_currency, name='get_account_currency'),
]
