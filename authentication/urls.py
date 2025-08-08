from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('users/<int:id>/penalties/', views.UserPenaltyView.as_view(), name='user-penalties'),
]
