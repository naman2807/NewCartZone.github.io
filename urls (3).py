from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="shophome"),
    path("about/", views.about, name="aboutus"),
    path("contact/", views.contact, name="contactus"),

    path("search/", views.search, name="search"),
    path("product/<int:myid>", views.prodview, name="product"),
    path("checkout/", views.checkout, name="checkout"),
    path("handlerequest/", views.handlerequest, name="handlerequest")
]
