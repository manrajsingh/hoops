from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main' ),
    path('contact', views.contact, name='contact'),
    path('dashboard/<slug:slug>',views.dashboard, name="dashboard"),
]
