from django.urls import path
from .views import LoginView, LogoutView, UserMethods, GroupsMethods,JoiningGroups, InvitationsMethods, ExperimentsMethods, SamplesMethods, TestsMethods, ResultsMethods
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
  path('login', LoginView.as_view(), name='login'),
  path('logout', LogoutView.as_view(), name='logout'),
  path('user', UserMethods.as_view(), name='user'),
  path('user/<int:_id>', UserMethods.as_view(), name='user_by_id'),
  path('groups', GroupsMethods.as_view(), name='groups'),
  path('groups/new_member/<str:inv_token>', JoiningGroups.as_view(), name='groups_new_mwmber'),
  path('groups/<int:_id>', GroupsMethods.as_view(), name='groups_by_id'),
  path('invitations', InvitationsMethods.as_view(), name='invitations'),
  path('invitations/<int:_id>', InvitationsMethods.as_view(), name='invitations_by_id'),
  path('experiments', ExperimentsMethods.as_view(), name='experiments'),
  path('experiments/<int:_id>', ExperimentsMethods.as_view(), name='experiments_by_id'),
  path('samples', SamplesMethods.as_view(), name='samples'),
  path('samples/<int:_id>', SamplesMethods.as_view(), name='samples_by_id'),
  path('tests', TestsMethods.as_view(), name='tests'),
  path('tests/<int:_id>', TestsMethods.as_view(), name='tests_by_id'),
  path('results', ResultsMethods.as_view(), name='results'),
  path('results/<int:_id>', ResultsMethods.as_view(), name='results_by_id'),
  # YOUR PATTERNS
  path('schema/', SpectacularAPIView.as_view(), name='schema'),
  # Optional UI:
  path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
  path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
