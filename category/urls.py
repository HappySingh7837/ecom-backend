from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_favorite/<int:id>/', views.add_favorite, name='add_favorite'),
]
