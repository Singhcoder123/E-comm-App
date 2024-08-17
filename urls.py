from django.urls import path
from Ecommapp import views
from Ecommapp.views import SimpleView
urlpatterns = [
    path('',views.home),
    path('about',views.about),
    path('contact',views.contact),
    path('ad/<a>/<b>',views.addition),
    path('myview',SimpleView.as_view()),
    path('checkgreaternum',views.checkgreaternum),
    path('index',views.index),
    path('reg',views.registration),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('cart',views.cart),
    path('pd',views.product_detail),
    path('po',views.place_order),

]