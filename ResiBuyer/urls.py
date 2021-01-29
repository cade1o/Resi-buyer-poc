"""ResiBuyer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views
from django.contrib.auth import views as auth_views
from . import views as user_views

urlpatterns = [
    path('', views.index,name='home'),
    path('admin/',admin.site.urls, name='admin'),
    path('order/place/',views.order_place, name='order_place'),
    path('order/view/', views.order_view, name='order_view'),
    path('place_order/', views.place_order, name='place_order'),
    path('checkout/',views.checkout, name='checkout'),
    path('register/', user_views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name = 'UI/authentication_page/login.html'), name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'UI/authentication_page/logout.html'), name = 'logout'),
    path('invoice/<int:order_id>/', views.make_invoice, name='invoice'),
    path('add_tracking_info/<int:order_id>/', views.add_tracking_info, name='add_tracking_info'),
    path('generate_full_tracking_info/<int:order_id>/', views.generate_full_tracking_info, name='generate_full_tracking_info'),
    path('blockchain/', views.view_blockchain, name='view_blockchain'),
    path('mine/', views.mine_unconfirmed_data, name='mine_unconfirmed_data'),
    path('register_node/', views.register_node, name='register_node'),
    path('get_chain/', views.get_blockchain, name='get_blockchain'),
    path('add_block/', views.verify_and_add_block, name='add_block'),
    path('add_tx/', views.receive_unconfirmed_tx, name='add_tx'),
]
