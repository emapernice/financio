from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('curency/', views.currency_list, name='currency_list'),
    path('curency/create/', views.currency_create, name='currency_create'),
    path('curency/update/<int:pk>/', views.currency_update, name='currency_update'),
    path('curency/delete/<int:pk>/', views.currency_delete, name='currency_delete'),

    path('entity/', views.entity_list, name='entity_list'),
    path('entity/create/', views.entity_create, name='entity_create'),
    path('entity/update/<int:pk>/', views.entity_update, name='entity_update'),
    path('entity/delete/<int:pk>/', views.entity_delete, name='entity_delete'),
]
