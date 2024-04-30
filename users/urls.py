from django.urls import path
from .views import register_view, login_view, authuser_view, logout_view

urlpatterns = [
    path('register/', register_view),
    path('login/', login_view),
    path('authenticate/', authuser_view),
    path('logout/', logout_view),
]
