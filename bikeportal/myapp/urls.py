from django.contrib import admin
from django.urls import path, include
from .import views
urlpatterns = [
    path('',views.home, name = 'home'),
    path('about/',views.about, name = 'about'),
    path('services/',views.services, name = 'services'),
    path('product/',views.product, name = 'product'),
    path('cart/',views.cart, name = 'cart'),
    path('checkout/',views.checkout, name = 'checkout'),
    path('contact/',views.contact, name = 'contact'),
    path('detail/',views.detail, name = 'detail'),
    path('detail/<int:id>/',views.detail, name = 'detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('mechanic/',views.Mechanic,name ='mechanic'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),


]