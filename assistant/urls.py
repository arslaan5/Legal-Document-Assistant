from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('main/', views.query_view, name="index"),
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
]
