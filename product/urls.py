from django.urls import path
from . import views

urlpatterns = [
    path('my-products/', views.my_products, name='my_products'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:pid>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pid>/', views.delete_product, name='delete_product'),
    path('cart/', views.show_cart, name='cart'),
    path('add-to-cart/<int:pid>/', views.add_to_cart, name='add_to_cart'),
    path('delete-from-cart/<int:pid>/', views.delete_from_cart, name='delete_from_cart'),
    path('order-history/', views.order_history, name='order_history'),
    path('order-detail/<int:oid>/', views.order_detail, name='order_detail'),
    path('check-out/', views.check_out, name='check_out'),
    path('contact-seller/<int:uid>/', views.contact_seller, name='contact_seller'),
]