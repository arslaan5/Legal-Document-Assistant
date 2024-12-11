from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf.urls import handler400, handler403, handler404, handler500

handler400 = 'views.error_view'
handler403 = 'views.error_view'
handler404 = 'views.error_view'
handler500 = 'views.error_view'

urlpatterns = [
    path('main/', views.query_view, name="index"),
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
]
