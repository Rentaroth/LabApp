from django.urls import path
from .views import LoginView, LogoutView, UserMethods

urlpatterns = [
  path('login', LoginView.as_view(), name='login'),
  path('logout', LogoutView.as_view(), name='logout'),
  path('user', UserMethods.as_view(), name='user'),
  path('user/<int:user_id>', UserMethods.as_view(), name='user')
]
