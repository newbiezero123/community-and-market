# shop/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),  # หน้าแสดงสินค้า 
    path('add_product/', views.add_product, name='add_product'), 
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('purchase_item/', views.purchase_item, name='purchase_item'),
    path('order/success/', views.order_success, name='order_success'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('purchase_cart_items/', views.purchase_cart_items, name='purchase_cart_items'),  # หน้าแสดงการสั่งซื้อจากตะกร้า
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order_history/', views.order_history, name='order_history'),
    path('order_history_detail/<int:order_id>/', views.order_history_detail, name='order_history_detail'),
    path('manage-products/', views.manage_products, name='manage_products'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('sales_report/', views.sales_report, name='sales_report'),

]
