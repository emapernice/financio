from django.urls import path
from . import views

app_name = 'fixed'

urlpatterns = [
    path('', views.fixedrecord_list, name='fixedrecord_list'),
    path('create/', views.fixedrecord_create, name='fixedrecord_create'),
    path('update/<int:pk>/', views.fixedrecord_update, name='fixedrecord_update'),
    path('delete/<int:pk>/', views.fixedrecord_delete, name='fixedrecord_delete'),

]
