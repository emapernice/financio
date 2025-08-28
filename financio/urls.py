"""
URL configuration for financio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('records/', include('records.urls', namespace='records')),
    path('core/', include('core.urls', namespace='core')),
    path('fixed/', include('fixed.urls', namespace='fixed')),
    path('budgets/', include('budgets.urls', namespace='budgets')),
    path('investments/', include('investments.urls', namespace='investments')),
    path('transfers/', include('transfers.urls', namespace='transfers')),
    path("dashboard/", include("dashboard.urls", namespace="dashboard")),
]
