from django.urls import path

from .views import *

urlpatterns = [
    path('', main_view, name='main_view'),
    path('add_jewelerypiece', add_jewelerypiece, name='add_jewelerypiece'),
    path('add_material', add_material, name='add_material'),
    path('add_order', add_order, name='add_order'),
    path('add_orderdetails', add_orderdetails, name='add_orderdetails'),
    path('add_client', add_client, name='add_client'),
    path('add_category', add_category, name='add_category'),
    path('items_list', items_list, name='items_list'),
    path('query/', QueryView.as_view(), name='query'),
    path('fill_db', fill_db, name='fill_db'),
    path('clear_db', DeleteAllObjectsView.as_view(), name='clear_db'),
    path('jewelery_piece/edit/<int:pk>', edit_jewelerypiece, name='edit_jewelerypiece'),
    path('material/edit/<int:pk>', edit_materal, name='edit_material'),
    path('order/edit/<int:pk>', edit_order, name='edit_order'),
    path('orderdetails/edit/<int:pk>', edit_orderdetails, name='edit_orderdetails'),
    path('client/edit/<int:pk>', edit_client, name='edit_client'),
    path('category/edit/<int:pk>', edit_category, name='edit_category'),
    path('jewelery_piece/detele/<int:pk>', delete_jewelerypiece, name='delete_jewelerypiece'),
    path('material/detele/<int:pk>', delete_material, name='delete_material'),
    path('order/detele/<int:pk>', delete_order, name='delete_order'),
    path('orderdetails/detele/<int:pk>', delete_orderdetails, name='delete_orderdetails'),
    path('category/detele/<int:pk>', delete_category, name='delete_category'),
    path('client/detele/<int:pk>', delete_client, name='delete_client'),
]