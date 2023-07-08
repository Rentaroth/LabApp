from django.urls import path
from .views import LoginView, LogoutView, UserCRUD

urlpatterns = [
  path('login', LoginView.as_view(), name='login'),
  path('logout', LogoutView.as_view(), name='logout'),
  path('user', UserCRUD.as_view(), name='user'),
  path('user/<int:user_id>/', UserCRUD.as_view(), name='user')
]
