from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('product', views.product, name='product'),
    path('logout', views.logout, name='logout'),
    path('temp', views.temp)

]