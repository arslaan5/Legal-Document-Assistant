from django.urls import path
from . import views

urlpatterns = [
    path('', views.query_view, name="index"),
    path('end-session/', views.end_session, name='end_session'),
]